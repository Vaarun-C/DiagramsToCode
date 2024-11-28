def rgb():
    from random import randint
    h = randint(0,360)
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

import cv2
import numpy as np

def detect_rectangle_outlines(image_path):
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Image at {image_path} could not be loaded.")
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply binary inversion thresholding
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, 11, 2)

    # Detect edges using Canny
    edges = cv2.Canny(binary, 50, 150)
    # cv2.imshow('edges', edges)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # List to store bounding boxes of rectangle outlines
    rectangle_outlines = []

    # Process each contour
    for contour in contours:
        # Approximate the contour to a polygon
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        
        # Check if the polygon has 4 vertices
        if len(approx) == 4:
            # Get bounding box of the contour
            x, y, w, h = cv2.boundingRect(approx)

            # Ensure the aspect ratio and size are reasonable (to eliminate noise)
            # aspect_ratio = float(w) / h
            # if 0.5 < aspect_ratio < 2.0 and w > 10 and h > 10:  # Adjust thresholds if needed
            if w>20 and h>20:
                rectangle_outlines.append((x, y, w, h))

    # Draw detected rectangle outlines
    output_image = cv2.cvtColor(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
    for i, (x, y, w, h) in enumerate(rectangle_outlines):
        cv2.rectangle(output_image, (x, y), (x + w, y + h), rgb(), 2)
        cv2.imshow("Detected Rectangle Outlines", output_image)
        cv2.waitKey(0)
        print(i)

    # Show intermediate steps and results
    cv2.imshow("Original Image", image)
    cv2.imshow("Binary Image", binary)
    cv2.imshow("Edge Detection", edges)
    cv2.imshow("Detected Rectangle Outlines", output_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return rectangle_outlines

# Run the function with your image
detected_rectangles = detect_rectangle_outlines('test1.png')
print("Detected rectangle outlines (x, y, w, h):", detected_rectangles)
