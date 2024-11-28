from PIL import Image, ImageDraw
import random
import os
from collections import defaultdict
import json
import random

background_size_limits = (700, 2500)
image_size = (80, 80)
class_usage = defaultdict(int)
resizing_size = (0.7, 1.5)
line_wid_var = 3

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
    r = round((r_) * 150)
    g = round((g_) * 150)
    b = round((b_) * 150)
    return (r, g, b)

def get_random_line_style():
    # Return either None for solid line or tuple for dashed line
    if random.choice([True, False]):
        return None  # Solid line
    else:
        # Random dash pattern (dash length, gap length)
        return (5, 15)

def create_rect_position(max_width, max_height, min_size=200, max_size=500):
    # Generate random width and height for rectangle
    width = random.randint(min_size, max_size)
    height = random.randint(min_size, max_size)
    
    # Generate random position
    x = random.randint(0, max_width - width)
    y = random.randint(0, max_height - height)
    
    # Check for overlap with existing positions
    new_rect = (x, y, x + width, y + height)

    # If we couldn't find non-overlapping position, return None
    return new_rect

def draw_dashed_line(draw, coordinates, color, dash_length, gap_length, width):
    x1, y1, x2, y2 = coordinates
    # Calculate line length and angle
    import math
    length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    angle = math.atan2(y2 - y1, x2 - x1)
    
    # Draw dashed line segments
    current_length = 0
    drawing = True  # Start with drawing (not gap)
    
    while current_length < length:
        segment_length = dash_length if drawing else gap_length
        next_length = min(current_length + segment_length, length)
        
        if drawing:
            start_x = x1 + math.cos(angle) * current_length
            start_y = y1 + math.sin(angle) * current_length
            end_x = x1 + math.cos(angle) * next_length
            end_y = y1 + math.sin(angle) * next_length
            draw.line((start_x, start_y, end_x, end_y), fill=color, width=width)
        
        current_length = next_length
        drawing = not drawing

def draw_dashed_rectangle(draw, coordinates, color, dash_length, gap_length, width):
    x1, y1, x2, y2 = coordinates
    # Draw four sides of rectangle with dashed lines
    draw_dashed_line(draw, (x1, y1, x2, y1), color, dash_length, gap_length, width)  # Top
    draw_dashed_line(draw, (x2, y1, x2, y2), color, dash_length, gap_length, width)  # Right
    draw_dashed_line(draw, (x2, y2, x1, y2), color, dash_length, gap_length, width)  # Bottom
    draw_dashed_line(draw, (x1, y2, x1, y1), color, dash_length, gap_length, width)  # Left

def create_image(image_num=0, output_folder="output", imp_categories=[]):
    background_size = (random.randint(*background_size_limits), random.randint(*background_size_limits))
    background = Image.new("RGB", background_size, "white")
    num_retries = 20
    width,height = background_size
    draw = ImageDraw.Draw(background)

    # Choose a random set of non-overlapping points on the background for 1000X1000
    # num_points = random.randint(25, 35)

    # Generate rectangles
    num_rectangles = int((background_size[0]*background_size[1]*5)/1000000) + random.randint(0, 4)
    for _ in range(num_rectangles):
        rect_pos = create_rect_position(width, height)
            
        # Random color and line style
        color = hsl_to_rgb(random.randint(0, 360))
        line_width = line_wid_var
        dash_pattern = get_random_line_style()
            
        # If dash pattern is specified, create dashed outline manually
        if dash_pattern:
            x1, y1, x2, y2 = rect_pos
            draw_dashed_rectangle(draw, (x1, y1, x2, y2), color, 
                                dash_pattern[0], dash_pattern[1], line_width)
        else:
            # Draw rectangle
            draw.rectangle(rect_pos, outline=color, width=line_width)
    
    # Generate lines
    num_lines = 4*num_rectangles
    for _ in range(num_lines):

        # Generate random line endpoints
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)

        # Horizontal
        if random.choice([True, False]):
            x2 = random.randint(0, width)
            y2 = y1

        #Vertical
        else:
            x2 = x1
            y2 = random.randint(0, height)
        
        # Random color and line style
        color = hsl_to_rgb(random.randint(0, 360))
        line_width = line_wid_var
        dash_pattern = get_random_line_style()
        
        if dash_pattern:
            draw_dashed_line(draw, (x1, y1, x2, y2), color, 
                           dash_pattern[0], dash_pattern[1], line_width)
        else:
            draw.line((x1, y1, x2, y2), fill=color, width=line_width)

    # Calculate new number of points based on background size
    num_points = int((background_size[0]*background_size[1]*35)/1000000) + random.randint(-10, 10)
    # print(f"SIZE CHOSEN: \u001b[31m{background_size}\u001b[0m AND NUMBER OF POINTS: \u001b[31m{num_points}\u001b[0m")
    points = set()

    num_of_wrong_classes = int(0.7 * num_points)

    while len(points) < num_points:
        x = random.randint(0, background_size[0] - image_size[0])
        y = random.randint(0, background_size[1] - image_size[1])
        new_point = (x, y)

        overlapping = False
        for point in points:
            if abs(point[0] - new_point[0]) < resizing_size[1]*image_size[0] and abs(point[1] - new_point[1]) < resizing_size[1]*image_size[1]:
                overlapping = True
                num_retries -= 1
                break

        if not overlapping:
            num_retries = 20
            points.add(new_point)

        if num_retries <= 0:
            num_points -= 1

    # Paste randomly chosen images from ./augmented folder onto the background and also create the annotation file based on the point positions
    augmented_folder = "./augmented"

    chosen_categories = []
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(output_folder + "/images", exist_ok=True)
    os.makedirs(output_folder + "/labels", exist_ok=True)

    with open(f"{output_folder}/labels/image{image_num}.txt", "w") as file:
        for point in points:
            x, y = point

            if num_of_wrong_classes > 0:
                category = random.choice(list(set(categories)-set(imp_categories)))
                num_of_wrong_classes -= 1
            else:
                try:
                    min_usage = min(class_usage.values()) if class_usage else 0
                    least_used_classes = [cat for cat in imp_categories if class_usage[cat] == min_usage]
                    category = random.choice(least_used_classes)
                    class_usage[category] += 1
                except Exception as e:
                    # print(min_usage, category, least_used_classes, imp_categories)
                    raise e

            chosen_categories.append(category)
            folder_path = os.path.join(augmented_folder, category)
            images = os.listdir(folder_path)
            image_name = random.choice(images)
            image_path = os.path.join(folder_path, image_name)
            image = Image.open(image_path)
            # image = image.resize(image_size)

            resize_chance = random.random()
            if resize_chance < 0.5:  # 50% chance to resize either width or height
                resize_factor = random.uniform(resizing_size[0], resizing_size[1])  # Random width scale between 50% to 150%
                new_dim = int(image_size[0] * resize_factor)
                new_width = new_height = new_dim
                # if random.random() < 0.5:
                #     # Resize only the width
                #     width_factor = random.uniform(resizing_size[0], resizing_size[1])  # Random width scale between 50% to 150%
                #     new_width = int(image_size[0] * width_factor)
                #     new_height = image_size[1]  # Keep height the same
                # else:
                #     # Resize only the height
                #     height_factor = random.uniform(resizing_size[0], resizing_size[1])  # Random height scale between 50% to 150%
                #     new_width = image_size[0]  # Keep width the same
                #     new_height = int(image_size[1] * height_factor)
            else:
                # Keep original size
                new_width, new_height = image_size

            # width, height = image_size

            image = image.resize((new_width, new_height))

            center_x = (x + new_width / 2) / background_size[0]
            center_y = (y + new_height / 2) / background_size[1]
            bbox_width = new_width / background_size[0]
            bbox_height = new_height / background_size[1]

            if(category in imp_categories):
                file.write(f"{imp_categories.index(category)} {center_x} {center_y} {bbox_width} {bbox_height}\n")
            background.paste(image, (x, y))

            # Write the distribution of the categories to a file
            # with open(f"{output_folder}/category_distribution.txt", "w") as dist_file:
            #     for cat, count in class_usage.items():
            #         dist_file.write(f"{cat}: {count}\n")

    # Save it to the output folder
    background.save(f"{output_folder}/images/image{image_num}.png")

    return chosen_categories

