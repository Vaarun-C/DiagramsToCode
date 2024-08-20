from PIL import Image, ImageDraw
import random
import os
from collections import defaultdict

background_size = (1000, 1000)
image_size = (80, 80)
class_usage = defaultdict(int)

def create_image(image_num=0, output_folder="output"):
    background = Image.new("RGB", background_size, "white")

    # Choose a random set of non-overlapping points on the background
    num_points = random.randint(10, 25)
    points = set()

    while len(points) < num_points:
        x = random.randint(0, background_size[0] - image_size[0])
        y = random.randint(0, background_size[1] - image_size[1])
        new_point = (x, y)

        overlapping = False
        for point in points:
            if abs(point[0] - new_point[0]) < image_size[0] and abs(point[1] - new_point[1]) < image_size[1]:
                overlapping = True
                break

        if not overlapping:
            points.add(new_point)

    # Paste randomly chosen images from ./augmented folder onto the background and also create the annotation file based on the point positions
    augmented_folder = "./augmented"
    
    chosen_categories = []
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(output_folder + "/images", exist_ok=True)
    os.makedirs(output_folder + "/labels", exist_ok=True)

    with open(f"{output_folder}/labels/image{image_num}.txt", "w") as file:
        for point in points:
            x, y = point

            min_usage = min(class_usage.values()) if class_usage else 0
            least_used_classes = [cat for cat in categories if class_usage[cat] == min_usage]
            category = random.choice(least_used_classes)

            chosen_categories.append(category)
            class_usage[category] += 1

            folder_path = os.path.join(augmented_folder, category)
            images = os.listdir(folder_path)
            image_name = random.choice(images)
            image_path = os.path.join(folder_path, image_name)
            image = Image.open(image_path)
            image = image.resize(image_size)

            width, height = image_size
            file.write(f"{categories.index(category)} {(x+width/2)/background_size[0]} {(y+height/2)/background_size[1]} {width/background_size[0]} {height/background_size[1]}\n")
            background.paste(image, (x, y))

            # Write the distribution of the categories to a file
            # with open(f"{output_folder}/category_distribution.txt", "w") as dist_file:
            #     for cat, count in class_usage.items():
            #         dist_file.write(f"{cat}: {count}\n")

    # Save it to the output folder
    background.save(f"{output_folder}/images/image{image_num}.png")

    return chosen_categories

def validate_output():
    number_of_images = len(os.listdir("output/images"))
    number_of_labels = len(os.listdir("output/labels"))

    assert number_of_images == number_of_labels, f"Number of images and labels do not match: {number_of_images} images, {number_of_labels} labels"

    # Draw a bounding box on the image for each label
    for i in range(number_of_images):
        image_path = f"output/images/image{i}.png"
        label_path = f"output/labels/image{i}.txt"
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)

        with open(label_path, "r") as file:
            for line in file:
                category, x, y, w, h = line.split(",")
                x, y, w, h = float(x), float(y), float(w), float(h)
                x1, y1 = x - w/2, y - h/2
                x2, y2 = x + w/2, y + h/2

                x1, y1, x2, y2 = x1*background_size[0], y1*background_size[1], x2*background_size[0], y2*background_size[1]

                draw.rectangle([x1, y1, x2, y2], outline="red")

                # Add the respective category name under the bounding box
                category = int(category)
                with open("class_names.txt", "r") as class_file:
                    categories = class_file.read().split("\n")
                    category_name = categories[category]

                draw.text((x1, y2), category_name, fill="red")

        # image.show()

if __name__ == "__main__":
    
    categories = []
    with open("class_names.txt", "r") as file:
        categories = file.read().split("\n")
    assert len(categories) != 0, "No categories found in class_names.txt"
    categories = categories[:5]

    number_of_images_train = 1
    number_of_images_val = int(0.2 * number_of_images_train)

    for i in range(number_of_images_train):
        create_image(i, "output/train")
    
    for i in range(number_of_images_val):
        create_image(i, "output/val")
    
