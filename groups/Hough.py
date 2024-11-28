# import cv2
# import numpy as np

# def detect_squares(image_path):
#     # Read the image
#     image = cv2.imread(image_path)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
#     # Apply edge detection
#     edges = cv2.Canny(gray, 50, 150, apertureSize=3)

#     # Find contours in the edges image
#     contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

#     squares = []
    
#     for contour in contours:
#         # Approximate the contour to reduce the number of points
#         epsilon = 0.02 * cv2.arcLength(contour, True)
#         approx = cv2.approxPolyDP(contour, epsilon, True)

#         # If the contour has 4 vertices, it might be a square
#         if len(approx) == 4:
#             # Check if the contour is convex
#             if cv2.isContourConvex(approx):
#                 # Calculate the area of the contour
#                 area = cv2.contourArea(approx)
#                 # Filter out very small areas to remove noise
#                 if area > 1000:
#                     # Further verification to ensure it's a square (aspect ratio check)
#                     x, y, w, h = cv2.boundingRect(approx)
#                     aspect_ratio = float(w) / h
#                     if 0.9 <= aspect_ratio <= 1.1:
#                         squares.append(approx)
    
#     # Draw squares on the original image
#     cv2.drawContours(image, squares, -1, (0, 255, 0), 3)

#     # Show the result
#     cv2.imshow('Squares Detected', image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

# # Example usage
# image_path = './test1.png'
# detect_squares(image_path)



import cv2
import numpy as np
import matplotlib.pyplot as plt

def hough_transform_visualization(image_path):
    # Read the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply edge detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Perform Hough Line Transform
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

    # Create an empty accumulator for visualization
    height, width = edges.shape
    max_rho = int(np.sqrt(height**2 + width**2))
    accumulator = np.zeros((2 * max_rho, 180), dtype=np.uint64)

    # Fill the accumulator based on detected lines
    if lines is not None:
        for line in lines:
            rho, theta = line[0]
            theta_deg = int(np.rad2deg(theta))
            accumulator[int(rho) + max_rho, theta_deg] += 1

    # Visualize the original image, edges, and the accumulator
    plt.figure(figsize=(12, 12))

    plt.subplot(2, 2, 1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title('Original Image')

    plt.subplot(2, 2, 2)
    plt.imshow(edges, cmap='gray')
    plt.title('Edges')

    plt.subplot(2, 2, 3)
    plt.imshow(accumulator, cmap='hot', extent=[0, 180, -max_rho, max_rho])
    plt.title('Hough Accumulator')
    plt.xlabel('Theta (degrees)')
    plt.ylabel('Rho (pixels)')

    plt.colorbar()
    plt.show()

# Example usage
image_path = './test1.png'
hough_transform_visualization(image_path)

import cv2
import numpy as np

def detect_bounding_rectangles(image_path):
    # Read the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply edge detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Define a kernel (structuring element) for morphological operations
    kernel = np.ones((5, 5), np.uint8)  # You can adjust the kernel size based on your needs
    
    # Apply morphological closing (dilation followed by erosion)
    closed_edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    # Find contours
    contours, hierarchy = cv2.findContours(closed_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    filled_rectangles = []
    hollow_rectangles = []

    for i, contour in enumerate(contours):
        # Approximate the contour to a polygon
        epsilon = 0.01 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Check if the approximated polygon has 4 vertices
        if len(approx) == 4:
            # Get the bounding rectangle
            x, y, w, h = cv2.boundingRect(approx)

            # Check if the polygon is convex (likely to be filled)
            if cv2.isContourConvex(approx):
                filled_rectangles.append((x, y, w, h))
            else:
                # Check for hollow shapes (child contours)
                if hierarchy[0][i][3] != -1:  # A contour with a parent is hollow
                    hollow_rectangles.append((x, y, w, h))

    # Draw filled and hollow rectangles in different colors
    for (x, y, w, h) in filled_rectangles:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green for filled rectangles

    for (x, y, w, h) in hollow_rectangles:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Blue for hollow rectangles

    # Show the result
    cv2.imshow('Bounding Rectangles Detected', image)
    cv2.imshow('closed_edges', closed_edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
image_path = './test1.png'
detect_bounding_rectangles(image_path)





import cv2
import numpy as np
import random
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

def draw_all_approximations(image_path):
    # Read the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply edge detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Define a kernel (structuring element) for morphological operations
    kernel = np.ones((5, 5), np.uint8)  # You can adjust the kernel size based on your needs
    
    # Apply morphological closing (dilation followed by erosion)
    closed_edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    # Find contours
    contours, _ = cv2.findContours(closed_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Loop through each contour and approximate it
    for contour in contours:
        # Approximate the contour to a polygon
        epsilon = 0.01 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Draw the approximated polygon on the image
        cv2.drawContours(image, [approx], 0, hsl_to_rgb(random.randint(0,359)), 2)  # Green color for approximations

    # Display the image with approximated contours
    cv2.imshow('Approximated Contours', image)
    cv2.imshow('closed_edges', closed_edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
image_path = './test1.png'
draw_all_approximations(image_path)





