import matplotlib.pyplot as plt
import numpy as np

# Sample data (replace with actual values)
systems = ['System A', 'System B']
correct_detections = [80, 90]  # Replace with actual correct detections
false_positives = [10, 15]  # Replace with actual false positives
ground_truth = [100, 100]  # Replace with actual ground truth values

# Bar width for visualization
bar_width = 0.25

# X-axis positions
x = np.arange(len(systems))

# Create the bar chart
plt.figure(figsize=(10, 6), facecolor='#2D2B3C')

plt.bar(x - bar_width, correct_detections, width=bar_width, label='Correct Detections', color='#F28E2C')
plt.bar(x, false_positives, width=bar_width, label='False Positives', color='#E15759')
plt.bar(x + bar_width, ground_truth, width=bar_width, label='Ground Truth', color='#4E79A7')

# Add labels, title, and legend
plt.xlabel('Systems', fontsize=12, color='white')
plt.ylabel('Counts', fontsize=12, color='white')
plt.title('Comparison of Correct Detections and False Positives vs Ground Truth', fontsize=14, color='white')
plt.xticks(x, systems, fontsize=12, color='white')
plt.yticks(color='white')
plt.legend(fontsize=12, facecolor='#2D2B3C', edgecolor='white', labelcolor='white')

# Show grid for better readability
plt.grid(axis='y', linestyle='--', alpha=0.7, color='gray')

# Show the graph
plt.tight_layout()
plt.show()
