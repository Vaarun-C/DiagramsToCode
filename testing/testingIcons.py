import requests
import os
import json

# Specify the endpoint URL
ENDPOINT_URL = "http://0.0.0.0:8000/getawsicons"

# Specify the directory containing images
IMAGE_DIR = "/Users/varunchandrashekar/base/Projects/DiagramsToCode/testing/aws_diagrams"

# Specify the output file for responses
OUTPUT_FILE = "responses.json"

# Initialize a dictionary to store responses
responses = {}

# Sequentially process images in the directory
image_files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
for index, image_file in enumerate(image_files[:100]):  # Limit to 100 images
    image_path = os.path.join(IMAGE_DIR, image_file)
    try:
        with open(image_path, 'rb') as img:
            # Create form-data payload with MIME type
            files = {'architectureDiagram': (image_file, img, 'image/png')}
            print(f"Sending {image_file} ({index + 1}/100)")

            # Make the POST request
            response = requests.post(ENDPOINT_URL, files=files)
            

            # Check for successful response
            if response.status_code == 200:
                responses[image_file] = [det['classType'] for det in response.json()['detections']]
                print(f"Response for {image_file}: {responses[image_file]}")
            else:
                print(f"Failed to upload {image_file}: {response.status_code} - {response.text}")
                responses[image_file] = {"error": response.text, "status_code": response.status_code}

    except Exception as e:
        print(f"Error processing {image_file}: {e}")
        responses[image_file] = {"error": str(e)}

# Save the responses to a JSON file
with open(OUTPUT_FILE, 'w') as outfile:
    json.dump(responses, outfile, indent=4)

print(f"Responses saved to {OUTPUT_FILE}")
