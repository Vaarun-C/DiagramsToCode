mapTypesToNames = {
'AWS::EFS::FileSystem': 'Arch_Amazon-EFS_64', #Varun
'AWS::EC2::VPNConnection': 'Arch_AWS-Site-to-Site-VPN_64', # Varun
'AWS::IAM::Role':'Arch_Amazon-Translate_64',#Vikas
"AWS::EC2::VPC":'Arch_Amazon-Virtual-Private-Cloud_64',#Vikas
'AWS::IAM::Role': 'Arch_AWS-Identity-and-Access-Management_64', # Varun
'AWS::MediaPackage::Channel':'Arch_AWS-Elemental-MediaPackage_64',#Vikas
# 'Arch_AWS-Local-Zones_64', # GPT says This is managed outside of CloudFormation through the AWS Management Console, CLI, or API.
'AWS::LakeFormation::DataLakeSettings': 'Arch_AWS-Lake-Formation_64', #Varun
'AWS::IoTSiteWise::AssetModel': 'Arch_AWS-IoT-SiteWise_64', # Varun
'AWS::DataSync::Task':'Arch_AWS-DataSync_64',#Vikas
'AWS::Transfer::Server':'Arch_AWS-Transfer-Family_64',#Vikas
'AWS::IAM::Role':'Arch_Amazon-Chime-SDK_64',#Vikas
'AWS::CleanRooms::Collaboration':'Arch_AWS-Clean-Rooms_64',#Vikas
'AWS::Rekognition::StreamProcessor':'Arch_Amazon-Rekognition_64',#Vikas
'AWS::GuardDuty::Detector':'Arch_Amazon-GuardDuty_64',#Vikas
'AWS::Connect::Instance':'Arch_Amazon-Connect_64',
'AWS::IoT::SecurityProfile': 'Arch_AWS-IoT-Device-Defender_64', # Varun
'AWS::HealthLake::FHIRDatastore':'Arch_AWS-HealthLake_64',#Vikas
'AWS::ECR::Repository': 'Arch_Amazon-Elastic-Container-Registry_64', # Varun
'AWS::KinesisFirehose::DeliveryStream':'Arch_Amazon-Data-Firehose_64',#Vikas
'AWS::IoT::Thing': 'Arch_AWS-IoT-Core_64', # Varun
'AWS::Pinpoint::App': 'Arch_Amazon-Pinpoint_64', # Varun
'AWS::Shield::Protection': 'Arch_AWS-Shield_64', # Varun
'AWS::CodeCommit::Repository':'Arch_AWS-CodeCommit_64',#Vikas
'AWS::IoTFleetHub::Application': 'Arch_AWS-IoT-FleetWise_64', # Varun
'AWS::RAM::ResourceShare': 'Arch_AWS-Resource-Access-Manager_64', # Varun
'AWS::Amplify::App': 'Arch_AWS-Amplify_64',    # Varun
'AWS::MediaStore::Container':'Arch_AWS-Elemental-MediaStore_64',#Vikas
'AWS::FIS::ExperimentTemplate': 'Arch_AWS-Fault-Injection-Service_64',  # Varun
'AWS::Neptune::DBCluster': 'Arch_Amazon-Neptune_64', #Varun
'AWS::CertificateManager::Certificate': 'Arch_AWS-Certificate-Manager_64', # Varun
'AWS::ACMPCA::CertificateAuthority': 'Arch_AWS-Private-Certificate-Authority_64', # Varun
'AWS::CloudFormation::Stack': 'Arch_AWS-CloudFormation_64', # Varun
'AWS::Timestream::Database': 'Arch_Amazon-Timestream_64', # Varun
'AWS::SecretsManager::Secret': 'Arch_AWS-Secrets-Manager_64', # Varun
# 'Arch_AWS-Cloud-Development-Kit_64',#NOT A THIJNG ANYMORE
'AWS::Cognito::UserPool': 'Arch_Amazon-Cognito_64',    # Varun
'AWS::GlobalAccelerator::Accelerator': 'Arch_AWS-Global-Accelerator_64', #Varun
'AWS::QuickSight::Visualization': 'Arch_Amazon-QuickSight_64', # Varun
'AWS::CodeBuild::Project': 'Arch_AWS-CodeBuild_64', # Varun
'AWS::DataZone::Environment': 'Arch_Amazon-DataZone_64', # Varun
'AWS::Location::Map': 'Arch_Amazon-Location-Service_64', # Varun
'AWS::S3Outposts::Bucket': 'Arch_AWS-Outposts-rack_64', # Varun
'AWS::CodePipeline::Pipeline': 'Arch_AWS-CodePipeline_64', # Varun
# 'Arch_Amazon-Chime_64', # Can't find
'AWS::ROSA::Service': 'Arch_Red-Hat-OpenShift-Service-on-AWS_64', # Varun
'AWS::SES::EmailIdentity': 'Arch_Amazon-Simple-Email-Service_64', # Varun
'AWS::IoT::Thing': 'Arch_AWS-IoT-Device-Management_64', # Varun
'AWS::Comprehend::DocumentClassifier':'Arch_Amazon-Comprehend-Medical_64',#Vikas
'AWS::SecurityHub::Hub':'Arch_AWS-Security-Hub_64',#Vikas
'AWS::WAFv2::WebACL': 'Arch_AWS-WAF_64', # Varun
'AWS::SSM::Document': 'Arch_AWS-Systems-Manager_64', # Varun (If the architecture focuses on automation, runbooks, or operational tasks.)
'AWS::EC2::TransitGateway': 'Arch_AWS-Transit-Gateway_64', # Varun
'AWS::Athena::WorkGroup':'Arch_Amazon-Athena_64', #Vikas
'AWS::DataSync::LocationFSxLustre':'Arch_Amazon-FSx-for-Lustre_64',#Vikas
'AWS::EC2::Volume': 'Arch_Amazon-Elastic-Block-Store_64', # Varun According to GPT o7
'AWS::Backup::BackupPlan':'Arch_AWS-Backup_64',#Vikas
# 'Arch_Bottlerocket_64',#Can't find
# 'Arch_Amazon-EKS-Cloud_64',
'AWS::QLDB::Ledger':'Arch_Amazon-Quantum-Ledger-Database_64'#Vikas
}