#!/bin/bash

# Exit on any error
set -e

# Colour Codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'

NC='\033[0m' # Reset color

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
K8S_DIR="${SCRIPT_DIR}/../k8s"

echo -e "${BLUE}Starting cluster deployment...${NC}"
echo -e "Using configuration files from: ${K8S_DIR}"

# Create namespace
echo -e "${GREEN}Creating namespace...${NC}"
kubectl apply -f "${K8S_DIR}/namespace.yaml"

# Install Redis
echo -e "${GREEN}Installing Redis...${NC}"
helm install redis1 bitnami/redis -f "${K8S_DIR}/redis/redis1-values.yaml" --namespace diagrams2code
helm install redis2 bitnami/redis -f "${K8S_DIR}/redis/redis2-values.yaml" --namespace diagrams2code

# Wait for Redis instances to be ready
echo -e "${RED}Waiting for Redis instances to be ready...${NC}"
kubectl wait --for=condition=ready pod redis1-master-0 -n diagrams2code --timeout=300s
kubectl wait --for=condition=ready pod redis2-master-0 -n diagrams2code --timeout=300s

# Update Redis passwords
echo -e "${GREEN}Updating Redis passwords...${NC}"
"${SCRIPT_DIR}/updateRedisPasswords.sh"

# Apply configs and secrets
echo -e "${GREEN}Applying configs...${NC}"
kubectl apply -f "${K8S_DIR}/configs/"
echo -e "${GREEN}Applying secrets...${NC}"
kubectl apply -f "${K8S_DIR}/secrets/"

# Deploy ZooKeeper
echo -e "${GREEN}Deploying ZooKeeper...${NC}"
kubectl apply -f "${K8S_DIR}/zookeeper"

# Wait for ZooKeeper to be ready
echo -e "${RED}Waiting for ZooKeeper to be ready...${NC}"
kubectl wait --for=condition=ready pod -l app=zookeeper -n diagrams2code --timeout=300s

# Deploy Kafka after ZooKeeper is ready
echo -e "${GREEN}Deploying Kafka...${NC}"
kubectl apply -f "${K8S_DIR}/kafka/."

# Wait for Kafka to be ready
echo -e "${RED}Waiting for Kafka to be ready...${NC}"
kubectl wait --for=condition=ready pod -l app=kafka-broker -n diagrams2code --timeout=300s

# Deploy API Gateway and microservices
echo -e "${GREEN}Deploying API Gateway...${NC}"
kubectl apply -f "${K8S_DIR}/api-gateway/"

echo -e "${GREEN}Deploying microservices...${NC}"
kubectl apply -f "${K8S_DIR}/microservices/"

echo -e "${BLUE}Cluster deployment completed successfully!${NC}"