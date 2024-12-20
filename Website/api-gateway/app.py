from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from kafka import KafkaProducer
import base64
import json
import redis
import os
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify allowed domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Kafka Configuration
IMAGE_TOPIC = "image_topic"
KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL", "localhost:9092")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER_URL],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8")
)

# Redis setup for tracking requests
redis_client = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True
)

@app.post("/generateawstemplate")
async def process_image(
    UUID: str = Form(...),  # Ensure UUID is passed as a form field
    ArchitectureDiagram: UploadFile = File(...)  # Ensure the file is passed correctly
):
    # Read the image content
    print(ArchitectureDiagram.filename)
    image_content = await ArchitectureDiagram.read()
    encoded_image = base64.b64encode(image_content).decode("utf-8")

    redis_client.set(UUID, "processing", ex=60 * 5)  # Expire after 5 minutes

    # Prepare the message payload
    message = {
        "uuid": UUID,
        "filename": ArchitectureDiagram.filename,
        "content": encoded_image,
        "timestamp": time.time()
    }

    try:
        producer.send(
            IMAGE_TOPIC,
            key=UUID,
            value=message
        )
        print("Pushed to topic:", IMAGE_TOPIC)
        producer.flush()
    except Exception as e:
        return {"ImageStatus": "Failed", "error": str(e)}

    return {"ImageStatus": "Image received", "image_id": UUID}

@app.get("/result/")
async def get_result(uuid: str):
    result = redis_client.get(uuid)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found or expired")
    
    if result == "processing":
        return {"status": "Processing"}

    # Delete the result from Redis to avoid stale data
    redis_client.delete(uuid)

    return {"status": "Completed", "result": result}