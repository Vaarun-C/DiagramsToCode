# # def hsl_to_rgb(h, s, l):
# #     """
# #     Convert HSL color space to RGB color space.

# #     Parameters:
# #     h (float): Hue angle in degrees [0, 360]
# #     s (float): Saturation as a percentage [0, 100]
# #     l (float): Lightness as a percentage [0, 100]

# #     Returns:
# #     tuple: (r, g, b) values in range [0, 255]
# #     """
    
# #     s /= 100
# #     l /= 100

# #     c = (1 - abs(2 * l - 1)) * s  # Chroma
# #     x = c * (1 - abs((h / 60) % 2 - 1))  # Second largest component
# #     m = l - c / 2  # Match lightness
    
# #     if 0 <= h < 60:
# #         r_, g_, b_ = c, x, 0
# #     elif 60 <= h < 120:
# #         r_, g_, b_ = x, c, 0
# #     elif 120 <= h < 180:
# #         r_, g_, b_ = 0, c, x
# #     elif 180 <= h < 240:
# #         r_, g_, b_ = 0, x, c
# #     elif 240 <= h < 300:
# #         r_, g_, b_ = x, 0, c
# #     else:
# #         r_, g_, b_ = c, 0, x

# #     # Convert to RGB and scale to [0, 255]
# #     r = round((r_ + m) * 255)
# #     g = round((g_ + m) * 255)
# #     b = round((b_ + m) * 255)

# #     return (r, g, b)

# # # Example usage:
# # h = 200  # Hue (degrees)
# # s = 50   # Saturation (percentage)
# # l = 50   # Lightness (percentage)

# # rgb = hsl_to_rgb(h, s, l)
# # print(f"RGB: {rgb}")




# import cv2
# import numpy as np

# def apply_canny_edge_detection(image_path, save_path):
#     # Read the input image
#     image = cv2.imread(image_path)
    
#     # Convert to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
#     # Apply Canny edge detection
#     edges = cv2.Canny(gray, 100, 200)

#     cv2.imc
    
#     # Save the result to the specified path
#     cv2.imwrite(save_path, edges)
    
#     # Optionally, display the result
#     cv2.imshow('Canny Edge Detection', edges)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

# # Example usage:
# input_image_path = './test1.png'
# output_image_path = './test1_edges.png'
# # apply_canny_edge_detection(input_image_path, output_image_path)

# # print(f"Edges detected and saved to {output_image_path}")



# def apply_canny_with_closing(image_path, save_path):
#     # Read the input image
#     image = cv2.imread(image_path)
    
#     # Convert to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
#     # Apply Canny edge detection
#     edges = cv2.Canny(gray, 100, 200)
    
#     # Define a kernel (structuring element) for morphological operations
#     kernel = np.ones((5, 5), np.uint8)  # You can adjust the kernel size based on your needs
    
#     # Apply morphological closing (dilation followed by erosion)
#     closed_edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    
#     # Save the result to the specified path
#     cv2.imwrite(save_path, closed_edges)
    
#     # Optionally, display the original edges and closed edges
#     cv2.imshow('Original Edges', edges)
#     cv2.imshow('Closed Edges', closed_edges)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

# apply_canny_with_closing(input_image_path, output_image_path)

# print(f"Closed edges image saved to {output_image_path}")



import cv2
import numpy as np

def detect_rectangles(image_path, save_path):
    # Read the input image
    image = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Canny edge detection
    edges = cv2.Canny(gray, 100, 200)
    
    # Define a kernel (structuring element) for morphological operations
    kernel = np.ones((5, 5), np.uint8)  # You can adjust the kernel size based on your needs
    
    # Apply morphological closing (dilation followed by erosion)
    closed_edges = edges#cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    
    # Apply Hough Line Transform to detect lines
    lines = cv2.HoughLinesP(closed_edges, 1, np.pi / 180, threshold=100, minLineLength=50, maxLineGap=10)
    # cv2.Hough
    
    # Create a copy of the original image to draw on
    image_copy = np.copy(image)
    
    # Draw the lines detected by Hough Line Transform
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(image_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw green lines
    
    # Find contours in the edge-detected image
    contours, _ = cv2.findContours(closed_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Loop through each contour and approximate it
    for contour in contours:
        # Approximate the contour to a polygon
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # If the approximated contour has 4 vertices, we consider it as a rectangle
        if len(approx) == 4:
            # Draw the approximated rectangle on the image (in red)
            cv2.drawContours(image_copy, [approx], 0, (0, 0, 255), 3)
    
    # Save the final image with rectangles detected
    # cv2.imwrite(save_path, image_copy)
    
    # Display the image with rectangles
    cv2.imshow('Detected Rectangles', image_copy)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage:
input_image_path = './test1.png'
output_image_path = 'detected_rectangles.jpg'
detect_rectangles(input_image_path, output_image_path)

print(f"Rectangles detected and saved to {output_image_path}")
