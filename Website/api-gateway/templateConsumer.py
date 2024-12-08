from kafka import KafkaConsumer
import redis
import json

# Kafka configuration
TEMPLATE_TOPIC = "template-topic"
KAFKA_BROKER = "localhost:9092"
REDIS_PORT = 6380 # Second instance of redis

consumer = KafkaConsumer(
    TEMPLATE_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
)

# Redis setup
redis_client = redis.StrictRedis(host="localhost", port=REDIS_PORT, decode_responses=True)

for message in consumer:
    result = message.value
    correlation_id = result.get("uuid")

    print(result)

    if correlation_id:
        # Store the final result in Redis
        redis_client.set(correlation_id, json.dumps(result), ex=60 * 5)  # Expire after 5 minutes
        print(f"Result stored for UUID {correlation_id}")
