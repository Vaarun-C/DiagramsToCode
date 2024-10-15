const RESOURCES = {}
const waitInterval = 3000
//https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html

function getRequiredProps(){
    const props = document.getElementsByClassName('variablelist')[0].firstChild.children;
    var obj = {}
    for(let i=0;i<props.length/2;i+=2){//iterates over every property
        const prop = props[i];
        const propData = props[i+1].innerText;
        const baseStr = propData.indexOf('Required:');
        if (propData.slice(baseStr+"Required:".length+1).startsWith("No")) continue;
        obj[prop] = propData;
    }
    return obj;
}

async function getResourceTypes(){
    for (const rsc of document.getElementsByClassName('itemizedlist')[1].children){ //every rsc type
        const a_tag = rsc.getElementsByTagName('a')[0];
        const rsc_name = a_tag.innerText;

        a_tag.click();
        await new Promise((resolve) => setTimeout(resolve, waitInterval));// Wait waitInterval milliseconds

        RESOURCES[rsc_name] = getRequiredProps();

        window.history.back();
        await new Promise((resolve) => setTimeout(resolve, waitInterval));// Wait waitInterval milliseconds
    }
}

async function collectDetails(){
    var resources = document.getElementsByClassName('highlights')[0];
    for (const resource of resources.getElementsByTagName('ul')[0].children){// every rsc

        resource.getElementsByTagName('a')[0].click();
        await new Promise((resolve) => setTimeout(resolve, waitInterval));// Wait waitInterval milliseconds
        
        await getResourceTypes();

        window.history.back();        
        await new Promise((resolve) => setTimeout(resolve, waitInterval));// Wait waitInterval milliseconds

        console.log(RESOURCES);
    }
}

await collectDetails();



var resources = document.getElementsByClassName('highlights')[0];
for (const resource of resources.getElementsByTagName('ul')[0].children){// every rsc
    const a_tag = resource.getElementsByTagName('a')[0];
    window.open(a_tag.href, '_blank');
}


//STEP 1
obj = {}
var resources = document.getElementsByClassName('highlights')[0];
for (const resource of resources.getElementsByTagName('ul')[0].children){// every rsc
    const a_tag = resource.getElementsByTagName('a')[0];

    obj[a_tag.innerText] = a_tag.href
}
console.log(JSON.stringify(obj))

