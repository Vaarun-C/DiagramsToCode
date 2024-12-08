from fastapi import FastAPI, Form
from pydantic import BaseModel
from typing import List

app = FastAPI()

class ClassList(BaseModel):
    items: List[str]

SUGGESTIONS = {
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

    'AWS::Glue::Database': [
        'AWS::Glue::Crawler',
        'AWS::Glue::Job'
    ],

    'AWS::Events::EventBus': [
        'AWS::Events::Rule'
    ],

    'AWS::SNS::Topic': [
        'AWS::SNS::Subscription'
    ],

    'AWS::AppSync::GraphQLApi': [
        'AWS::AppSync::GraphQLSchema',
        'AWS::AppSync::ApiKey',
        'AWS::AppSync::GetResolver',
        'AWS::AppSync::PutResolver'
    ],

    'AWS::Kendra::Index': [
        'AWS::Kendra::DataSource'
    ],

    'AWS::Lex::Bot': [
        'AWS::Lex::BotAlias'
    ],

    'AWS::IAM::RoleForTextractExecution': [
        'AWS::SNS::Topic',
        'AWS::SNS::Subscription'
    ],

    'AWS::IAM::RoleForTranscribeExecution': [
        'AWS::SNS::Topic',
        'AWS::SNS::Subscription'
    ],

    'AWS::Batch::ComputeEnvironment': [
        'AWS::Batch::JobQueue', 
        'AWS::Batch::JobDefinition'
    ],

    'AWS::ElasticBeanstalk::Application': [
        'AWS::ElasticBeanstalk::Environment'
    ],
    
    'AWS::EKS::Cluster': [
        'AWS::EKS::Nodegroup'
    ],

    'AWS::ECS::FargateCluster': [
        'AWS::ECS::TaskDefinitionFargate',
        'AWS::ECS::ServiceFargate'
    ],    

    'AWS::DMS::ReplicationInstance': [
        'AWS::DMS::ReplicationTask'
    ],

    'AWS::CloudWatch::Dashboard': [
        'AWS::CloudWatch::Alarm'
    ],

    'AWS::APS::Workspace': [
        'AWS::IAM::RoleForPrometheusQuery',
        'AWS::IAM::RoleForPrometheusWrite'
    ],

    'AWS::AutoScaling::AutoScalingGroup': [
        'AWS::AutoScaling::ScalingPolicy'
    ],

    'AWS::Organizations::Organization': [
        'AWS::Organizations::OrganizationalUnit',
        'AWS::Organizations::Policy'
    ],

    'AWS::CloudFront::Distribution': [
        'AWS::ApiGateway::MethodForCloudfront'
    ],

    'AWS::VpcLattice::ServiceNetwork': [
        'AWS::VpcLattice::Service',
        'AWS::VpcLattice::Listener',
        'AWS::ApiGateway::VpcLink'
    ],

    'AWS::EC2::VPCEndpointService': [
        'AWS::ElasticLoadBalancingV2::Listener',
        'AWS::EC2::VPCEndpointServicePermissions'
    ]
}

@app.post("/getsuggestions")
async def get_suggestion(request: ClassList):
    items = request.items
    new_types = []
    for class_type in items:
        new_types.extend(SUGGESTIONS.get(class_type, []))

    return {"message": new_types}