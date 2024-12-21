from kafka import KafkaConsumer
import redis
import json
import os
import logging

# Kafka configuration
TEMPLATE_TOPIC = "template-topic"
KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL", "localhost:9092")
# KAFKA_BROKER = "localhost:9092"
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TemplateConsumer")

consumer = KafkaConsumer(
    TEMPLATE_TOPIC,
    bootstrap_servers=[KAFKA_BROKER_URL],
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
)

# Redis setup
redis_client = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True
)

for message in consumer:
    result = message.value
    correlation_id = result.get("uuid")

    if correlation_id:
        # Store the final result in Redis
        redis_client.set(correlation_id, json.dumps(result), ex=60 * 5)  # Expire after 5 minutes
        print(f"Result stored for UUID {correlation_id}")
