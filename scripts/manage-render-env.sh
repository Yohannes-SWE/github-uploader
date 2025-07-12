#!/bin/bash

# Render Environment Variables Management Script
# This script helps manage environment variables for Render services

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔧 Render Environment Variables Manager${NC}"
echo "====================================="

# Check if user is logged in
if ! render whoami > /dev/null 2>&1; then
    echo -e "${RED}❌ Not logged in to Render${NC}"
    echo "Please run: render login"
    exit 1
fi

echo -e "${GREEN}✅ Logged in to Render as: $(render whoami)${NC}"

# Function to list services
list_services() {
    echo -e "\n${YELLOW}Available Services:${NC}"
    echo "=================="
    render services list --format table
}

# Function to show current environment variables
show_env_vars() {
    local service_id=$1
    echo -e "\n${YELLOW}Current Environment Variables for $service_id:${NC}"
    echo "============================================="
    render env list --service-id $service_id --format table
}

# Function to update environment variables
update_env_vars() {
    local service_id=$1
    echo -e "\n${YELLOW}Updating Environment Variables for $service_id:${NC}"
    echo "============================================="
    
    # Backend environment variables
    if [[ $service_id == *"backend"* ]]; then
        echo "Setting backend environment variables..."
        render env set BASE_URL=https://repotorpedo-backend.onrender.com --service-id $service_id
        render env set GITHUB_CALLBACK_URL=https://repotorpedo-backend.onrender.com/api/auth/github/callback --service-id $service_id
        render env set ALLOWED_ORIGINS=https://repotorpedo-frontend.onrender.com --service-id $service_id
        render env set ENVIRONMENT=production --service-id $service_id
        echo -e "${GREEN}✅ Backend environment variables updated${NC}"
    fi
    
    # Frontend environment variables
    if [[ $service_id == *"frontend"* ]]; then
        echo "Setting frontend environment variables..."
        render env set REACT_APP_API_URL=https://repotorpedo-backend.onrender.com --service-id $service_id
        render env set REACT_APP_ENVIRONMENT=production --service-id $service_id
        echo -e "${GREEN}✅ Frontend environment variables updated${NC}"
    fi
}

# Function to redeploy service
redeploy_service() {
    local service_id=$1
    echo -e "\n${YELLOW}Redeploying $service_id:${NC}"
    echo "======================="
    render deploy --service-id $service_id
}

# Main menu
while true; do
    echo -e "\n${BLUE}Choose an option:${NC}"
    echo "1. List all services"
    echo "2. Show environment variables for a service"
    echo "3. Update backend environment variables"
    echo "4. Update frontend environment variables"
    echo "5. Redeploy backend service"
    echo "6. Redeploy frontend service"
    echo "7. Update all environment variables and redeploy"
    echo "8. Exit"
    
    read -p "Enter your choice (1-8): " choice
    
    case $choice in
        1)
            list_services
            ;;
        2)
            read -p "Enter service ID: " service_id
            show_env_vars $service_id
            ;;
        3)
            read -p "Enter backend service ID: " service_id
            update_env_vars $service_id
            ;;
        4)
            read -p "Enter frontend service ID: " service_id
            update_env_vars $service_id
            ;;
        5)
            read -p "Enter backend service ID: " service_id
            redeploy_service $service_id
            ;;
        6)
            read -p "Enter frontend service ID: " service_id
            redeploy_service $service_id
            ;;
        7)
            echo -e "\n${YELLOW}This will update all environment variables and redeploy both services${NC}"
            read -p "Enter backend service ID: " backend_id
            read -p "Enter frontend service ID: " frontend_id
            update_env_vars $backend_id
            update_env_vars $frontend_id
            redeploy_service $backend_id
            redeploy_service $frontend_id
            echo -e "\n${GREEN}🎉 All services updated and redeployed!${NC}"
            ;;
        8)
            echo "Goodbye!"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid choice. Please try again.${NC}"
            ;;
    esac
done 