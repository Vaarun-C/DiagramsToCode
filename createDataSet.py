import os
import shutil
from collections import Counter

path = "./icons/Architecture-Service-Icons_06072024"
categories = os.listdir(path)
chosen_dimensions = 64
num_classes = 0
class_names = []

for category in categories:

    # Ignore Mac OS files
    if category == ".DS_Store":
        continue

    # Get the names of the PNG images
    icons = os.listdir(f"{path}/{category}/{chosen_dimensions}")
    png_icons = [icon for icon in icons if icon.endswith(".png") and "@5x" not in icon]
    num_classes += len(png_icons)
    class_names.extend(png_icons)

    # Create folders and copy the images
    for class_name in png_icons:
        folder_name = class_name[:-4]
        folder_path = os.path.join("train", folder_name)
        src_image_path = os.path.join(path, category, str(chosen_dimensions), class_name)
        dst_image_path = os.path.join(folder_path, "image.png")
        count = 2
        
        try:
            os.makedirs(folder_path, exist_ok=True)


            # Some services have more than 1 type of image with the same name. For those store all images
            while os.path.exists(dst_image_path):
                dst_image_path = os.path.join(folder_path, f"image{count}.png")
                count += 1
                
            shutil.copy(src_image_path, dst_image_path)
        except Exception as e:
            print(f"Error processing {class_name}: {e}")

print(f"Total number of classes: {num_classes}")

name_counts = Counter(class_names)

# Find duplicates
duplicates = {name: count for name, count in name_counts.items() if count > 1}

if duplicates:
    print("Duplicate class names found:")
    for name, count in duplicates.items():
        print(f"{name}: {count} times")
else:
    print("No duplicate class names found.")

# Print missing folders for debugging
class_folders = os.listdir("./train")
print("Total number of folders:", len(class_folders))
missing_folders = set(class_name[:-4] for class_name in class_names) - set(class_folders)
if missing_folders:
    print(f"Missing folders: {missing_folders}")
