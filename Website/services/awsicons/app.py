from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import io
from ultralytics import YOLO

app = FastAPI()
model_names = None
model = YOLO("298_icons_best.pt")

CLS_NAME_TO_TYPE = {
    "Arch_Amazon-Elastic-Container-Service_64": "AWS::ECS::Cluster",
    "Arch_Amazon-Simple-Storage-Service_64": "AWS::S3::Bucket",
    "Arch_AWS-Lambda_64": "AWS::Lambda::Function",
    "Arch_Amazon-RDS_64": "AWS::RDS::DBInstance",
    "Arch_AWS-Fargate_64": "AWS::ECS::Cluster",
    "Arch_Amazon-EC2_64": "AWS::EC2::Instance"
}

@app.post("/getawsicons")
async def root(architectureDiagram: UploadFile = File(...)):
    global model_names

    # Read the image file and convert to PIL Image
    image_data = await architectureDiagram.read()
    image = Image.open(io.BytesIO(image_data))

    all_classes = set(range(298))
    removed_classes = set([57]) #
    allowed_classes = list(all_classes-removed_classes)

    # Predict using best weights from the model
    results = model.predict(image, save=False, classes=allowed_classes, conf=0.6)
    model_names = model.names

    types = get_detected_types(results[0])

    return {"message": types}

def get_detected_types(result) -> list[str]:
    detected_classes_types = []
    for box in result.boxes: # type: ignore
        class_id = int(box.cls) # Get the class id for the current box
        class_name = model_names[class_id]# type: ignore  Get the class name from the model's names list
        try:
            detected_classes_types.append(CLS_NAME_TO_TYPE[class_name])
        except:
            print(class_name, "not in Mongo yet !!!!")
    return detected_classes_types