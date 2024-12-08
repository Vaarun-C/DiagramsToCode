import os
import anthropic
import json
import base64

prompt = '''
Can you recognize the various service icons in this AWS architecture diagram. Don't skip any icons and give me a list instead of a set. Give it to me in this format. For example:
[
    "AWS::Lambda::Function",
    "AWS::Lambda::Function",
    "AWS::StepFunctions::StateMachine",
    "AWS::DynamoDB::Table",
    "AWS::Events::EventBus",
    "AWS::ApiGateway::RestApi",
    "AWS::KMS::Key"
]
'''

def encode_image(image_path):
    """Encode image to base64 string"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

claude_responses = {}
client = anthropic.Anthropic(
    api_key="my_api_key",
)

image_dir = "/Users/varunchandrashekar/base/Projects/DiagramsToCode/testing/aws_diagrams"

for i, image_name in enumerate(os.listdir(image_dir)):
    image_path = os.path.join(image_dir, image_name)
    
    # Skip if not an image file
    if not image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue
    
    # Encode image to base64
    base64_image = encode_image(image_path)
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2000,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",  # Change to appropriate type if needed
                            "data": base64_image
                        }
                    }
                ]
            }
        ]
    )
    
    claude_responses[image_name] = message.content
    print(f"Running for image {i}: {image_name}")

    # Write responses to file
    with open("claude_responses.json", "w") as file:  # Changed 'r' to 'w' mode
        json.dump(claude_responses, indent=4, fp=file)  # Using json.dump instead of dumps