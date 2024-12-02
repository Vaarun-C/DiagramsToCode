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

def drawRects(image, rectangle_outlines):
    # Draw detected rectangle outlines
    output_image = cv2.cvtColor(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
    for i, (x, y, w, h) in enumerate(rectangle_outlines):
        cv2.rectangle(output_image, (x, y), (x + w, y + h), rgb(), 2)
        cv2.imshow("Detected Rectangle Outlines", output_image)
        # print(i)
        # cv2.waitKey(0)
    cv2.imshow("Detected Rectangle Outlines", output_image)
    print(rectangle_outlines)
    cv2.waitKey(0)

def detectRectangles(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    edges = cv2.Canny(thresh, 50, 150) # edge detection

    kernel_hz40 = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    kernel_vt40 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
    kernel_hz20 = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 1))  # define a rectangular structural element (horizontal lines)
    kernel_vt20 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 20))  # define a rectangular structural element (vertical lines)
    kernel_hz7 = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 1))
    kernel_vt7 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 7))
    kernel_hz3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 1))
    kernel_vt3 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 3))
    kernel3 = np.ones((3, 3), np.uint8)
    kernel5 = np.ones((5, 5), np.uint8)
    kernel7 = np.ones((7, 7), np.uint8)
    kernel9 = np.ones((9, 9), np.uint8)

    #* FOR SOLID LINES

    # perform morphological opening
    only_lines_hz = cv2.morphologyEx(edges, cv2.MORPH_OPEN, kernel_hz20)
    only_lines_vt = cv2.morphologyEx(edges, cv2.MORPH_OPEN, kernel_vt20)

    # dilate to elongate the detected lines
    only_lines_hz_extended = cv2.dilate(only_lines_hz, kernel_hz3, iterations=1)
    only_lines_vt_extended = cv2.dilate(only_lines_vt, kernel_vt3, iterations=1)
    output_solid_lines = cv2.bitwise_or(only_lines_hz_extended, only_lines_vt_extended)

    # get all rectangle outlines
    contours, _ = cv2.findContours(output_solid_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rectangle_outlines_solid = []
    for contour in contours:        
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True) # approximate the contour to a polygon
        x, y, w, h = cv2.boundingRect(approx)
        if w>50 and h>50:
            rectangle_outlines_solid.append((x, y, w, h))

    # drawRects(image, rectangle_outlines_solid)



    #* FOR DASHED LINES
    
    # get mask of solid lines
    thickened_lines = cv2.dilate(output_solid_lines, kernel3, iterations=1)
    line_mask = cv2.bitwise_not(thickened_lines)
    masked_img = cv2.bitwise_and(edges, edges, mask=line_mask)

    # get everything but the solid lines
    closed_img_hz = cv2.morphologyEx(masked_img, cv2.MORPH_CLOSE, kernel_hz7)
    closed_img = cv2.morphologyEx(closed_img_hz, cv2.MORPH_CLOSE, kernel_vt7)
    eroded_img = cv2.morphologyEx(closed_img, cv2.MORPH_OPEN, kernel5)
    no_solid_lines = cv2.subtract(closed_img, eroded_img)

    # smooth out the detected dashed lines
    no_solid_lines_dialated = cv2.dilate(no_solid_lines, kernel9, iterations=1)
    no_solid_lines_smoothened = cv2.erode(no_solid_lines_dialated, kernel9, iterations=1)
    
    # perform morphological opening
    only_dashed_lines_hz = cv2.morphologyEx(no_solid_lines_smoothened, cv2.MORPH_OPEN, kernel_hz40)
    only_dashed_lines_vt = cv2.morphologyEx(no_solid_lines_smoothened, cv2.MORPH_OPEN, kernel_vt40)
    only_dashed_lines = cv2.bitwise_or(only_dashed_lines_hz, only_dashed_lines_vt)

    # thin the detected lines
    output_dashed_lines = cv2.morphologyEx(only_dashed_lines, cv2.MORPH_ERODE, kernel3)

    # get all rectangle outlines
    contours, _ = cv2.findContours(output_dashed_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rectangle_outlines_dashed = []
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True) # approximate the contour to a polygon
        x, y, w, h = cv2.boundingRect(approx)
        if w>50 and h>50:
            rectangle_outlines_dashed.append((x, y, w, h))

    # drawRects(image, rectangle_outlines_dashed)

    return rectangle_outlines_solid + rectangle_outlines_dashed




#? how to run
# image = cv2.imread('groups/test1.png', cv2.IMREAD_COLOR)
# detectRectangles(image)