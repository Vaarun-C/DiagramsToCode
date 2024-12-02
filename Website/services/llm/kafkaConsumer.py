from kafka import KafkaConsumer, KafkaProducer
import json
import logging

# Kafka configuration
KAFKA_BROKER = "localhost:9092"
DETECTED_SERVICES_TOPIC = "detected-services-topic"
DETECTED_PLUS_SUGGESTIONS_TOPIC = "final-services-topic"
DLQ_TOPIC = "service-suggestions-dead-letter-queue"

# Suggestion rules
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

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ServiceSuggestionsConsumer")

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    DETECTED_SERVICES_TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    group_id="service-suggestions-group",
    auto_offset_reset="earliest",
)

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda x: json.dumps(x).encode("utf-8"),
)

def process_services(items):
    """
    Generate new types based on existing items using SUGGESTIONS rules.
    """
    new_types = []
    for class_type in items:
        # Append suggestions for each class_type if present
        new_types.extend(SUGGESTIONS.get(class_type, []))
    return new_types

def handle_dead_letter(message):
    """
    Send the failed message to a dead-letter queue.
    """
    try:
        producer.send(DLQ_TOPIC, message)
        logger.info(f"Message sent to Dead Letter Queue: {message}")
    except Exception as e:
        logger.error(f"Failed to send message to DLQ: {e}")

def main():
    for message in consumer:
        try:
            payload = message.value
            logger.info(f"Received message: {payload}")

            detections = payload.get("detections")
            if not detections:
                logger.error("No 'detections' found in the message payload.")
                continue

            icon_detection_types = [det["classType"] for det in detections]

            # Generate suggestions based on rules
            suggestions = process_services(icon_detection_types)

            combined_messages = icon_detection_types + suggestions

            # Prepare the result message
            result = {
                "uuid": payload.get("uuid", "unknown"),
                "filename": payload.get("filename", "unknown"),
                "data": combined_messages
            }

            # Send the result to the target topic
            producer.send(DETECTED_PLUS_SUGGESTIONS_TOPIC, result)
            logger.info(f"Sent suggestions to topic '{DETECTED_PLUS_SUGGESTIONS_TOPIC}': {result}")

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            handle_dead_letter(message.value)

if __name__ == "__main__":
    main()