main_links = {
    "AWS Amplify Console":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Amplify.html",
    "AWS Amplify UI Builder":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AmplifyUIBuilder.html",
    "Amazon API Gateway":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ApiGateway.html",
    "Amazon API Gateway V2":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ApiGatewayV2.html",
    "AWS AppConfig":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AppConfig.html",
    "Amazon AppFlow":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AppFlow.html",
    "Amazon AppIntegrations":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AppIntegrations.html",
    "Application Auto Scaling":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ApplicationAutoScaling.html",
    "AWS App Mesh":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AppMesh.html",
    "AWS App Runner":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AppRunner.html",
    "Amazon AppStream 2.0":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AppStream.html",
    "AWS AppSync":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AppSync.html",
    "AWS ARC - Zonal Shift":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ARCZonalShift.html",
    "Alexa Skills Kit":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Alexa_ASK.html",
    "Amazon Athena":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Athena.html",
    "AWS Audit Manager":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AuditManager.html",
    "AWS Auto Scaling":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AutoScalingPlans.html",
    "AWS B2B Data Interchange":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_B2BI.html",
    "AWS Backup":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Backup.html",
    "AWS Backup gateway":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_BackupGateway.html",
    "AWS Batch":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Batch.html",
    "Amazon Bedrock":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Bedrock.html",
    "AWS Billing Conductor":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_BillingConductor.html",
    "AWS Budgets":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Budgets.html",
    "AWS Certificate Manager":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CertificateManager.html",
    "AWS Chatbot":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Chatbot.html",
    "AWS Clean Rooms":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CleanRooms.html",
    "CleanRoomsML":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CleanRoomsML.html",
    "AWS Cloud9":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Cloud9.html",
    "AWS CloudFormation":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CloudFormation.html",
    "Amazon CloudFront":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CloudFront.html",
    "AWS Cloud Map":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ServiceDiscovery.html",
    "AWS CloudTrail":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CloudTrail.html",
    "Amazon CloudWatch":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CloudWatch.html",
    "Amazon CloudWatch Application Insights":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ApplicationInsights.html",
    "CloudWatch Application Signals":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ApplicationSignals.html",
    "Amazon CloudWatch Evidently":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Evidently.html",
    "Amazon CloudWatch Internet Monitor":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_InternetMonitor.html",
    "Amazon CloudWatch Logs":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Logs.html",
    "Amazon CloudWatch Synthetics":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Synthetics.html",
    "AWS CodeArtifact":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CodeArtifact.html",
    "AWS CodeBuild":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CodeBuild.html",
    "AWS CodeCommit":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CodeCommit.html",
    "AWS CodeConnections":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CodeConnections.html",
    "AWS CodeDeploy":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CodeDeploy.html",
    "Amazon CodeGuru Profiler":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CodeGuruProfiler.html",
    "Amazon CodeGuru Reviewer":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CodeGuruReviewer.html",
    "AWS CodePipeline":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CodePipeline.html",
    "AWS CodeStar":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CodeStar.html",
    "AWS CodeStar Connections":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CodeStarConnections.html",
    "AWS CodeStar Notifications":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CodeStarNotifications.html",
    "Amazon Cognito":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Cognito.html",
    "Amazon Comprehend":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Comprehend.html",
    "AWS Config":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Config.html",
    "Amazon Connect":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Connect.html",
    "Amazon Connect Outbound Campaigns":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ConnectCampaigns.html",
    "AWS Control Tower":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ControlTower.html",
    "Amazon Connect Customer Profiles":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CustomerProfiles.html",
    "AWS Cost Explorer":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CE.html",
    "AWS Cost and Usage Report":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CUR.html",
    "AWS Data Exports":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_BCMDataExports.html",
    "Amazon Data Lifecycle Manager":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DLM.html",
    "AWS Data Pipeline":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DataPipeline.html",
    "AWS DataSync":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DataSync.html",
    "Amazon DataZone":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DataZone.html",
    "AWS Deadline Cloud":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Deadline.html",
    "DynamoDB Accelerator":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DAX.html",
    "Amazon Detective":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Detective.html",
    "AWS Device Farm":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DeviceFarm.html",
    "Amazon DevOps Guru":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DevOpsGuru.html",
    "AWS Directory Service":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DirectoryService.html",
    "AWS Database Migration Service":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DMS.html",
    "Amazon DocumentDB (with MongoDB compatibility)":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DocDB.html",
    "Amazon DocumentDB (with MongoDB compatibility) elastic":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DocDBElastic.html",
    "Amazon DynamoDB":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DynamoDB.html",
    "Amazon EC2":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_EC2.html",
    "Amazon EC2 Auto Scaling":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AutoScaling.html",
    "Amazon ECR":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ECR.html",
    "Amazon ECS":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ECS.html",
    "Amazon Elastic File System":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_EFS.html",
    "Amazon Elastic Kubernetes Service":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_EKS.html",
    "AWS Elastic Beanstalk":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ElasticBeanstalk.html",
    "Elastic Load Balancing":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ElasticLoadBalancing.html",
    "Elastic Load Balancing V2":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ElasticLoadBalancingV2.html",
    "Amazon EMR":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_EMR.html",
    "Amazon EMR Serverless":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_EMRServerless.html",
    "Amazon EMR on EKS":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_EMRContainers.html",
    "Amazon ElastiCache":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ElastiCache.html",
    "AWS Entity Resolution":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_EntityResolution.html",
    "Amazon EventBridge":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Events.html",
    "Amazon EventBridge Pipes":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Pipes.html",
    "Amazon EventBridge Scheduler":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Scheduler.html",
    "Amazon EventBridge Schemas":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_EventSchemas.html",
    "Amazon FinSpace schemas":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_FinSpace.html",
    "AWS Fault Injection Service":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_FIS.html",
    "AWS Firewall Manager":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_FMS.html",
    "Amazon Forecast":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Forecast.html",
    "Amazon Fraud Detector":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_FraudDetector.html",
    "Amazon FSx":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_FSx.html",
    "Amazon GameLift":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_GameLift.html",
    "AWS Global Accelerator":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_GlobalAccelerator.html",
    "AWS Glue":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Glue.html",
    "AWS Glue DataBrew":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DataBrew.html",
    "Amazon Managed Grafana":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Grafana.html",
    "AWS Ground Station":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_GroundStation.html",
    "Amazon GuardDuty":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_GuardDuty.html",
    "AWS HealthImaging":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_HealthImaging.html",
    "AWS HealthLake":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_HealthLake.html",
    "AWS Identity and Access Management":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_IAM.html",
    "AWS IAM Identity Center":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SSO.html",
    "Identity Store":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_IdentityStore.html",
    "AWS Identity and Access Management Access Analyzer":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AccessAnalyzer.html",
    "EC2 Image Builder":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ImageBuilder.html",
    "AWS Systems Manager Incident Manager":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SSMIncidents.html",
    "AWS Systems Manager Incident Manager Contacts":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SSMContacts.html",
    "Amazon Inspector classic":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Inspector.html",
    "Amazon Inspector":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_InspectorV2.html",
    "AWS IoT":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_IoT.html",
    "AWS IoT 1-Click":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_IoT1Click.html",
    "AWS IoT Analytics":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_IoTAnalytics.html",
    "AWS IoT Core Device Advisor":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_IoTCoreDeviceAdvisor.html",
    "AWS IoT Events":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_IoTEvents.html",
    "Fleet Hub for AWS IoT Device Management":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_IoTFleetHub.html",
    "AWS IoT FleetWise":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_IoTFleetWise.html",
    "AWS IoT Greengrass":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Greengrass.html",
    "AWS IoT Greengrass Version 2":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_GreengrassV2.html",
    "AWS IoT SiteWise":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_IoTSiteWise.html",
    "AWS IoT TwinMaker":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_IoTTwinMaker.html",
    "AWS IoT Wireless":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_IoTWireless.html",
    "Amazon IVS":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_IVS.html",
    "Amazon IVS Chat":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_IVSChat.html",
    "Amazon Kendra":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Kendra.html",
    "Amazon Kendra Intelligent Ranking":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_KendraRanking.html",
    "Amazon Keyspaces (for Apache Cassandra)":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Cassandra.html",
    "Amazon Kinesis":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Kinesis.html",
    "Amazon Managed Service for Apache Flink":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_KinesisAnalytics.html",
    "Amazon Managed Service for Apache Flink V2":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_KinesisAnalyticsV2.html",
    "Amazon Data Firehose":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_KinesisFirehose.html",
    "Amazon Kinesis Video Streams":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_KinesisVideo.html",
    "AWS Key Management Service":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_KMS.html",
    "AWS Lake Formation":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_LakeFormation.html",
    "AWS Lambda":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Lambda.html",
    "AWS Launch Wizard":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_LaunchWizard.html",
    "Amazon Lex":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Lex.html",
    "AWS License Manager":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_LicenseManager.html",
    "Amazon Lightsail":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Lightsail.html",
    "Amazon Location Service":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Location.html",
    "Amazon Lookout for Equipment":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_LookoutEquipment.html",
    "Amazon Lookout for Metrics":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_LookoutMetrics.html",
    "Amazon Lookout for Vision":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_LookoutVision.html",
    "AWS Mainframe Modernization":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_M2.html",
    "AWS Mainframe Modernization Application Testing":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AppTest.html",
    "Amazon Macie":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Macie.html",
    "Amazon Managed Blockchain":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ManagedBlockchain.html",
    "AWS Elemental MediaConnect":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_MediaConnect.html",
    "AWS Elemental MediaConvert":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_MediaConvert.html",
    "AWS Elemental MediaLive":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_MediaLive.html",
    "AWS Elemental MediaPackage":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_MediaPackage.html",
    "AWS Elemental MediaPackage V2":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_MediaPackageV2.html",
    "AWS Elemental MediaTailor":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_MediaTailor.html",
    "AWS Elemental MediaStore":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_MediaStore.html",
    "Amazon MQ":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AmazonMQ.html",
    "Amazon MemoryDB":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_MemoryDB.html",
    "Amazon Managed Streaming for Apache Kafka":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_MSK.html",
    "Amazon Managed Streaming for Apache Kafka Connect":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_KafkaConnect.html",
    "Amazon Managed Workflows for Apache Airflow":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_MWAA.html",
    "Amazon Neptune":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Neptune.html",
    "Amazon Neptune Analytics":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_NeptuneGraph.html",
    "AWS Network Firewall":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_NetworkFirewall.html",
    "AWS Network Manager":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_NetworkManager.html",
    "Amazon Nimble Studio":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_NimbleStudio.html",
    "Observability Access Manager (OAM)":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Oam.html",
    "AWS HealthOmics":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Omics.html",
    "Amazon OpenSearch Ingestion":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_OSIS.html",
    "Amazon OpenSearch Service":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_OpenSearchService.html",
    "Amazon OpenSearch Service (legacy Elasticsearch resource)":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Elasticsearch.html",
    "Amazon OpenSearch Serverless":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_OpenSearchServerless.html",
    "AWS OpsWorks":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_OpsWorks.html",
    "AWS OpsWorks CM":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_OpsWorksCM.html",
    "AWS Organizations":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Organizations.html",
    "AWS Panorama":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Panorama.html",
    "AWS Payment Cryptography":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_PaymentCryptography.html",
    "Amazon Personalize":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Personalize.html",
    "Amazon Pinpoint":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Pinpoint.html",
    "Amazon Pinpoint Email":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_PinpointEmail.html",
    "AWS Private Certificate Authority":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ACMPCA.html",
    "AWS Private Certificate Authority for Active Directory":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_PCAConnectorAD.html",
    "AWS Private Certificate Authority Connector for SCEP":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_PCAConnectorSCEP.html",
    "AWS Proton":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Proton.html",
    "Amazon Managed Service for Prometheus":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_APS.html",
    "Amazon Q Business":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_QBusiness.html",
    "Amazon QLDB":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_QLDB.html",
    "Amazon QuickSight":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_QuickSight.html",
    "AWS Resource Access Manager":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_RAM.html",
    "Amazon Relational Database Service":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_RDS.html",
    "Amazon Redshift":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Redshift.html",
    "Amazon Redshift Serverless":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_RedshiftServerless.html",
    "AWS Migration Hub Refactor Spaces":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_RefactorSpaces.html",
    "Amazon Rekognition":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Rekognition.html",
    "AWS Resilience Hub":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ResilienceHub.html",
    "AWS Resource Explorer":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ResourceExplorer2.html",
    "AWS Resource Groups":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ResourceGroups.html",
    "AWS RoboMaker":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_RoboMaker.html",
    "IAM Roles Anywhere":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_RolesAnywhere.html",
    "Amazon Route 53":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Route53.html",
    "Amazon Route 53 Recovery Control":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Route53RecoveryControl.html",
    "Amazon Route 53 Recovery Readiness":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Route53RecoveryReadiness.html",
    "Amazon Route 53 Resolver":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Route53Resolver.html",
    "Amazon Route 53 Profiles":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Route53Profiles.html",
    "Amazon CloudWatch RUM":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_RUM.html",
    "Amazon S3":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_S3.html",
    "Amazon S3 Express":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_S3Express.html",
    "Amazon S3 Object Lambda":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_S3ObjectLambda.html",
    "Amazon S3 on Outposts":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_S3Outposts.html",
    "Amazon SageMaker":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SageMaker.html",
    "AWS Secrets Manager":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SecretsManager.html",
    "Amazon Security Lake":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SecurityLake.html",
    "AWS Service Catalog":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ServiceCatalog.html",
    "AWS Service Catalog AppRegistry":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ServiceCatalogAppRegistry.html",
    "AWS Security Hub":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SecurityHub.html",
    "Amazon Simple Email Service":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SES.html",
    "Amazon SimpleDB":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SDB.html",
    "AWS Shield":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Shield.html",
    "AWS Signer":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Signer.html",
    "AWS SimSpace Weaver":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SimSpaceWeaver.html",
    "Amazon Simple Notification Service":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SNS.html",
    "Amazon Simple Queue Service":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SQS.html",
    "AWS Step Functions":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_StepFunctions.html",
    "AWS Systems Manager":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SSM.html",
    "AWS Systems Manager Quick Setup":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SSMQuickSetup.html",
    "AWS Support App":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SupportApp.html",
    "AWS Systems Manager for SAP":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SystemsManagerSAP.html",
    "Amazon Timestream":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Timestream.html",
    "AWS Transfer Family":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Transfer.html",
    "Amazon Verified Permissions":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_VerifiedPermissions.html",
    "Amazon Connect Voice ID":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_VoiceID.html",
    "Amazon VPC Lattice":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_VpcLattice.html",
    "AWS WAF":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_WAF.html",
    "AWS WAF Regional":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_WAFRegional.html",
    "AWS WAF V2":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_WAFv2.html",
    "Amazon Connect Wisdom":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Wisdom.html",
    "Amazon WorkSpaces":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_WorkSpaces.html",
    "Amazon WorkSpaces Thin Client":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_WorkSpacesThinClient.html",
    "Amazon WorkSpaces Secure Browser":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_WorkSpacesWeb.html",
    "AWS X-Ray":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_XRay.html",    
    "Shared property types":"https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-reference-shared.html"
}
