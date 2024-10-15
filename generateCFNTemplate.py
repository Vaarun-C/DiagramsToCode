import os
import yaml
from ultralytics import YOLO
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from collections import defaultdict
import json
# from PIL import Image, ImageOps, ImageDraw
# import cv2
# import random

# Make directories if they don't exist
input_path = 'testArchitectureDiagrams'
output_path = 'testCFNTemplates'
detection_file = os.path.join(output_path, "detections.txt")
weight_for_model = "./best_tuned.pt"
# architecture_image = Image.open(input_path + "/image67.png")
# background_size = (1000, 1000)
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

# Pad input image with white
# width, height = architecture_image.size

def hsl_to_rgb(h):
    x =  (1 - abs((h / 60) % 2 - 1))  # Second largest component
    if 0 <= h < 60:
        r_, g_, b_ = 1, x, 0
    elif 60 <= h < 120:
        r_, g_, b_ = x, 1, 0
    elif 120 <= h < 180:
        r_, g_, b_ = 0, 1, x
    elif 180 <= h < 240:
        r_, g_, b_ = 0, x, 1
    elif 240 <= h < 300:
        r_, g_, b_ = x, 0, 1
    else:
        r_, g_, b_ = 1, 0, x
    r = round((r_) * 255)
    g = round((g_) * 255)
    b = round((b_) * 255)
    return (r, g, b)

# # Function to draw bounding box and labels
# def draw_boxes(image, boxes, font_scale=0.5, font_thickness=2):

#     grouping_dict = {}

#     for i, (x1, y1, x2, y2, label) in enumerate(boxes):

#         if(((x1//10)*10, (y1//10)*10, (x2//10)*10, (y2//10)*10) in grouping_dict):
#             rand_number = grouping_dict[((x1//10)*10, (y1//10)*10, (x2//10)*10, (y2//10)*10)]
#         else:
#             rand_number = random.randint(0, 360)
#             grouping_dict[((x1//10)*10, (y1//10)*10, (x2//10)*10, (y2//10)*10)] = rand_number

#         # Choose a font
#         font = cv2.FONT_HERSHEY_SIMPLEX
#         text_size = cv2.getTextSize(label, font, font_scale, font_thickness)[0]
        
#         # Positioning for the text: start at y1 and move text below previous ones
#         text_x = x1
#         text_y = y1 - 2
        
#         # Ensure text is inside image bounds and not above the top of the image
#         if text_y < text_size[1]:
#             text_y = y1 + text_size[1] + 5
        
#         # Adjust if previous text labels are present
#         text_y += i * (text_size[1] + 5)  # Stack text vertically
        
#         # Draw bounding box
#         cv2.rectangle(image, (x1, y1), (x2, y2), color=hsl_to_rgb(rand_number), thickness=2)
        
#         # Draw filled rectangle behind the text
#         cv2.rectangle(image, (text_x, text_y - text_size[1] - 2), 
#                       (text_x + text_size[0], text_y), color=hsl_to_rgb(rand_number), thickness=cv2.FILLED)
        
#         # Put the text on the image
#         cv2.putText(image, label, (text_x, text_y - 2), font, font_scale, (0,0,0), font_thickness)

# # Find the difference between width and height
# if width != height:
#     padding = (0, 0, 0, 0)  # (left, top, right, bottom)
#     if width > height:
#         padding = (0, (width - height) // 2, 0, (width - height + 1) // 2)  # Padding top and bottom
#     else:
#         padding = ((height - width) // 2, 0, (height - width + 1) // 2, 0)  # Padding left and right

#     # Apply padding
#     padded_image = ImageOps.expand(architecture_image, padding, fill=(255, 255, 255))  # You can change the fill color

#     padded_image.save(input_path + "/image67.png")
architecture_image = input_path + "/testSQ9.png"
# displayImage = cv2.imread(input_path + "/testSQ12.png")

# # Predict using best weights from the model
model = YOLO(weight_for_model)
results = model.predict(architecture_image, save=True, line_width=1, imgsz=1000, conf=0.5)

detected_classes = []
for result in results:
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
        count_of_classes[cls_name] =+ 1
        
        service_template = {
            "Type": icon_template["Type"],
            "Properties": icon_template["Properties"]
        }

        data["Resources"][service_name] = service_template
    else:
        print(f"No additional details found for class {cls_name}")

with open(output_path + "/template.yaml", 'w') as file:
    yaml.dump(data, file, default_flow_style=False)  # default_flow_style=False makes the output more readable

with open(output_path + "/template.json", 'w') as file:
    file.write(json.dumps(data, indent=4))

# # Collect boxes and labels
# boxes_with_labels = []
# for result in results:
#     for box in result.boxes: # type: ignore
#         # Get the bounding box coordinates
#         x1, y1, x2, y2 = map(int, box.xyxy[0])
        
#         # Get the class id and confidence score
#         class_id = int(box.cls)
#         confidence = box.conf[0]
        
#         # Generate the label (class name and confidence)
#         label = f"{model.names[class_id]}: {confidence:.2f}"
        
#         # Add bounding box and label to the list
#         boxes_with_labels.append((x1, y1, x2, y2, label))

# # Sort the bounding boxes by their y1 coordinate to stack text labels properly
# boxes_with_labels.sort(key=lambda x: x[1])

# # Draw bounding boxes and labels on the image
# draw_boxes(displayImage, boxes_with_labels)

# # Save the output image
# cv2.imwrite("output_image_with_stacked_labels.jpg", displayImage)

# Get the names of detected classes from the detections
# if os.path.exists(detection_file):
#     with open(detection_file, "r") as file:
#         lines = file.readlines()
#         detected_cls_ids = [int(line.split()[0]) for line in lines]

#     with open('data.yaml', 'r') as data_file:
#         data = yaml.safe_load(data_file)
#         detected_classes = [data["names"][cls_id] for cls_id in detected_cls_ids]

#     print("Detected classes")
#     print("-"*50)
#     for d in detected_classes:
#         print(d)
#     print("-"*50)
# else:
#     print(f"No detections found in {detection_file}.")

