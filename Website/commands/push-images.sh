#!/bin/bash
@echo off

echo Building and pushing images to Docker Hub

# Enable experimental features for Buildx (if not already enabled)
export DOCKER_CLI_EXPERIMENTAL=enabled

# Create a new Buildx builder if one does not exist
docker buildx create --use

docker buildx build --platform linux/amd64,linux/arm64 -t capthestone/website-awsicons:latest --push .

# Multi-platform build for the frontend image
docker buildx build --platform linux/amd64,linux/arm64 -t "capthestone/frontend:latest" ../diagrams-to-code --push
echo "Built and pushed frontend:latest for amd64 and arm64"

# Multi-platform build for website-service image
docker buildx build --platform linux/amd64,linux/arm64 -t "capthestone/website-awsicons:latest" ../services/awsicons --push
echo "Built and pushed website-awsicons:latest for amd64 and arm64"

# Multi-platform build for website-generateawstemplate image
docker buildx build --platform linux/amd64,linux/arm64 -t "capthestone/website-generateawstemplate:latest" ../services/generateawstemplate --push
echo "Built and pushed website-generateawstemplate:latest for amd64 and arm64"

# Multi-platform build for website-llm image
docker buildx build --platform linux/amd64,linux/arm64 -t "capthestone/website-llm:latest" ../services/llm --push
echo "Built and pushed website-llm:latest for amd64 and arm64"

docker push "capthestone/frontend:latest"
echo Pushed frontend:latest to Docker Hub

docker push "capthestone/website-awsicons:latest"
echo Pushed website-awsicons:latest to Docker Hub

docker push "capthestone/website-generateawstemplate:latest"
echo Pushed website-generateawstemplate:latest to Docker Hub

docker push "capthestone/website-llm:latest"
echo Pushed website-llm:latest to Docker Hub