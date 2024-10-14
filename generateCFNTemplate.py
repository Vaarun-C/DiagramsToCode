import os
import yaml
from ultralytics import YOLO
from PIL import Image, ImageOps, ImageDraw

# Make directories if they don't exist
input_path = 'testArchitectureDiagrams'
output_path = 'testCFNTemplates'
detection_file = os.path.join(output_path, "detections.txt")
weight_for_model = "./best.pt"
architecture_image = Image.open(input_path + "/image67.png")
background_size = (1000, 1000)

# Make directories if they don't exist
os.makedirs(input_path, exist_ok=True)
os.makedirs(output_path, exist_ok=True)

# Pad input image with white
width, height = architecture_image.size

# Find the difference between width and height
if width != height:
    padding = (0, 0, 0, 0)  # (left, top, right, bottom)
    if width > height:
        padding = (0, (width - height) // 2, 0, (width - height + 1) // 2)  # Padding top and bottom
    else:
        padding = ((height - width) // 2, 0, (height - width + 1) // 2, 0)  # Padding left and right

    # Apply padding
    padded_image = ImageOps.expand(architecture_image, padding, fill=(255, 255, 255))  # You can change the fill color

    padded_image.save(input_path + "/padded_test.png")
    architecture_image = input_path + "/padded_test.png"

# Predict using best weights from the model
model = YOLO(weight_for_model)
results = model.predict(architecture_image, save=True)
for r in results:
    r.save_txt(detection_file)

# Get the names of detected classes from the detections
detected_classes = []
if os.path.exists(detection_file):
    with open(detection_file, "r") as file:
        lines = file.readlines()
        detected_cls_ids = [int(line.split()[0]) for line in lines]

    with open('data.yaml', 'r') as data_file:
        data = yaml.safe_load(data_file)
        detected_classes = [data["names"][cls_id] for cls_id in detected_cls_ids]

    print("Detected classes")
    print("-"*50)
    for d in detected_classes:
        print(d)
    print("-"*50)
else:
    print(f"No detections found in {detection_file}.")


# Testing
image = Image.open(input_path + "/image67.png")
draw = ImageDraw.Draw(image)

with open(detection_file, "r") as file:
    for i,line in enumerate(file):
        category, x, y, w, h = line.split()
        x, y, w, h = float(x), float(y), float(w), float(h)
        x1, y1 = x - w/2, y - h/2
        x2, y2 = x + w/2, y + h/2

        x1, y1, x2, y2 = x1*background_size[0], y1*background_size[1], x2*background_size[0], y2*background_size[1]

        draw.rectangle([x1, y1, x2, y2], outline="red")

        # Add the respective category name under the bounding box
        category_name = detected_classes[i]

        draw.text((x1, y2), category_name, fill="red")

image.show()