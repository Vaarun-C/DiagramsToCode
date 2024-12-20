#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Set paths relative to the script's directory
TEMPLATE_PATH="$SCRIPT_DIR/redis-config-template.yaml"
OUTPUT_PATH="$SCRIPT_DIR/../k8s/configs/redis-configmap.yaml"

# Fetch Redis passwords
REDIS1_PASSWORD=$(kubectl get secret --namespace diagrams2code redis1 -o jsonpath="{.data.redis-password}" | base64 -d)
REDIS2_PASSWORD=$(kubectl get secret --namespace diagrams2code redis2 -o jsonpath="{.data.redis-password}" | base64 -d)

# Replace placeholders in the template
sed -e "s/{{REDIS1_PASSWORD}}/$REDIS1_PASSWORD/" \
    -e "s/{{REDIS2_PASSWORD}}/$REDIS2_PASSWORD/" \
    "$TEMPLATE_PATH" > "$OUTPUT_PATH"

echo "ConfigMap updated with Redis passwords."
