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
