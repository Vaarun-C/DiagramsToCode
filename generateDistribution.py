import os
import matplotlib.pyplot as plt

# Configuration
output_folder = "output/train"  # Folder where images and labels are stored
label_folder = os.path.join(output_folder, "labels")  # Folder containing the label files
image_size = (1000, 1000)  # Size of the background image
point_size = 10  # Adjust this value to change the size of the points

# Load the categories
with open("class_names_imp.txt", "r") as file:
    categories = file.read().splitlines()

# List of important classes
important_classes = categories  # Replace with your important class names

# Initialize a dictionary to store positions for each important class
class_positions = {class_name: [] for class_name in important_classes}

# Parse the label files
for label_file in os.listdir(label_folder):
    with open(os.path.join(label_folder, label_file), "r") as file:
        for line in file:
            category_idx, x_center, y_center, width, height = map(float, line.split())
            category = categories[int(category_idx)]
            
            x_center *= image_size[0]
            y_center *= image_size[1]
            class_positions[category].append((x_center, y_center))

# Create subplots
num_classes = len(important_classes)
fig, axes = plt.subplots(num_classes, 1, figsize=(10, 4 * num_classes))

# Plotting each class
for i, class_name in enumerate(important_classes):
    ax = axes[i]
    if class_positions[class_name]:
        x, y = zip(*class_positions[class_name])
        ax.scatter(x, y, color='blue', label=f"Class: {class_name}", alpha=0.6, s=point_size)
    ax.set_title(f"Distribution of {class_name}")
    ax.set_xlabel("X Position")
    ax.set_ylabel("Y Position")
    ax.legend(loc="upper right")
    ax.grid(True)

# Adjust layout and show the plot
plt.tight_layout()
plt.savefig("category_distribution.png")
