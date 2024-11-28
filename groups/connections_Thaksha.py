import cv2
import numpy as np
import matplotlib.pyplot as plt

def load_image(image_path):
    # Loading the image
    image = cv2.imread(image_path)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def preprocess_image(image):
    # Convert to grayscale and edge detection
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, threshold1=50, threshold2=150)
    return edges

def find_arrows(edges):
    """Find lines and detect arrows using Hough Transform."""
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=30, maxLineGap=10)
    
    arrows = []
    
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # Check for arrowheads (simple method)
            dx, dy = x2 - x1, y2 - y1
            angle = np.arctan2(dy, dx) * 180 / np.pi
            if angle < 0:
                angle += 360
            # Store lines with their direction
            arrows.append((x1, y1, x2, y2, angle))
    
    return arrows

def draw_arrows(image, arrows):
    # Draw the identified arrows on the original image for visualization
    for x1, y1, x2, y2, angle in arrows:
        cv2.arrowedLine(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return image

def main(image_path):
    image = load_image(image_path)
    edges = preprocess_image(image)
    arrows = find_arrows(edges)
    
    # Draw arrows for visualization
    output_image = draw_arrows(image.copy(), arrows)

    # Display results
    plt.figure(figsize=(10, 6))
    plt.subplot(1, 2, 1)
    plt.title('Original Image with Arrows')
    plt.imshow(output_image)
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.title('Edge Detection')
    plt.imshow(edges, cmap='gray')
    plt.axis('off')

    plt.show()

    # Print detected arrows for further processing
    for arrow in arrows:
        print(f"Arrow from ({arrow[0]}, {arrow[1]}) to ({arrow[2]}, {arrow[3]}) at angle {arrow[4]:.2f}")

if __name__ == "__main__":
    # Replace 'path_to_your_image.png' with the actual path to your PNG image
    main(r"test1.png")
