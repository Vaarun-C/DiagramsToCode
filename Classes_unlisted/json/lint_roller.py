import subprocess

files= ['Arch_Amazon-Braket_64.json',
'Arch_Amazon-CodeWhisperer_64.json',
'Arch_Amazon-Detective_64.json',
'Arch_Amazon-EventBridge_64.json',
'Arch_Amazon-Fraud-Detector_64.json',
'Arch_Amazon-Managed-Grafana_64.json',
'Arch_Amazon-Simple-Queue-Service_64.json',
'Arch_AWS-AppConfig_64.json',
'Arch_AWS-AppFabric_64.json',
'Arch_AWS-Cloud-Development-Kit_64.json',
'Arch_AWS-Cloud9_64.json',
'Arch_AWS-CodeBuild_64.json',
'Arch_AWS-DeepRacer_64.json',
'Arch_AWS-Elemental-MediaStore_64.json',
'Arch_AWS-Fault-Injection-Service_64.json',
'Arch_AWS-Glue_64.json',
'Arch_AWS-Ground-Station_64.json',
'Arch_AWS-HealthLake_64.json',
'Arch_AWS-Identity-and-Access-Management_64.json',
'Arch_AWS-IoT-Device-Management_64.json',
'Arch_AWS-IoT-TwinMaker_64.json',
'Arch_AWS-Proton_64.json',
'Arch_AWS-Resource-Access-Manager_64.json',
'Arch_AWS-Signer_64.json']


for i in files:
    subprocess.run(['cfn-lint', i])
