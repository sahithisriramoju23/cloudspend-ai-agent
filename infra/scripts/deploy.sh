#!/bin/bash

echo "Deploying CloudSpend AI..."

# Build Docker images
docker-compose -f infra/docker/docker-compose.yml build

# Start services
docker-compose -f infra/docker/docker-compose.yml up -d

echo "Deployment complete!"
