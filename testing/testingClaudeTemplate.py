import os
import anthropic
import json

prompt = '''
Can you generate a comprehensive AWS Cloudformation Template. Don't skip any services. Make sure the Template follows a cohesive structure like this:

AWSTemplateFormatVersion: ...
Description: ...

Parameters:
...
Conditions:
...
Resources:
...
Outputs:
...
'''

claude_responses = {}
client = anthropic.Anthropic(
    api_key="my_api_key",
)

recognised_services = {}

with open('claude_responses.json', 'r') as file:
    recognised_services = json.loads(file.read())
 
for i, image_name, services in enumerate(recognised_services.values()):
    
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
                    }
                ]
            }
        ]
    )
    
    claude_responses[image_name] = message.content
    print(f"Running for image {i}: {image_name}")

    # Write responses to file
    with open("claude_responses_template.json", "w") as file:  # Changed 'r' to 'w' mode
        json.dump(claude_responses, indent=4, fp=file)  # Using json.dump instead of dumps