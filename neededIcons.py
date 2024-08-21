import os

base_path = "./icons/Architecture-Service-Icons_06072024"
size = "64"

important_paths = [
    "Arch_Compute",
    "Arch_Database",
    "Arch_Containers",
    "Arch_Storage"
]

# Write the class names in the important paths to class_names.txt
with open("class_names_imp.txt", "w") as class_file:
    for path in important_paths:
        class_names = os.listdir(os.path.join(base_path, path, size))
        for class_name in class_names:

            # Write only class names that are PNG images and do not contain "@5x"
            if class_name.endswith(".png") and "@5x" not in class_name:
                class_file.write(f"{class_name[:-4]}\n")