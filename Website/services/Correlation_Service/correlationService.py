import time
import redis
from kafka import KafkaConsumer, KafkaProducer
import json

# Configuration
REDIS_HOST = "localhost"
REDIS_PORT = 6379
KAFKA_BROKER = "localhost:9092"
DETECTED_SERVICES_TOPIC = "final-services-topic"
DETECTED_GROUPS_TOPIC = "detected-group-topic"
FINAL_SERVICES_TOPIC = "services-with-groups-topic"
DLQ_TOPIC = "dead_letter_queue"
CORRELATION_TIMEOUT = 30  # Timeout in seconds

# Redis connection
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# Kafka setup
consumer_services = KafkaConsumer(
    DETECTED_SERVICES_TOPIC,
    DETECTED_GROUPS_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    group_id="correlation_service",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
)
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda m: json.dumps(m).encode("utf-8"),
)

def correlate_messages(uuid):
    """
    Check if all required parts are present for a UUID and construct the final message.
    """
    # Fetch correlated data from Redis
    data = redis_client.hgetall(uuid)
    if not data:
        return None

    # Extract and parse services and groups
    services = json.loads(data.get(DETECTED_SERVICES_TOPIC, "[]"))
    groups = json.loads(data.get(DETECTED_GROUPS_TOPIC, "[]"))

    # Construct the final message if both services and groups exist
    if services and groups:
        correlated_data = {
            "uuid": uuid,
            "filename": uuid[uuid.find(':')+1:],
            "services": services,
            "groups": groups
        }
        print("Correlated Data:", correlated_data)
        return correlated_data

    return None  # Not yet ready

def handle_timeout(uuid):
    """
    Handle expired correlation requests.
    """
    data = redis_client.hgetall(uuid)
    if data:
        # Publish the incomplete data to the DLQ
        producer.send(DLQ_TOPIC, {"uuid": uuid, "data": data, "reason": "timeout"})
        # Remove the key from Redis
        redis_client.delete(uuid)
        print(f"Timeout handled for UUID: {uuid}")

def process_message(topic, message):
    """
    Process incoming messages and correlate them.
    """
    print(message)
    uuid = message["uuid"]
    data = message["data"]
    file_name = message["filename"]

    # Update Redis with the new data
    redis_client.hset(f"{uuid}:{file_name}", topic, json.dumps(data))
    # Set an expiration for the key (timeout handling)
    redis_client.expire(f"{uuid}:{file_name}", CORRELATION_TIMEOUT)

    # Attempt to correlate
    correlated_data = correlate_messages(f"{uuid}:{file_name}")
    if correlated_data:
        # Publish fully correlated data to the final topic
        producer.send(FINAL_SERVICES_TOPIC, {"uuid": f"{uuid}:{file_name}", "data": correlated_data})
        # Remove the key from Redis
        redis_client.delete(f"{uuid}:{file_name}")
        print(f"Correlated message published for UUID: {uuid}:{file_name}")

def main():
    # Main loop
    print("Correlation Service is running...")
    for message in consumer_services:
        topic = message.topic
        value = message.value

        # Process the message
        process_message(topic, value)

        # Check for expired keys (timeouts)
        expired_keys = redis_client.keys("*")
        for key in expired_keys:
            if not redis_client.ttl(key):  # If TTL has expired
                handle_timeout(key)

if __name__ == "__main__":
    main()