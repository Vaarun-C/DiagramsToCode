import os
import yaml
from ultralytics import YOLO
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from collections import defaultdict
import json

# Make directories if they don't exist
input_path = 'testArchitectureDiagrams'
output_path = 'testCFNTemplates'
detection_file = os.path.join(output_path, "detections.txt")
weight_for_model = "/Users/varun/base/projects/DiagramsToCode/train12/weights/best.pt"
architecture_path = "/Users/varun/base/projects/DiagramsToCode/test"
uri = "mongodb+srv://varuncblr:VarunVikas@workflowmanagement.teozhuj.mongodb.net/?retryWrites=true&w=majority&appName=workflowManagement"
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['DiagramsToCode']
icons_collection = db['icons']

# Make directories if they don't exist
os.makedirs(input_path, exist_ok=True)
os.makedirs(output_path, exist_ok=True)

# Predict using best weights from the model
model = YOLO(weight_for_model)
all_classes = set(range(298))
removed_classes = set([57])
allowed_classes = list(all_classes-removed_classes)
results = model.predict(architecture_path, save=True, line_width=1, classes=allowed_classes, conf=0.6)

for i, result in enumerate(results):
    detected_classes = []
    for box in result.boxes: # type: ignore
        # Get the class id for the current box
        class_id = int(box.cls)
        
        # Get the class name from the model's names list
        class_name = model.names[class_id]
        
        # Add the class name to the list of detected classes
        detected_classes.append(class_name)

    # Write template
    data = {
        "AWSTemplateFormatVersion": '2010-09-09',
        "Description": "CloudFormation Template",
        "Resources": {}
    }
    count_of_classes = defaultdict(int)

    for cls_name in detected_classes:

        # Remove '_64'
        cls_name = cls_name.replace('_64', '')
        service_template = {}
        icon_template = icons_collection.find_one({"name": cls_name})
        
        if icon_template:

            cleaned_name = cls_name.replace('-', '').replace('_', '').replace('ArchAmazon', '')
            service_name = "My"+cleaned_name+str(count_of_classes[cls_name] + 1)
            count_of_classes[cls_name] += 1
            
            service_template = {
                "Type": icon_template["Type"],
                "Properties": icon_template["Properties"]
            }

            data["Resources"][service_name] = service_template
        else:
            print(f"No additional details found for class {cls_name}")

    with open(output_path + f"/template{i}.yaml", 'w') as file:
        yaml.dump(data, file, default_flow_style=False)  # default_flow_style=False makes the output more readable

    with open(output_path + f"/template{i}.json", 'w') as file:
        file.write(json.dumps(data, indent=4))