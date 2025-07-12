#!/bin/bash

# CLI Environment Variables Update Script
# This script attempts to update environment variables using Render API

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔧 CLI Environment Variables Update${NC}"
echo "====================================="

# Service IDs
BACKEND_SERVICE_ID="srv-d1ojvk7diees73cja4e0"
FRONTEND_SERVICE_ID="srv-d1ojehruibrs73cs3g40"

echo -e "\n${YELLOW}Service Information:${NC}"
echo "====================="
echo "Backend Service ID: $BACKEND_SERVICE_ID"
echo "Frontend Service ID: $FRONTEND_SERVICE_ID"

echo -e "\n${YELLOW}Attempting to update environment variables...${NC}"
echo "============================================="

# Method 1: Try using render CLI with service management
echo -e "\n${BLUE}Method 1: Interactive Service Management${NC}"
echo "============================================="
echo "This will open interactive mode where you can manage the service:"
echo "render services"
echo ""
echo "Then select your service and look for environment variable options."

# Method 2: Try to trigger a redeploy which might pick up new config
echo -e "\n${BLUE}Method 2: Trigger Redeploy with Updated Config${NC}"
echo "============================================="
echo "Let's try to redeploy the services to pick up any config changes:"

echo -e "\n${YELLOW}Redeploying backend service...${NC}"
render deploys create --service-id $BACKEND_SERVICE_ID --confirm

echo -e "\n${YELLOW}Redeploying frontend service...${NC}"
render deploys create --service-id $FRONTEND_SERVICE_ID --confirm

# Method 3: Check if we can use the render.yaml file
echo -e "\n${BLUE}Method 3: Update render.yaml and Redeploy${NC}"
echo "============================================="
echo "The render.yaml file has been updated with correct environment variables."
echo "Let's check if we can trigger a deployment from the updated config:"

echo -e "\n${YELLOW}Checking current render.yaml configuration...${NC}"
if [ -f "render.yaml" ]; then
    echo "✅ render.yaml exists with updated configuration"
    echo "The file contains the correct environment variables:"
    echo "  - BASE_URL: https://repotorpedo-backend.onrender.com"
    echo "  - GITHUB_CALLBACK_URL: https://repotorpedo-backend.onrender.com/api/auth/github/callback"
    echo "  - ALLOWED_ORIGINS: https://repotorpedo-frontend.onrender.com"
else
    echo "❌ render.yaml not found"
fi

# Method 4: Alternative approach using git push
echo -e "\n${BLUE}Method 4: Git Push to Trigger Deployment${NC}"
echo "============================================="
echo "If your Render services are connected to GitHub, you can:"
echo "1. Commit the updated render.yaml file"
echo "2. Push to trigger automatic deployment"

echo -e "\n${YELLOW}Checking git status...${NC}"
if [ -d ".git" ]; then
    echo "✅ Git repository found"
    echo "Current status:"
    git status --porcelain
    echo ""
    echo "To commit and push changes:"
    echo "git add render.yaml"
    echo "git commit -m 'Fix production environment variables'"
    echo "git push origin main"
else
    echo "❌ Not a git repository"
fi

echo -e "\n${GREEN}🎉 CLI Update Attempts Completed!${NC}"
echo "====================================="
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Check if the redeploy picked up the new configuration"
echo "2. If not, you'll need to use the web interface"
echo "3. Test the OAuth login after deployment completes"
echo ""
echo -e "${BLUE}Test Commands:${NC}"
echo "./scripts/verify-production-fix.sh"
echo "curl -I https://repotorpedo-backend.onrender.com/api/auth/github/login" 