import time
from kafka import KafkaConsumer
import json

# Consumer setup
consumer = KafkaConsumer(
    'detected-services-topic',  # Replace with your topic
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='test-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))  # Deserialize JSON
)

for message in consumer:
    # Debugging message: print entire message metadata
    print(f"Received Kafka Message Metadata: {message}")  
    
    # Get payload (the actual message content)
    payload = message.value
    
    # Check and debug timestamp
    kafka_timestamp = message.timestamp
    print(f"Kafka Timestamp (ms): {kafka_timestamp}")  # Timestamp in milliseconds
    
    # Convert timestamp from milliseconds to seconds
    kafka_timestamp_seconds = kafka_timestamp / 1000
    print(f"Converted Kafka Timestamp (seconds): {kafka_timestamp_seconds}")
    
    # Calculate latency
    end_to_end_latency = time.time() - kafka_timestamp_seconds
    print(f"UUID: {payload.get('uuid')} | End-to-End Latency: {end_to_end_latency:.2f} seconds")

    consumer.commit()