import cv2
import numpy as np

# Step 1: Load the image (assuming it's already black and white)
image = cv2.imread("test1.png", cv2.IMREAD_GRAYSCALE)

# Step 2: Convert the image to binary (white background, black lines)
_, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
cv2.imshow('binary_image', binary_image)

# Step 3: Find connected components
num_labels, labels = cv2.connectedComponents(binary_image)

# Step 4: Generate random colors for each label
# Create a color image to show the labeled components
output_image = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGR)

# Generate random colors for each label (excluding label 0, which is the background)
colors = np.random.randint(0, 256, size=(num_labels, 3), dtype=np.uint8)

# Step 5: Color each component with a random color
for i in range(1, num_labels):  # Start from 1 to skip the background (label 0)
    output_image[labels == i] = colors[i]

# Step 6: Display the result
cv2.imshow('Segmented Image', output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
