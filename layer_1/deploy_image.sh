#!/usr/bin/env bash

set -e

echo "Starting multi-region ECR deployment..."

AWS_ACCOUNT_ID="830359385979"
REPO_NAME="backend_service_gaurang"
IMAGE_TAG="stable"

MUMBAI_REGION="ap-south-1"
LONDON_REGION="eu-west-2"

pushd ./backend_api
    echo "Building Docker image..."
    docker build -t ${REPO_NAME}:${IMAGE_TAG} .
popd

push_to_region() {
    local region=$1
    local ecr_uri="${AWS_ACCOUNT_ID}.dkr.ecr.${region}.amazonaws.com/${REPO_NAME}_${region}"
    
    
    aws ecr get-login-password --region ${region} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${region}.amazonaws.com
    docker tag ${REPO_NAME}:${IMAGE_TAG} ${ecr_uri}:${IMAGE_TAG}

    echo "Pushing to ${region}"
    docker push ${ecr_uri}:${IMAGE_TAG}
    echo "Successfully pushed to ${region}"
}

push_to_region ${MUMBAI_REGION} ${MUMBAI_ECR}
push_to_region ${LONDON_REGION} ${LONDON_ECR}