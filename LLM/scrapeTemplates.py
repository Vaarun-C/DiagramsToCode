import os
import json
import sys
import shutil
import yaml
import subprocess
from colorama import Fore, Back, Style

github_links = [
    "https://github.com/aws-solutions-library-samples/.github",
    "https://github.com/aws-solutions-library-samples/amazon-elasticache-caching-for-amazon-rds",
    "https://github.com/aws-solutions-library-samples/amazon-personalize-online-recommendations-with-google-tag-manager",
    "https://github.com/aws-solutions-library-samples/aws-batch-arch-for-protein-folding",
    "https://github.com/aws-solutions-library-samples/aws-insurancelake-etl",
    "https://github.com/aws-solutions-library-samples/aws-insurancelake-infrastructure",
    "https://github.com/aws-solutions-library-samples/aws-ops-automator",
    "https://github.com/aws-solutions-library-samples/breweries-sitewise-simulator",
    "https://github.com/aws-solutions-library-samples/cfn-ps-dotnetcore-fargate-cicd",
    "https://github.com/aws-solutions-library-samples/cfn-ps-microsoft-activedirectory",
    "https://github.com/aws-solutions-library-samples/distributed-compute-on-aws-with-cross-regional-dask",
    "https://github.com/aws-solutions-library-samples/fraud-detection-using-machine-learning",
    "https://github.com/aws-solutions-library-samples/guidance-for-a-multi-tenant-generative-ai-gateway-with-cost-and-usage-tracking-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-active-active-replication-on-amazon-rds-for-mysql",
    "https://github.com/aws-solutions-library-samples/guidance-for-ai-assistants-with-amazon-q-business",
    "https://github.com/aws-solutions-library-samples/guidance-for-ai-driven-player-insights-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-amazon-vpc-lattice-automated-dns-configuration-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-analytics-observability-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-analyzing-customer-conversations-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-asynchronous-inference-with-stable-diffusion-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-attachment-management-to-aws-cloud-wan",
    "https://github.com/aws-solutions-library-samples/Guidance-for-Authentication-with-Digital-Wallets-on-AWS",
    "https://github.com/aws-solutions-library-samples/guidance-for-automated-deletion-of-vault-archives-in-amazon-s3-glacier",
    "https://github.com/aws-solutions-library-samples/guidance-for-automated-geospatial-insights-engine-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-automated-provisioning-of-application-ready-amazon-eks-clusters",
    "https://github.com/aws-solutions-library-samples/guidance-for-automated-restore-and-copy-for-amazon-s3-glacier-objects",
    "https://github.com/aws-solutions-library-samples/guidance-for-automating-amazon-vpc-routing-in-a-global-cloud-wan-deployment",
    "https://github.com/aws-solutions-library-samples/guidance-for-automating-ethereum-node-validator-using-graviton-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-automating-network-monitoring-and-alerting-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-automating-password-rotation-with-amazon-fsx-for-netapp-ontap",
    "https://github.com/aws-solutions-library-samples/guidance-for-automating-sap-configuration-health-checks-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-aws-deepracer-event-management",
    "https://github.com/aws-solutions-library-samples/guidance-for-aws-iot-greengrass-foundations",
    "https://github.com/aws-solutions-library-samples/guidance-for-aws-sustainability-insights-framework",
    "https://github.com/aws-solutions-library-samples/guidance-for-aws-sustainability-insights-framework-cli",
    "https://github.com/aws-solutions-library-samples/guidance-for-baseline-security-assessment-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-battery-digital-twin-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-bioinformatics-workflow-development-using-devops-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-building-a-high-performance-numerical-weather-prediction-system-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-building-a-real-time-bidder-for-advertising-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-building-a-sap-cloud-data-warehouse-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-building-a-sustainability-data-fabric-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-buy-it-now-on-third-party-website-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-carbon-data-lake-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-cell-based-architecture-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-chatbot-user-feedback-and-analytics-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-configuring-virtual-calls-on-salesforce-using-amazon-chime",
    "https://github.com/aws-solutions-library-samples/guidance-for-connecting-data-products-with-amazon-datazone",
    "https://github.com/aws-solutions-library-samples/guidance-for-container-runtime-security-monitoring-with-cncf-falco-and-aws-security-hub",
    "https://github.com/aws-solutions-library-samples/guidance-for-content-management-using-salesforce-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-continuous-data-migration-from-apache-cassandra-to-amazon-keyspaces",
    "https://github.com/aws-solutions-library-samples/guidance-for-conversational-chatbots-using-retrieval-augmented-generation-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-creating-a-customized-coding-companion-with-amazon-q-developer",
    "https://github.com/aws-solutions-library-samples/guidance-for-creating-a-personalized-avatar-with-amazon-sagemaker",
    "https://github.com/aws-solutions-library-samples/guidance-for-crossregion-failover-and-graceful-failback-and-observability-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-custom-domain-names-on-amazon-api-gateway-private-endpoints",
    "https://github.com/aws-solutions-library-samples/guidance-for-custom-game-backend-hosting-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-custom-search-of-an-enterprise-knowledge-base-with-amazon-opensearch-service",
    "https://github.com/aws-solutions-library-samples/guidance-for-customer-lifetime-value-analytics-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-customizing-normalization-library-for-aws-entity-resolution",
    "https://github.com/aws-solutions-library-samples/guidance-for-data-fabric-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-datalake-with-sap-and-non-sap-data-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-deduplicating-syndicated-data-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-deploying-a-data-transfer-dashboard-for-adtech-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-designing-resilient-applications-with-amazon-aurora-and-amazon-rds-proxy",
    "https://github.com/aws-solutions-library-samples/guidance-for-detecting-malware-threats-using-aws-transfer-family-managed-workflows-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-developing-apple-vision-pro-applications-with-unity-on-amazon-ec2",
    "https://github.com/aws-solutions-library-samples/guidance-for-devops-on-amazon-redshift",
    "https://github.com/aws-solutions-library-samples/guidance-for-digital-assets-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-digital-thread-using-graph-and-generative-ai-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-disaster-recovery-using-amazon-aurora",
    "https://github.com/aws-solutions-library-samples/guidance-for-e-commerce-products-similarity-search-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-ec2-spot-placement-score-tracker",
    "https://github.com/aws-solutions-library-samples/guidance-for-ecs-canary-deployments-for-backend-workloads-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-electric-vehicle-battery-health-prediction-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-enhancing-the-customer-experience-for-travel-and-hospitality-using-amazon-bedrock",
    "https://github.com/aws-solutions-library-samples/guidance-for-enterprise-search-and-audit-for-amazon-s3",
    "https://github.com/aws-solutions-library-samples/guidance-for-environmental-impact-factor-mapping-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-event-driven-application-auto-scaling-with-keda-on-amazon-eks",
    "https://github.com/aws-solutions-library-samples/guidance-for-external-connectivity-amazon-vpc-lattice",
    "https://github.com/aws-solutions-library-samples/guidance-for-full-duplex-open-platform-communication-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-galaxy-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-game-analytics-pipeline-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-game-production-environment-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-game-server-hosting-using-agones-and-open-match-on-amazon-eks",
    "https://github.com/aws-solutions-library-samples/guidance-for-generating-product-descriptions-with-amazon-bedrock",
    "https://github.com/aws-solutions-library-samples/guidance-for-generative-ai-deployments-using-amazon-sagemaker-jumpstart",
    "https://github.com/aws-solutions-library-samples/guidance-for-generative-ai-model-optimization-using-amazon-sagemaker",
    "https://github.com/aws-solutions-library-samples/guidance-for-generative-ai-shopping-assistant-using-agents-for-amazon-bedrock",
    "https://github.com/aws-solutions-library-samples/guidance-for-geospatial-insights-for-sustainability-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-handling-data-during-traffic-spikes-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-high-availability-oracle-databases-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-high-speed-rag-chatbots-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-implementing-google-privacy-sandbox-key-value-service-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-implementing-the-google-privacy-sandbox-aggregation-service-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-improving-application-development-productivity-with-the-sap-abap-assistant-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-incremental-data-exports-from-amazon-dynamodb-to-amazon-s3",
    "https://github.com/aws-solutions-library-samples/guidance-for-incremental-data-exports-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-industrial-digital-twin-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-integrated-scalable-search-for-amazon-documentdb",
    "https://github.com/aws-solutions-library-samples/guidance-for-integrating-3rd-party-saas-data-with-amazon-appflow-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-intelligent-route-optimization-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-iso20022-messaging-workflows-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-live-streams-hosted-by-digital-humans-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-low-code-intelligent-document-processing-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-low-latency-high-throughput-model-inference-using-amazon-sagemaker",
    "https://github.com/aws-solutions-library-samples/guidance-for-machine-learning-inference-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-media-provenance-with-c2pa-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-media2cloud-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-meter-data-analytics-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-modernizing-electric-vehicle-charging-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-monitoring-and-optimizing-energy-usage-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-monitoring-high-cardinality-telecom-metrics-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-multi-account-environment-on-amazon-quicksight",
    "https://github.com/aws-solutions-library-samples/guidance-for-multi-cluster-application-management-with-karmada-and-amazon-eks",
    "https://github.com/aws-solutions-library-samples/guidance-for-multi-modal-data-analysis-with-aws-health-and-ml-services",
    "https://github.com/aws-solutions-library-samples/guidance-for-multi-region-application-data-using-amazon-aurora",
    "https://github.com/aws-solutions-library-samples/guidance-for-multi-region-serverless-batch-applications-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-natural-language-queries-of-relational-databases-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-near-real-time-data-migration-from-apache-cassandra-to-amazon-keyspaces",
    "https://github.com/aws-solutions-library-samples/guidance-for-object-level-insights-and-cost-savings-with-amazon-s3",
    "https://github.com/aws-solutions-library-samples/guidance-for-okta-phone-based-multi-factor-authentication-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-optimizing-heterogeneous-auto-scaling-group-resource-utilization-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-oracle-migrations-to-amazon-aurora-postgresql-using-aws-dms",
    "https://github.com/aws-solutions-library-samples/guidance-for-patient-entity-resolution-with-aws-healthlake",
    "https://github.com/aws-solutions-library-samples/guidance-for-payment-systems-using-event-driven-architecture-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-persistent-world-game-hosting-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-personalized-engagement-using-online-and-mobile-user-behaviors-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-predictive-maintenance-with-amazon-monitron",
    "https://github.com/aws-solutions-library-samples/guidance-for-preparing-and-validating-records-for-entity-resolution-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-processing-overhead-imagery-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-processing-real-time-data-using-amazon-dynamo-db",
    "https://github.com/aws-solutions-library-samples/guidance-for-product-substitutions-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-product-traceability-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-programmatic-deployment-of-ndi-discovery-servers-for-broadcast-workflows-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-querying-sustainability-documents-using-generative-ai-for-esg-reporting-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-real-time-text-search-using-amazon-opensearch-service",
    "https://github.com/aws-solutions-library-samples/guidance-for-receiving-digital-imaging-and-communications-in-medicine-images-in-amazon-s3",
    "https://github.com/aws-solutions-library-samples/guidance-for-recency-frequency-and-monetization-analysis-on-amazon-pinpoint",
    "https://github.com/aws-solutions-library-samples/guidance-for-resilient-data-applications-using-amazon-dynamodb",
    "https://github.com/aws-solutions-library-samples/guidance-for-responsible-content-moderation-with-ai-services-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-retail-analytics-using-generative-ai-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-sap-data-integration-and-management-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-sap-generative-ai-assistant-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-scaling-electronic-design-automation-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-scheduling-batch-jobs-for-mainframe-modernization-service-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-secure-access-to-external-package-repositories-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-secure-blockchain-validation-using-aws-nitro-enclaves",
    "https://github.com/aws-solutions-library-samples/guidance-for-self-calibrating-level-4-digital-twins-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-self-healing-code-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-sentiment-analysis-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-simple-ecommerce-website-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-smart-and-sustainable-buildings-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-sql-based-etl-with-apache-spark-on-amazon-eks",
    "https://github.com/aws-solutions-library-samples/guidance-for-streamlining-data-access-with-jira-service-management-and-amazon-datazone",
    "https://github.com/aws-solutions-library-samples/guidance-for-text-generation-using-embeddings-from-enterprise-data-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-third-party-marketplace-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-tracking-assets-and-locating-devices-using-aws-iot",
    "https://github.com/aws-solutions-library-samples/guidance-for-training-an-aws-deepracer-model-using-amazon-sagemaker",
    "https://github.com/aws-solutions-library-samples/guidance-for-transactional-fraud-detection-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-ultra-low-latency-machine-learning-feature-stores-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-understanding-your-data-lineage-on-amazon-quickSight",
    "https://github.com/aws-solutions-library-samples/guidance-for-using-email-templates-with-amazon-pinpoint-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-using-google-tag-manager-for-server-side-website-analytics-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-utility-bill-processing-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-virtual-personal-stylist-on-aws",
    "https://github.com/aws-solutions-library-samples/guidance-for-visual-search-on-aws",
    "https://github.com/aws-solutions-library-samples/machine-learning-for-telecommunications",
    "https://github.com/aws-solutions-library-samples/multi-region-infrastructure-deployment",
    "https://github.com/aws-solutions-library-samples/osml-cdk-constructs",
    "https://github.com/aws-solutions-library-samples/osml-cesium-globe",
    "https://github.com/aws-solutions-library-samples/osml-data-intake",
    "https://github.com/aws-solutions-library-samples/osml-imagery-toolkit",
    "https://github.com/aws-solutions-library-samples/osml-model-runner",
    "https://github.com/aws-solutions-library-samples/osml-model-runner-test",
    "https://github.com/aws-solutions-library-samples/osml-models",
    "https://github.com/aws-solutions-library-samples/osml-tile-server",
    "https://github.com/aws-solutions-library-samples/osml-tile-server-test",
    "https://github.com/aws-solutions-library-samples/real-time-analytics-spark-streaming",
    "https://github.com/aws-solutions-library-samples/real-time-live-sports-updates-using-aws-appsync",
    "https://github.com/aws-solutions-library-samples/serverless-fixity-for-digital-preservation-compliance"
]
temp_directory = "./tempRepo"
temp_template_directory = "./temp_templates"
    
