#!/bin/bash

# Quick Production Fix Script
# This script automatically fixes the OAuth 404 error using Render CLI

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 Quick Production OAuth Fix${NC}"
echo "============================="

# Check if user is logged in
if ! render whoami > /dev/null 2>&1; then
    echo -e "${RED}❌ Not logged in to Render${NC}"
    echo "Please run: render login"
    exit 1
fi

echo -e "${GREEN}✅ Logged in as: $(render whoami)${NC}"

# Find service IDs
echo -e "\n${YELLOW}Finding your services...${NC}"
BACKEND_SERVICE=$(render services list --output json | jq -r '.[] | select(.name | contains("backend")) | .id' | head -1)
FRONTEND_SERVICE=$(render services list --output json | jq -r '.[] | select(.name | contains("frontend")) | .id' | head -1)

if [ -z "$BACKEND_SERVICE" ]; then
    echo -e "${RED}❌ Backend service not found${NC}"
    echo "Available services:"
    render services list --output text
    exit 1
fi

if [ -z "$FRONTEND_SERVICE" ]; then
    echo -e "${RED}❌ Frontend service not found${NC}"
    echo "Available services:"
    render services list --output text
    exit 1
fi

echo -e "${GREEN}✅ Found services:${NC}"
echo "Backend:  $BACKEND_SERVICE"
echo "Frontend: $FRONTEND_SERVICE"

# Update backend environment variables
echo -e "\n${YELLOW}Updating backend environment variables...${NC}"
render env set BASE_URL=https://repotorpedo-backend.onrender.com --service-id $BACKEND_SERVICE
render env set GITHUB_CALLBACK_URL=https://repotorpedo-backend.onrender.com/api/auth/github/callback --service-id $BACKEND_SERVICE
render env set ALLOWED_ORIGINS=https://repotorpedo-frontend.onrender.com --service-id $BACKEND_SERVICE
render env set ENVIRONMENT=production --service-id $BACKEND_SERVICE
echo -e "${GREEN}✅ Backend environment variables updated${NC}"

# Update frontend environment variables
echo -e "\n${YELLOW}Updating frontend environment variables...${NC}"
render env set REACT_APP_API_URL=https://repotorpedo-backend.onrender.com --service-id $FRONTEND_SERVICE
render env set REACT_APP_ENVIRONMENT=production --service-id $FRONTEND_SERVICE
echo -e "${GREEN}✅ Frontend environment variables updated${NC}"

# Redeploy services
echo -e "\n${YELLOW}Redeploying services...${NC}"
echo "Redeploying backend..."
render deploy --service-id $BACKEND_SERVICE
echo "Redeploying frontend..."
render deploy --service-id $FRONTEND_SERVICE

echo -e "\n${GREEN}🎉 Production fix completed!${NC}"
echo "============================="
echo "Your services are being redeployed with the correct environment variables."
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Wait 2-3 minutes for deployment to complete"
echo "2. Update your GitHub OAuth app callback URL to:"
echo "   https://repotorpedo-backend.onrender.com/api/auth/github/callback"
echo "3. Test the login at: https://repotorpedo-frontend.onrender.com"
echo ""
echo -e "${BLUE}To verify the fix, run:${NC}"
echo "./scripts/verify-production-fix.sh" 