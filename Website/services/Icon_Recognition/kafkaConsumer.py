from kafka import KafkaConsumer, KafkaProducer
from PIL import Image, UnidentifiedImageError
import io
import logging
import json
from YOLOModel import yolomodel
import base64
from kafka.errors import KafkaError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("IconDetectionConsumer")

model = yolomodel()

# Kafka configuration
KAFKA_BROKER = "localhost:9092"
IMAGE_TOPIC = "image_topic"
DETECTED_SERVICES_TOPIC = "detected-services-topic"
DLQ_TOPIC_NAME = "icon-dead-letter-queue"

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    IMAGE_TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    group_id="icon-detection-group",
    auto_offset_reset="earliest",  # Start from the beginning if no offsets are committed
    enable_auto_commit=True
)

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

def process_image(image_data: bytes) -> list:
    """
    Processes the image using YOLO model and returns detections.
    """
    try:
        image = Image.open(io.BytesIO(image_data))
        image.verify()
        image = Image.open(io.BytesIO(image_data))
        
        # Run YOLO predictions
        detections = [obj.to_dict() for obj in model.predict(image)]
        logger.info(f"Detections: {detections}")
        return detections
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
                "detections": detections
            }
            producer.send(DETECTED_SERVICES_TOPIC, result)
            logger.info(f"Sent detections to topic '{DETECTED_SERVICES_TOPIC}': {result}")
        except Exception as e:
            logger.error(f"Unexpected error during message processing: {e}")
            handle_dead_letter(payload)

if __name__ == "__main__":
    main()
