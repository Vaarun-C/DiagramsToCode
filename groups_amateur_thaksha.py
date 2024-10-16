import cv2
import numpy as np
import pytesseract

def hsl_to_rgb(h):
    x = (1 - abs((h / 60) % 2 - 1))
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
    return (round(r_ * 255), round(g_ * 255), round(b_ * 255))

def draw_all_lines(image_path):
    # Read the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, 11, 2)

    # Use Canny edge detection
    edges = cv2.Canny(thresh, 50, 150)

    # Show the edges detected
    cv2.imshow('Edges', edges)
    cv2.waitKey(0)

    # Use Hough Transform to detect lines
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=50, maxLineGap=10)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(image, (x1, y1), (x2, y2), hsl_to_rgb(np.random.randint(0, 360)), 2)

    # Show the image with detected lines
    cv2.imshow('Detected Lines', image)
    cv2.waitKey(0)

    return lines

def is_rectangle(p1, p2, p3, p4, distance_threshold=10):
    return (abs(p1[0] - p3[0]) <= distance_threshold and abs(p2[0] - p4[0]) <= distance_threshold and
            abs(p1[1] - p2[1]) <= distance_threshold and abs(p3[1] - p4[1]) <= distance_threshold) or \
           (abs(p1[1] - p3[1]) <= distance_threshold and abs(p2[1] - p4[1]) <= distance_threshold and
            abs(p1[0] - p2[0]) <= distance_threshold and abs(p3[0] - p4[0]) <= distance_threshold)

def find_rectangles_from_lines(lines):
    if lines is None:
        return []

    rectangles = []
    points = []

    # Extract endpoints from detected lines
    for line in lines:
        for x1, y1, x2, y2 in line:
            points.append((x1, y1))
            points.append((x2, y2))

    points = list(set(points))  # Remove duplicate points

    # Check combinations of points to form rectangles
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            p1 = points[i]
            p2 = points[j]

            for k in range(len(points)):
                for l in range(k + 1, len(points)):
                    p3 = points[k]
                    p4 = points[l]

                    if is_rectangle(p1, p2, p3, p4):
                        # Calculate area of the rectangle
                        rect_width = max(p1[0], p3[0]) - min(p1[0], p3[0])
                        rect_height = max(p1[1], p2[1]) - min(p1[1], p2[1])
                        rect_area = rect_width * rect_height

                        # Check if area is greater than the minimum threshold
                        if rect_area >= 64 * 64:
                            rectangles.append((p1, p2, p3, p4))
                        # elif 

    return rectangles

def draw_rectangles(image, rectangles):
    for rect in rectangles:
        cv2.polylines(image, [np.array(rect)], isClosed=True, color=(0, 255, 0), thickness=2)

def detect_rectangles(image_path):
    lines = draw_all_lines(image_path)

    # Now find rectangles based on detected lines
    rectangles = find_rectangles_from_lines(lines)

    # Read the image again to draw rectangles
    image = cv2.imread(image_path)
    draw_rectangles(image, rectangles)

    # Display the final image with rectangles
    cv2.imshow('Detected Rectangles', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print(f"Detected {len(rectangles)} rectangles.")

# Example usage
image_path = r"" # Change this to your image path
detect_rectangles(image_path)
