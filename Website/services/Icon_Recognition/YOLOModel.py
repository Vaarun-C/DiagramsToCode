from ultralytics import YOLO
from PIL import Image
from Detection_Object import detection_object
from ultralytics.engine.results import Results

class yolomodel:
    def __init__(self) -> None:       
        self.model = YOLO("298_icons_best.pt")
        self.conf_thresh = 0.6
        self.CLS_NAME_TO_TYPE = {
            # Analytics
            "Arch_Amazon-EMR_64": "AWS::EMR::Cluster",
            "Arch_Amazon-Kinesis_64": "AWS::Kinesis::Stream",
            "Arch_Amazon-Kinesis-Data-Streams_64": "AWS::Kinesis::Stream",
            "Arch_Amazon-Kinesis-Video-Streams_64": "AWS::Kinesis::Stream",
            "Arch_Amazon-Managed-Streaming-for-Apache-Kafka_64": "AWS::MSK::Cluster",
            "Arch_Amazon-OpenSearch-Service_64": "AWS::OpenSearchService::Domain",
            "Arch_Amazon-Redshift_64": "AWS::Redshift::Cluster",
            "Arch_AWS-Glue_64": "AWS::Glue::Database",

            # App Integration
            "Arch_Amazon-EventBridge_64": "AWS::Events::EventBus",
            "Arch_Amazon-Managed-Workflows-for-Apache-Airflow_64": "AWS::MWAA::Environment",
            "Arch_Amazon-MQ_64": "AWS::AmazonMQ::Broker",
            "Arch_Amazon-Simple-Notification-Service_64": "AWS::SNS::Topic",
            "Arch_Amazon-Simple-Queue-Service_64": "AWS::SQS::Queue",
            "Arch_AWS-AppSync_64": "AWS::AppSync::GraphQLApi",
            "Arch_AWS-Step-Functions_64": "AWS::StepFunctions::StateMachine",

            # Artificial Intelligence
            "Arch_Amazon-Kendra_64": "AWS::Kendra::Index",
            "Arch_Amazon-Lex_64": "AWS::Lex::Bot",
            "Arch_Amazon-SageMaker_64": "AWS::SageMaker::NotebookInstance",
            "Arch_Amazon-SageMaker-Studio-Lab_64": "AWS::SageMaker::NotebookInstance",
            "Arch_Amazon-Bedrock_64": "AWS::IAM::RoleForBedrock",
            "Arch_Amazon-Comprehend_64": "AWS::IAM::RoleForComprehend",
            "Arch_Amazon-Transcribe_64": "AWS::IAM::RoleForTranscribeExecution",
            "Arch_Amazon-Polly_64": "AWS::IAM::RoleForPollyExecution",
            
            # Compute
            "Arch_Amazon-EC2_64": "AWS::EC2::Instance",
            "Arch_AWS-Batch_64": "AWS::Batch::ComputeEnvironment",
            "Arch_AWS-Elastic-Beanstalk_64": "AWS::ElasticBeanstalk::Application",
            "Arch_AWS-Lambda_64": "AWS::Lambda::Function",
            "Arch_Elastic-Load-Balancing_64": "AWS::ElasticLoadBalancingV2::TargetGroup",

            #Containers
            "Arch_Amazon-Elastic-Container-Service_64": "AWS::ECS::Cluster",
            "Arch_Amazon-Elastic-Kubernetes-Service_64": "AWS::EKS::Cluster",
            "Arch_AWS-Fargate_64": "AWS::ECS::FargateCluster",

            # Database
            "Arch_Amazon-Aurora_64": "AWS::RDS::DBCluster",
            "Arch_Amazon-RDS_64": "AWS::RDS::DBInstance",
            "Arch_Amazon-DynamoDB_64": "AWS::DynamoDB::Table",
            "Arch_Amazon-ElastiCache_64": "AWS::ElastiCache::CacheCluster",
            "Arch_AWS-Database-Migration-Service_64": "AWS::DMS::ReplicationInstance",

            # Management-Governance
            "Arch_Amazon-CloudWatch_64": "AWS::CloudWatch::Dashboard",
            "Arch_Amazon-Managed-Grafana_64": "AWS::Grafana::Workspace",
            "Arch_Amazon-Managed-Service-for-Prometheus_64": "AWS::APS::Workspace",
            "Arch_AWS-Auto-Scaling_64": "AWS::AutoScaling::AutoScalingGroup",
            "Arch_AWS-CloudTrail_64": "AWS::CloudTrail::Trail",
            "Arch_AWS-Control-Tower_64": "AWS::Organizations::Organization",

            # Networking
            "Arch_Amazon-API-Gateway_64": "AWS::ApiGateway::RestApi",
            "Arch_Amazon-CloudFront_64": "AWS::CloudFront::Distribution",
            "Arch_Amazon-Route-53_64": "AWS::Route53::RecordSet",
            "Arch_Amazon-VPC-Lattice_64": "AWS::VpcLattice::ServiceNetwork",
            "Arch_AWS-PrivateLink_64": "AWS::EC2::VPCEndpointService",

            # Storage
            "Arch_Amazon-Simple-Storage-Service_64": "AWS::S3::Bucket",

            # Security
            "Arch_AWS-Key-Management-Service_64": "AWS::KMS::Key"
        }
        self.model_names = self.model.names

    def predict(self, architectureDiagram: Image) -> list[detection_object]:
        all_classes = set(range(298))
        removed_classes = set([57])
        allowed_classes = list(all_classes-removed_classes)

        results = self.model.predict(architectureDiagram, save=False, classes=allowed_classes, conf=self.conf_thresh)
        detections = results[0].boxes
        detection_objects = []
        
        for det in detections:
            x_min, y_min, x_max, y_max = det.xyxy[0].tolist()
            class_name = self.model_names[int(det.cls)]
            
            try:
                class_type = self.CLS_NAME_TO_TYPE[class_name]
                detection_objects.append(detection_object([x_max, y_max, x_min, y_min], class_type, float(det.conf)))
            except KeyError:
                print(class_name, "not in Mongo yet !!!!")

        return detection_objects