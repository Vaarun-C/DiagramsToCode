from kafka import KafkaConsumer, KafkaProducer
import json
import logging
from CodeGenerator import template_generator
import logging

# Kafka configuration
KAFKA_BROKER = "localhost:9092"
INFO_TOPIC = "services-with-groups-topic"
TEMPLATE_TOPIC = "template-topic"
DLQ_TOPIC = "template-dead-letter-queue"

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TemplateConsumer")

generator = template_generator()

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    INFO_TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    group_id="template-group",
    auto_offset_reset="earliest",
)

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda x: json.dumps(x).encode("utf-8"),
)

def process_services(items):
    """
    Generate a CloudFormation template.
    """


def handle_dead_letter(message):
    """
    Send the failed message to a dead-letter queue.
    """
    try:
        producer.send(DLQ_TOPIC, message)
        logger.info(f"Message sent to Dead Letter Queue: {message}")
    except Exception as e:
        logger.error(f"Failed to send message to DLQ: {e}")

def main():
    for message in consumer:
        try:
            payload = message.value
            logger.info(f"Received message: {payload}")

            data = payload.get("data")
            if not data:
                logger.error("No 'data' found in the message payload.")
                continue

            services = data.get("services")
            if not services:
                logger.error("No 'services' found in the message payload.")
                continue

            groups = data.get("groups")
            if not groups:
                logger.error("No 'groups' found in the message payload.")
                continue

            template = generator.create_template(data.get("filename"), services)

            UUID_without_filename = payload.get("uuid", "unknown")[:payload.get("uuid", "unknown").find(":")]

            # Prepare the result message
            result = {
                "uuid": UUID_without_filename,
                "filename": data.get("filename", "unknown"),
                "template": template
            }

            # Send the result to the target topic
            producer.send(TEMPLATE_TOPIC, result)
            logger.info(f"Sent suggestions to topic '{TEMPLATE_TOPIC}': {result}")

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            handle_dead_letter(message.value)

if __name__ == "__main__":
    main()
