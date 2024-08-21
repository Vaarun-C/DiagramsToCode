import os

def generate_data_yaml(class_names):

    with open(class_names, "r") as file:
        class_names = file.read().split("\n")
        
        number_of_classes = len(class_names)

        data_yaml = f"train: ./dataset/train\nval: ./dataset/val\nnc: {number_of_classes}\nnames: {class_names}"

        with open("data.yaml", "w") as file:
            file.write(data_yaml)

if __name__ == "__main__":
    generate_data_yaml("class_names_imp.txt")