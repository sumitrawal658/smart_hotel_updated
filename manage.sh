#!/bin/bash

GREEN='\033[0;32m'
NC='\033[0m'

while true; do
    clear
    echo -e "${GREEN}Smart Hotel IoT Infrastructure Management${NC}"
    echo "1. Deploy Infrastructure"
    echo "2. Stop Infrastructure"
    echo "3. View Logs"
    echo "4. Restart Services"
    echo "5. Exit"
    
    read -p "Select an option: " choice
    
    case $choice in
        1) ./deploy.sh ;;
        2) ./cleanup.sh ;;
        3) docker-compose logs --tail=100 -f ;;
        4) docker-compose restart ;;
        5) exit 0 ;;
        *) echo "Invalid option" ;;
    esac
    
    read -p "Press enter to continue..."
done 