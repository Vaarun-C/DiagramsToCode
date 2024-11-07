from fastapi import FastAPI, Form
from pydantic import BaseModel
from typing import List

app = FastAPI()

class ClassList(BaseModel):
    items: List[str]

LLM_SUGGESTIONS = {
    'AWS::ECS::Cluster': [
        'AWS::ECS::TaskDefinition',
        'AWS::ECS::Service'
    ],

    'AWS::EC2::VPC': [
        'AWS::EC2::InternetGateway',
        'AWS::EC2::RouteTable',
        'AWS::EC2::Route',
        'AWS::EC2::VPCGatewayAttachment',
        'AWS::EC2::SubnetRouteTableAssociation'
    ],

    'AWS::S3::Bucket': [
        'AWS::S3::BucketPolicy'
    ],

    'AWS::Lambda::Function': [
        'AWS::ApiGateway::RestApi',
        'AWS::ApiGateway::Resource',
        'AWS::ApiGateway::MethodForLambda',
        'AWS::Lambda::Permission'
    ],

    "AWS::EC2::Instance": [
        'AWS::EC2::VPC'
    ]
}

@app.post("/getllmsuggestion")
async def root(items: List[str] = Form(...)):
    print(items)
    new_types = []
    for class_type in items:
        new_types.extend(LLM_SUGGESTIONS.get(class_type, []))

    return {"message": new_types}