#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Cleaning up Smart Hotel IoT Infrastructure${NC}"

# Stop all containers
docker-compose down

# Remove created volumes (optional)
read -p "Do you want to remove all data volumes? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    docker volume prune -f
    rm -rf ./data/postgres
    rm -rf ./data/redis
fi

echo -e "${GREEN}Cleanup completed successfully!${NC}" 