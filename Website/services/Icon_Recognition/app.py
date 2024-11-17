from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import io
from fastapi.middleware.cors import CORSMiddleware
from YOLOModel import yolomodel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify allowed domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = yolomodel()

@app.post("/getawsicons")
async def root(architectureDiagram: UploadFile = File(...)):
    # Read the image file and convert to PIL Image
    image_data = await architectureDiagram.read()
    image = Image.open(io.BytesIO(image_data))

    detections = [obj.to_dict() for obj in model.predict(image)]

    return JSONResponse(content=detections)