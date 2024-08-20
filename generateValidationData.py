# Choose service icons randomly from the dataset and generate validation data

import os
import random
import shutil

def generate_validation_data(base_path, output_base_path, num_images):
    """
    Generate validation data by choosing random images from the given base path and saving them to the output base path.

    Args:
        base_path (str): The base path of the images.
        output_base_path (str): The base path where the validation images will be saved.
        num_images (int): The number of images to generate.

    Returns:
        None
    """
    for folder_name in os.listdir(base_path):
        if folder_name == ".DS_Store":
            continue

        folder_path = os.path.join(base_path, folder_name)
        output_folder_path = os.path.join(output_base_path, folder_name)

        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)

        for i in range(num_images):
            image_name = random.choice(os.listdir(folder_path))
            image_path = os.path.join(folder_path, image_name)
            output_image_path = os.path.join(output_folder_path, f"{i}.png")
            shutil.move(image_path, output_image_path)

# Generate validation data
base_path = "./augmented"
output_base_path = "./validation"
num_images = 5
generate_validation_data(base_path, output_base_path, num_images)