# Define a custom constructor for !tags
def tag_constructor(loader, node):
    if isinstance(node, yaml.ScalarNode):
        return {node.tag: loader.construct_scalar(node)}
    elif isinstance(node, yaml.MappingNode):
        return {node.tag: loader.construct_mapping(node)}
    elif isinstance(node, yaml.SequenceNode):
        return {node.tag: loader.construct_sequence(node)}
    else:
        raise TypeError("Unsupported node type")

# Extend SafeLoader to handle the tags
class CustomLoader(yaml.SafeLoader):
    pass

# Add the custom constructor for the !Ref tag
custom_tags = ["!Ref", "!Base64", "!Sub", "!GetAtt", "!Join", "!If", "!Select", "!Split", "!FindInMap"]
for tag in custom_tags:
    CustomLoader.add_constructor(tag, tag_constructor)

def lint(path):
    wrong_templates = {}
    right_templates = set()

    for template in os.listdir(path):
        if(template.endswith(".yaml") == False):
            continue
        print("Linting:", template)
        cfn_output = os.system(f"cfn-lint {template}")
        if cfn_output != 0:
            wrong_templates[template] = cfn_output
        else:
            right_templates.add(template)


    print("-"*5, "RIGHT TEMPLATES", "-"*5)
    for template in right_templates:
        print(template)

    print("-"*5, "WRONG TEMPLATES", "-"*5)
    print(json.dumps(wrong_templates, indent=4))

    return right_templates

