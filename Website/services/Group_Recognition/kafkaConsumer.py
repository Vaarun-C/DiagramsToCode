from kafka import KafkaConsumer, KafkaProducer
from PIL import Image, UnidentifiedImageError
import io
import logging
import json
from YOLOModel import yolomodel
import base64
import numpy as np
import cv2
from PIL import Image, UnidentifiedImageError
from states import Group, detection_object
from YOLOModel import yolomodel
from RectangleDetector import detectRectangles
from kafka.errors import KafkaError

# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GroupDetectionConsumer")

model = yolomodel()

# Kafka configuration
KAFKA_BROKER = "localhost:9092"
IMAGE_TOPIC = "image_topic"
DETECTED_SERVICES_TOPIC = "detected-group-topic"
DLQ_TOPIC_NAME = "group-dead-letter-queue"

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    IMAGE_TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    group_id="group-detection-group",
    auto_offset_reset="earliest",  # Start from the beginning if no offsets are committed
    enable_auto_commit=True
)

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

def get_dist(a,b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

def process_image(image_data: bytes) -> list:
    """
    Processes the image using YOLO model and returns detections.
    """
    try:
        image = Image.open(io.BytesIO(image_data))
        image.verify()  # Verify it's actually an image
        img_pillow = Image.open(io.BytesIO(image_data))  # Reopen after verify
        img_cv2 = cv2.cvtColor(np.array(img_pillow), cv2.COLOR_RGBA2BGR)
        
        # Run category icon detection
        try:
            detections = [obj for obj in model.predict(img_pillow)]
            logger.info(f"Category icon detections: {detections}")
        except Exception as e:
            logger.error(f"Error during category icon detection: {str(e)}")
            raise

        # Run rectangle detection
        try:
            rectangle_outlines = detectRectangles(img_cv2)
            logger.info(f"Rectangle detections: {rectangle_outlines}")
        except Exception as e:
            logger.error(f"Error during rectangle detection: {str(e)}")
            raise

        # assign icons to rectangles
        detected_groups = []
        for det in detections:
            x, y = det.box[2:]
            selected_i = 0
            min_dist = np.inf
            for i, rect in enumerate(rectangle_outlines):
                dist = get_dist((x,y),rect[:2])
                if dist < min_dist:
                    min_dist = dist
                    selected_i = i
            rect = rectangle_outlines.pop(i)
            detected_groups.append(Group(*rect, group_type=det.classType))

        # add remaining rectangles without icons
        for rect in rectangle_outlines:
            detected_groups.append(Group(*rect))

        detected_groups = [d.to_dict() for d in detected_groups]

        return detected_groups

    except UnidentifiedImageError:
        logger.error("Invalid or corrupted image file.")
        return []
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        return []

def handle_dead_letter(message):
    """
    Publishes the failed message to the dead-letter queue.
    """
    try:
        producer.send(DLQ_TOPIC_NAME, message)
        logger.info(f"Message sent to Dead Letter Queue: {message}")
    except KafkaError as e:
        logger.critical(f"Failed to send message to DLQ: {str(e)}")

def main():
    for message in consumer:
        try:
            payload = message.value
            logger.info(f"Received message: {payload}")

            image_data = payload.get("content", None)
            if image_data is None:
                logger.error("No image data found in the message.")
                continue

            image_data = base64.b64decode(image_data)

            # Process the image and get detections
            detections = process_image(io.BytesIO(image_data).getvalue())
            consumer.commit()

            # Publish results to the Detected Services Topic
            result = {
                "uuid": payload.get("uuid", "unknown"),
                "filename": payload.get("filename", "unknown"),
                "data": detections
            }
            print(result)
            producer.send(DETECTED_SERVICES_TOPIC, result)
            logger.info(f"Sent detections to topic '{DETECTED_SERVICES_TOPIC}': {result}")
        except Exception as e:
            logger.error(f"Unexpected error during message processing: {e}")
            handle_dead_letter(payload)

if __name__ == "__main__":
    main()
