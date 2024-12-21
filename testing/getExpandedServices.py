from groundTruth import ground_truth_data
from detected_icons_passthru import a as detected_types_data
from helper import write_dict

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

output_file = './suggested_types.txt'
output_results = {}
for img_name, detected_data in detected_types_data.items():
    detected_types = [*map(lambda x:x[1],detected_data)]
    new_types = []
    for det_type in detected_types:
        new_types.extend(LLM_SUGGESTIONS.get(det_type, []))
    output_results[img_name] = [*map(lambda x: f"\"{x}\"",detected_types + new_types)]

write_dict(output_file, output_results)
