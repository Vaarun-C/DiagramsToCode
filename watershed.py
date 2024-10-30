import cv2
import numpy as np, random
from matplotlib import pyplot as plt

def watershed_segmentation(image_path):
    # Step 1: Read the input image
    image = cv2.imread(image_path)
    
    # Step 2: Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Step 3: Apply a threshold to create a binary image
    # Use Otsu's thresholding to automatically determine a good threshold
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imshow("img binary", binary)
    # cv2.waitKey(0)

    # Step 4: Remove small noise with morphological operations (opening)
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)
    cv2.imshow("opening", opening)

    # Step 5: Dilate to ensure the foreground is clearly separated from the background
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    opening = binary
    sure_bg = ~binary##############################
    cv2.imshow("sure_bg", sure_bg)

    # Step 6: Apply distance transform to find the areas that are sure to be foreground (markers)
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    
    # Step 7: Threshold the distance transform to get sure foreground (regions far away from the boundary)
    _, sure_fg = cv2.threshold(dist_transform, 0.05 * dist_transform.max(), 255, 0)
    cv2.imshow("sure_fg", sure_fg)
    
    # Step 8: Subtract the sure foreground from the sure background to get the unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    
    # Step 9: Label the markers
    num_labels, markers = cv2.connectedComponents(sure_fg)
    connected_components_display = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
    for label in range(1, num_labels):  # Skip background label 0
        random_color = [random.randint(0, 255) for _ in range(3)]
        connected_components_display[markers == label] = random_color
    cv2.imshow('Connected Components', connected_components_display)
    
    
    
    # Step 10: Add one to all labels so that the background is not 0 but 1
    markers = markers + 1
    
    # Step 11: Mark the unknown region with 0 (so it can be later identified as the watershed boundary)
    markers[unknown == 255] = 0

    markers_display = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
    markers_display = np.uint8(markers * (255 / (markers.max() + 1)))  # Scale for better visualization
    cv2.imshow('Markers Before Watershed', markers_display)

    
    
    # Step 12: Apply the Watershed algorithm
    markers = cv2.watershed(image, markers)
    
    colored_output = np.zeros_like(image)
    unique_markers = np.unique(markers)    
    for marker in unique_markers:
        if marker == -1:  # Watershed boundary
            colored_output[markers == marker] = [0, 0, 255]  # Red for boundary
        elif marker == 1:  # Background
            continue  # Skip background
        else:
            # Generate a random color for each segment
            random_color = [random.randint(0, 255) for _ in range(3)]
            colored_output[markers == marker] = random_color


    # Step 13: Mark the watershed boundaries in red
    image[markers == -1] = [0, 0, 255]  # Watershed boundaries will appear in red
    image[markers != -1] = [100,0,100]
    
    # Step 14: Display and save the final image
    cv2.imshow('Watershed Segmentation', colored_output)
    # cv2.imwrite('watershed_result.jpg', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage:
input_image_path = './test1.png'  # Replace with your input image
watershed_segmentation(input_image_path)
