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

def run1(xx=20):
    # Load the image
    image = cv2.imread('test1.png', cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, 11, 2)

    # Apply edge detection
    edges = cv2.Canny(thresh, 50, 150)

    # Define a rectangular structural element (horizontal lines)
    kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (xx, 1))  # Change (50, 1) for vertical or diagonal
    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, xx))  # Change (50, 1) for vertical or diagonal

    # Perform morphological opening
    opened1 = cv2.morphologyEx(edges, cv2.MORPH_OPEN, kernel1)
    cv2.imshow('opened1', opened1)
    opened2 = cv2.morphologyEx(edges, cv2.MORPH_OPEN, kernel2)
    cv2.imshow('opened2', opened2)
    cv2.waitKey(0)
    quit()

    # Optionally, dilate to thicken the detected lines
    k1 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 1))
    k2 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 3))
    dilated1 = cv2.dilate(opened1, k1, iterations=1)
    dilated2 = cv2.dilate(opened2, k2, iterations=1)
    dilated = cv2.bitwise_or(dilated1, dilated2)

    # dialated_dialated = cv2.dilate(dilated, np.ones((3, 3), np.uint8))
    # dilated = dialated_dialated

    # Overlay detected lines on the original image
    line_overlay = cv2.cvtColor(dilated, cv2.COLOR_GRAY2BGR)
    # cv2.imshow('Detected Straight line_overlay', line_overlay)
    output = cv2.addWeighted(image, 0.0, line_overlay, 1, 0)

    # Show the results
    # cv2.imshow('Detected Straight Lines'+str(xx), output)
    # cv2.imwrite("C:/Users/vpaul/Downloads/test1line.png",output)

    # lines = cv2.HoughLinesP(dilated, 1, np.pi / 180, threshold=100, minLineLength=30, maxLineGap=3)
    # if lines is not None:
    #     for line in lines:
    #         x1, y1, x2, y2 = line[0]
    #         cv2.line(output, (x1, y1), (x2, y2), rgb(), 2)
    #         cv2.imshow('Detected Lines', output)

    new_edges = cv2.Canny(~dilated,150,50)
    new_edges = dilated
    # cv2.imshow('new_edges', new_edges)

    contours, _ = cv2.findContours(new_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rectangle_outlines = []
    for contour in contours:
        # Approximate the contour to a polygon
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        
        # Check if the polygon has 4 vertices
        if True or len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            if w>50 and h>50:
                rectangle_outlines.append((x, y, w, h))

    # Draw detected rectangle outlines
    output_image = cv2.cvtColor(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
    for i, (x, y, w, h) in enumerate(rectangle_outlines):
        cv2.rectangle(output_image, (x, y), (x + w, y + h), rgb(), 2)
        cv2.imshow("Detected Rectangle Outlines", output_image)
        # cv2.waitKey(0)
        print(i)
    cv2.imshow("Detected Rectangle Outlines", output_image)
    print(rectangle_outlines)
    # cv2.waitKey(0)
    # quit()




    
    thickened_lines = cv2.dilate(dilated, np.ones((3, 3), np.uint8), iterations=1)
    line_mask = cv2.bitwise_not(thickened_lines)
    masked_img = cv2.bitwise_and(edges, edges, mask=line_mask)
    # cv2.imshow('masked_img', masked_img)

    kernel11 = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 1))
    kernel22 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 7))
    close1 = cv2.morphologyEx(masked_img, cv2.MORPH_CLOSE, kernel11)
    # cv2.imshow('close1', close1)
    close2 = cv2.morphologyEx(close1, cv2.MORPH_CLOSE, kernel22)
    # cv2.imshow('close2', close2)

    erodeed_img = cv2.morphologyEx(close2, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    # cv2.imshow('erodeed_img', erodeed_img)

    only_lines = cv2.subtract(close2, erodeed_img)
    # only_lines = cv2.morphologyEx(only_li jnes, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    only_lines = cv2.dilate(only_lines, np.ones((9, 9), np.uint8), iterations=1)
    only_lines = cv2.erode(only_lines, np.ones((9, 9), np.uint8), iterations=1)
    cv2.imshow('only_lines', only_lines)
    # cv2.imwrite("C:/Users/vpaul/Downloads/only_lines.png",only_lines)

    kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
    opened11 = cv2.morphologyEx(only_lines, cv2.MORPH_OPEN, kernel1)
    opened22 = cv2.morphologyEx(only_lines, cv2.MORPH_OPEN, kernel2)
    output_img = cv2.bitwise_or(opened11, opened22)
    output_img = cv2.morphologyEx(output_img, cv2.MORPH_ERODE, np.ones((3, 3), np.uint8))

    cv2.imshow('output_img', output_img)

    # lines = cv2.HoughLinesP(output_img, 1, np.pi / 180, threshold=40, minLineLength=30, maxLineGap=3)
    # if lines is not None:
    #     for line in lines:
    #         x1, y1, x2, y2 = line[0]
    #         cv2.line(output, (x1, y1), (x2, y2), rgb(), 2)
    #         cv2.imshow('Detected Lines', output)

    contours, _ = cv2.findContours(output_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rectangle_outlines = []
    for contour in contours:
        # Approximate the contour to a polygon
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        
        # Check if the polygon has 4 vertices
        if True or len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            if w>50 and h>50:
                rectangle_outlines.append((x, y, w, h))

    # Draw detected rectangle outlines
    output_image = cv2.cvtColor(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
    for i, (x, y, w, h) in enumerate(rectangle_outlines):
        cv2.rectangle(output_image, (x, y), (x + w, y + h), rgb(), 2)
        cv2.imshow("Detected Rectangle Outlines", output_image)
        # cv2.waitKey(0)
        print(i)
    cv2.imshow("Detected Rectangle Outlines", output_image)
    print(rectangle_outlines)




    
run1()
cv2.waitKey(0)
cv2.destroyAllWindows()
