from fastapi import FastAPI, File, Form, UploadFile, BackgroundTasks, HTTPException, WebSocket
from kafka import KafkaProducer
import uuid
import base64
import json
import redis
import asyncio
from fastapi.middleware.cors import CORSMiddleware

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
kafka_servers = ["localhost:9092"]
background_tasks = BackgroundTasks()

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=kafka_servers,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8")
)

# Redis setup for tracking requests
redis_client = redis.StrictRedis(host="localhost", port=6379, decode_responses=True)

@app.post("/generateawstemplate")
async def process_image(UUID: str = Form(...), ArchitectureDiagram: UploadFile = File(...)):
    image_content = await ArchitectureDiagram.read()


    return {"ImageStatus": "Image received", "image_id": uuid}

@app.post("/result/")
async def get_result(uuid: str = Form(...)):
    result = redis_client.get(uuid)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found or expired")
    
    if result == "processing":
        return {"status": "Processing"}

    # Delete the result from Redis to avoid stale data
    redis_client.delete(uuid)

    return {"status": "Completed", "result": result}