def print_breaks(reason):
    heading = "*"*15+ reason+ "*"*15
    n = len(heading)
    print()
    print("*"*n)
    print(heading)
    print("*"*n)
    print()

def checkForDescAndVersion(templates):

    correct_templates = []
    wrong_templates = []

    for template in templates:
        with open(temp_template_directory+"/"+template, "r") as yaml_file:
            yaml_data = yaml.load(yaml_file, Loader=CustomLoader)
            if(not isinstance(yaml_data, dict)):
                print(f"Skipping {template} as it is not a dict...")
                continue

            print(f"{Fore.RED} TEMPLATE: {template}")
            print(Style.RESET_ALL)

            version = yaml_data.get("AWSTemplateFormatVersion")
            desc = yaml_data.get("Description")
            print(f"{Fore.YELLOW} VERSION: {version}")
            print(f"{Fore.GREEN} Description: {desc}")
            print(Style.RESET_ALL)

            if((version is not None) and (desc is not None)):
                correct_templates.append(template)
            else:
                wrong_templates.append(template)

    return (correct_templates, wrong_templates)

def main():

    os.makedirs(temp_directory, exist_ok = True) 

    # Clone into directory tempRepo
    for repo in github_links[:10]:
        os.makedirs(temp_template_directory, exist_ok = True) 

        print_breaks(f"CLONING {repo}")
        os.system(f"git clone {repo} {temp_directory}")

        print_breaks("MOVING .YAML FILES")
        subprocess.run(["find", temp_directory, "-name", "*.yaml", "-exec", "cp", "{}", temp_template_directory, ";"])
        
        print_breaks("LINTING")
        linted_templates = lint(temp_template_directory)

        if len(linted_templates) != 0:
            print_breaks("CHECKING FOR VERSION AND DESCRIPTIONS")
            correct_templates, wrong_templates = checkForDescAndVersion(linted_templates)

            if(len(wrong_templates) > 0):
                print(Style.RESET_ALL)
                print(f"{Back.CYAN} {Fore.BLACK} These templates have both version and description and are linted:{Style.RESET_ALL}")
                print(Fore.BLUE, end="")

                for i, template in enumerate(correct_templates):
                    print(i, template)

                print(Style.RESET_ALL, end="")
                
                for template in correct_templates:
                    confirmation = input(f"MOVE {Back.YELLOW} {Fore.BLACK} {template} {Style.RESET_ALL} TO DATASET?")
                    if(confirmation == 'y'):
                        print(f"{Back.GREEN} MOVING TEMPLATE {template} {Style.RESET_ALL}")
                    else:
                        print(f"{Back.RED} SKIPPING TEMPLATE {template} {Style.RESET_ALL}")
                    print()

            if(len(wrong_templates) > 0):
                print(f"{Fore.RED} Make changes to these templates and move them manually.... (Missing version or description) {Style.RESET_ALL}")
                print(Fore.BLUE, end="")

                for i, template in enumerate(wrong_templates):
                    print(i, template)

                print(Style.RESET_ALL, end="")
            input("Continue?...")

        print_breaks("REMOVING CONTENTS OF tempRepo")
        try:
            shutil.rmtree(temp_directory)
            print('Folder and its content removed') # Folder and its content removed
        except:
            print('Folder not deleted')

        print_breaks("REMOVING CONTENTS OF temp_templates")
        try:
            shutil.rmtree(temp_template_directory)
            print('Folder and its content removed') # Folder and its content removed
        except Exception as e:
            print('Folder not deleted: ', e)

if __name__ == "__main__":
    main()
