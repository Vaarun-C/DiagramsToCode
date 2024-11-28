from pymongo import MongoClient
from pymongo.server_api import ServerApi
import sys
import json

URI = "mongodb+srv://CapTheStone:VarunVikas@viewme.vzrbu.mongodb.net/?retryWrites=true&w=majority&appName=viewme&tlsAllowInvalidCertificates=true"

# Connect to MongoDB
try:
    client = MongoClient(URI, server_api=ServerApi('1'))
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    print("CONNECTION ERROR!!")
    quit()

db = client['Templates']
icons_collection = db['Templates[PROD]_cleaned']

record_template = {
    "Parameters": "",
    "Resources": "",
    "Type": "",
    "Dependencies": [],
    "Outputs": "",
    "Conditions": "",
    "Disclaimers": ""
}

"""
App Integration
- EventBridge
- Managed Workflows for Apache Airflow
- Amazon MQ
- SNS
- SQS
- AppSync
- Step Functions

AI
- Bedrock
- Comprehend
- Kendra
- Lex
- Polly
- Amazon Q
- Sagemaker
- Textract
- transcribe

Compute
- EC2
- Batch
- Elastic Beanstalk
- Outposts

Containers
- ECS
- EKS
- Fargate

Database
- Aurora
- RDS
- DynamoDB
- Elastic cache
- DMS

Arch_Management-Governance
- Cloudwatch
- Managed Grafana
- Managed service for proetheous
- auto scaling
- Cloudformation
- Cloudtrail
- COntrol Tower

Networking
- API gateway
- CLoudfront
- Route 53
- VPC
- VPC Lattice
- Direcft COnnect
- Private Link
- Site to Site VPN
- Transit gateway
- Elastic Load Balancing

Security
- Cognito
- Guard Duty
- Cloud HSM
- IAM Identity Center
- KMS
- Network Firewall
- Secrete manager
- WAF

Storage
- EFS
- EBS
- FSx
- S3
- Backup
"""

record_folder = "./testingMongo"
record = f"{sys.argv[1]}.yaml"
record_path = record_folder + "/" + record
record_template["Type"] = sys.argv[1]

with open(record_path) as file:
    lines = file.readlines()
    current_section = None  # Track the current section being processed

    for line in lines:
        # Check for section headers
        if line.strip().startswith("Parameters:"):
            current_section = "Parameters"
            continue
        elif line.strip().startswith("Resources:"):
            current_section = "Resources"
            continue
        elif line.strip().startswith("Outputs:"):
            current_section = "Outputs"
            continue
        elif line.strip().startswith("Dependencies:"):
            current_section = "Dependencies"
            continue
        elif line.strip().startswith("Conditions:"):
            current_section = "Conditions"
            continue
        elif line.strip().startswith("Disclaimers:"):
            current_section = "Disclaimers"
            continue
        elif line.strip() == "":
            # Skip empty lines
            continue

        # Append line to the appropriate section
        if current_section == "Parameters":
            record_template["Parameters"] += line
        elif current_section == "Resources":
            record_template["Resources"] += line
        elif current_section == "Conditions":
            record_template["Conditions"] += line
        elif current_section == "Outputs":
            record_template["Outputs"] += line
        elif current_section == "Dependencies":
            record_template["Dependencies"] = json.loads(line)
        elif current_section == "Disclaimers":
            record_template["Disclaimers"] = json.loads(line)

# Print or use the extracted sections
icons_collection.insert_one(record_template)
print(record_template)
print("Inserted Record")