import os

# Print length of the class names
with open("class_names.txt", "r") as file:
    categories = file.read().split("\n")
    print(categories)