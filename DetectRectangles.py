import cv2
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




image = cv2.imread('test1.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blurred, 50, 150)
contours, _ = cv2.findContours(edges, cv2.RETR_LIST , cv2.CHAIN_APPROX_SIMPLE)
contours, _ = cv2.findContours(edges, cv2.RETR_TREE  , cv2.CHAIN_APPROX_SIMPLE)
for contour in contours:
    # Approximate the contour to a polygon
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)

    # If the approximated polygon has 4 points, it's a rectangle
    if len(approx) == 4:
        # Optionally draw the contour/rectangle for visualization
        cv2.drawContours(image, [approx], -1, hsl_to_rgb(random.randint(0,360)), 3)
        print(approx)
        # cv2.imshow('Detected Rectangles in the making', image)
        # cv2.waitKey(0)
        # input()


"""
[[[649 524]]

 [[651 588]]

 [[701 591]]

 [[648 589]]]
"""
cv2.imshow('Detected Rectangles', image)
cv2.imshow('Detected Rectangles edges', edges)
cv2.imshow('Detected Rectangles blurred', blurred)

cv2.waitKey(0)
cv2.destroyAllWindows()