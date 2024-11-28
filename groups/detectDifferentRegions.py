import cv2
import numpy as np

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


# Load the image
image = cv2.imread('test1.png', cv2.IMREAD_COLOR)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply edge detection
edges = cv2.Canny(gray, 50, 150)

# Morphological operations to enhance line features
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
dilated = cv2.dilate(edges, kernel, iterations=1)

# Find contours
contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

output = image.copy()

# Filter contours for dotted and dashed lines
dashed_dotted_lines = []
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    aspect_ratio = w / h
    # if 0.2 < aspect_ratio < 5:  # Filtering based on aspect ratio
    area = cv2.contourArea(contour)
    if 4096 < area :  # Adjust size thresholds based on image
        dashed_dotted_lines.append(contour)
        cv2.drawContours(output, [contour], -1, rgb(), 2)

# Show the results
cv2.imshow('Detected regions and boundries', output)
cv2.waitKey(0)
cv2.destroyAllWindows()
