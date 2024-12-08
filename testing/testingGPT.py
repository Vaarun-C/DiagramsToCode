import json
import os
import colorama

# Directory containing the files
directory = "./GPTObj"

# Iterate through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".json"):
        filepath = os.path.join(directory, filename)

        try:
            with open(filepath, "r") as file:
                data = json.load(file)
            
            # Extract the "template" key
            if "template" in data:
                template_data = data["template"]
                
                # Overwrite the file with only the "template" content
                with open(filepath, "w") as file:
                    json.dump(template_data, file, indent=4)
                print(f"Updated file: {filename}")
            else:
                print(f"No 'template' key found in: {filename}")
        except json.decoder.JSONDecodeError:
            print(f"{colorama.Fore.RED}Failed for file {filename}{colorama.Fore.RESET}")
        except TypeError:
            print(f"{colorama.Fore.RED}Failed for file {filename}{colorama.Fore.RESET}")
