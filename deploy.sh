#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Starting Smart Hotel IoT Infrastructure Deployment${NC}"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

# Create necessary directories
echo "Creating required directories..."
mkdir -p ./data/postgres
mkdir -p ./data/redis

# Set up environment variables
echo "Setting up environment variables..."
cp .env.example .env 2>/dev/null || echo "No .env.example file found, skipping..."

# Build and start containers
echo "Building and starting containers..."
docker-compose up --build -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 10

# Run database migrations
echo "Running database migrations..."
docker-compose exec web flask db upgrade

echo -e "${GREEN}Deployment completed successfully!${NC}"
echo "Access the application at: http://localhost:5000" 