def validate_output():
    number_of_images = len(os.listdir("datasetCategory1_0_0/train/images"))
    number_of_labels = len(os.listdir("datasetCategory1_0_0/train/labels"))

    assert number_of_images == number_of_labels, f"Number of images and labels do not match: {number_of_images} images, {number_of_labels} labels"

    # Draw a bounding box on the image for each label
    for i in range(5):
        image_path = f"datasetCategory1_0_0/train/images/image{i}.png"
        label_path = f"datasetCategory1_0_0/train/labels/image{i}.txt"
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        background_size = image.size

        with open(label_path, "r") as file:
            for line in file:
                category, x, y, w, h = line.split()
                x, y, w, h = float(x), float(y), float(w), float(h)
                x1, y1 = x - w/2, y - h/2
                x2, y2 = x + w/2, y + h/2

                x1, y1, x2, y2 = x1*background_size[0], y1*background_size[1], x2*background_size[0], y2*background_size[1]

                draw.rectangle([x1, y1, x2, y2], outline="red", width=8)

                # Add the respective category name under the bounding box
                category = int(category)
                with open("class_names_categories.txt", "r") as class_file:
                    categories = class_file.read().split("\n")
                    # categories = [c for c in categories if c not in classes_to_ignore]
                    category_name = categories[category]

                draw.text((x1, y2), category_name, fill="red")

        image.show()

if __name__ == "__main__":

    # categories = []
    # with open("class_names_298.txt", "r") as file:
    #     categories = file.read().split("\n")
    # assert len(categories) != 0, "No categories found in class_names.txt"

    # important_categories = []
    # with open("class_names_categories.txt", "r") as file:
    #     important_categories = file.read().split("\n")
    # assert len(important_categories) != 0, "No categories found in class_names_imp.txt"

    # classes_to_ignore = set([
    # "Arch_AWS-Elemental-Appliances-&-Software_64",
    # "Arch_AWS-Elemental-Conductor_64",
    # "Arch_AWS-Elemental-Delta_64",
    # "Arch_AWS-Elemental-Live_64",
    # "Arch_Amazon-Pinpoint-APIs_64",
    # "Arch_Amazon-Pinpoint_64",
    # "Arch_Amazon-WorkDocs_64",
    # "Arch_Amazon-WorkDocs-SDK_64",
    # "Arch_TensorFlow-on-AWS_64",
    # "Arch_AWS-Marketplace_Dark_64",
    # "Arch_AWS-Marketplace_Light_64"
    # ])

    # categories = [c for c in categories if c not in classes_to_ignore]

    # number_of_images_train = 10
    # number_of_images_val = int(0.2 * number_of_images_train)

    # for i in range(number_of_images_train):
    #     create_image(i, "output/train", important_categories)
    #     print(f"Generated image for training {i+1}/{number_of_images_train}", end="\r")

    # for i in range(number_of_images_val):
    #     create_image(i, "output/val", important_categories)
    #     print(f"Generated image for validation {i+1}/{number_of_images_val}", end="\r")

    # with open("tempOutput.txt", "w") as file:
    # # print("CLASSES DISTRIBUTION")
    # # print(class_usage)
    #     file.write(json.dumps(class_usage, indent=4))
    validate_output()
