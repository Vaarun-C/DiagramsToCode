# Read the contents of the two text files
with open('larger.txt', 'r') as file:
    larger_list = file.readlines()

with open('services_66.txt', 'r') as file:
    smaller_list = set(file.read().splitlines())  # Using a set for faster lookup

# Process the larger list
modified_list = []
for name in larger_list:
    name = name.strip()  # Remove any extra whitespace or newline characters
    if name in smaller_list:
        modified_list.append(f"// {name}")
    else:
        modified_list.append(name)

# Write the modified list back to a file
with open('modified_larger.txt', 'w') as file:
    file.write("\n".join(modified_list))

print("Modification complete. Check 'modified_larger.txt' for the results.")
