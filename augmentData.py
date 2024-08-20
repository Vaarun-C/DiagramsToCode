import os
import tensorflow as tf

def augment_image(image):
    """
    Applies random image augmentations to the given image.

    Parameters:
    - image: A tensor representing the input image.

    Returns:
    - The augmented image tensor.
    """
    image = tf.image.random_flip_left_right(image)
    image = tf.image.random_flip_up_down(image)
    image = tf.image.random_brightness(image, max_delta=0.1)
    # image = tf.image.random_contrast(image, lower=0.8, upper=1.2)
    # image = tf.image.random_hue(image, max_delta=0.1)
    image = tf.image.random_saturation(image, lower=0.8, upper=1.2)
    return image

def preprocess_image(image_path):
    """
    Preprocesses an image by reading it from the given file path, decoding it, resizing it to a desired dimension,
    and augmenting it.

    Args:
        image_path (str): The file path of the image.

    Returns:
        tf.Tensor: The preprocessed image tensor.
    """
    image = tf.io.read_file(image_path)
    image = tf.image.decode_image(image, channels=3)
    image = tf.image.resize(image, [128, 128])  # Resize to desired dimensions
    image = augment_image(image)
    return image

def save_image(image, save_path):
    """
    Save the given image to the specified save path.

    Args:
        image: The image to be saved.
        save_path: The path where the image will be saved.

    Returns:
        None
    """
    image = tf.cast(image, tf.uint8)
    image = tf.image.encode_png(image)
    tf.io.write_file(save_path, image)

def process_folders(base_path, output_base_path):
    """
    Process the folders in the given base path and generate augmented images.
    Args:
        base_path (str): The base path of the folders to process.
        output_base_path (str): The base path where the augmented images will be saved.
    Returns:
        None
    """
    for folder_name in os.listdir(base_path):

        if folder_name == ".DS_Store":
            continue

        folder_path = os.path.join(base_path, folder_name)
        augmented_folder_path = os.path.join(output_base_path, folder_name)
        os.makedirs(augmented_folder_path, exist_ok=True)
        
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            
            if os.path.isfile(file_path) and file_name.endswith(".png"):
                image = preprocess_image(file_path)
                
                # Generate unique names for augmented images
                for i in range(20):  # Example: create 5 augmented images per original
                    augmented_image = augment_image(image)
                    augmented_file_name = f"{file_name[:-4]}_augmented_{i}.png"
                    print(f"Saving {augmented_file_name}", end="\r")
                    save_image(augmented_image, os.path.join(augmented_folder_path, augmented_file_name))

base_path = "train"  # Replace with your actual base path
output_base_path = "augmented"  # Directory to store augmented images

process_folders(base_path, output_base_path)
