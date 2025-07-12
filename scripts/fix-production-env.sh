#!/bin/bash

# Fix Production Environment Variables Script
# This script helps configure the correct environment variables for production

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔧 Production Environment Fix Script${NC}"
echo "=================================="

echo -e "\n${YELLOW}Current Production URLs:${NC}"
echo "Frontend: https://repotorpedo-frontend.onrender.com"
echo "Backend:  https://repotorpedo-backend.onrender.com"

echo -e "\n${YELLOW}Required Environment Variables for Backend:${NC}"
echo "================================================"
echo "BASE_URL=https://repotorpedo-backend.onrender.com"
echo "GITHUB_CALLBACK_URL=https://repotorpedo-backend.onrender.com/api/auth/github/callback"
echo "ALLOWED_ORIGINS=https://repotorpedo-frontend.onrender.com"
echo "ENVIRONMENT=production"
echo "GITHUB_CLIENT_ID=<your_github_client_id>"
echo "GITHUB_CLIENT_SECRET=<your_github_client_secret>"
echo "OPENAI_API_KEY=<your_openai_api_key>"
echo "SECRET_KEY=<your_secret_key>"

echo -e "\n${YELLOW}Required Environment Variables for Frontend:${NC}"
echo "================================================"
echo "REACT_APP_API_URL=https://repotorpedo-backend.onrender.com"
echo "REACT_APP_ENVIRONMENT=production"

echo -e "\n${YELLOW}Steps to Fix:${NC}"
echo "============="
echo "1. Go to https://dashboard.render.com"
echo "2. Select the 'repotorpedo-backend' service"
echo "3. Go to Environment → Environment Variables"
echo "4. Update the following variables:"
echo "   - BASE_URL: https://repotorpedo-backend.onrender.com"
echo "   - GITHUB_CALLBACK_URL: https://repotorpedo-backend.onrender.com/api/auth/github/callback"
echo "   - ALLOWED_ORIGINS: https://repotorpedo-frontend.onrender.com"
echo "5. Save and redeploy the service"

echo -e "\n${YELLOW}GitHub OAuth App Configuration:${NC}"
echo "====================================="
echo "1. Go to https://github.com/settings/developers"
echo "2. Find your OAuth App"
echo "3. Update the Authorization callback URL to:"
echo "   https://repotorpedo-backend.onrender.com/api/auth/github/callback"

echo -e "\n${YELLOW}Test Commands:${NC}"
echo "=============="
echo "curl -I https://repotorpedo-backend.onrender.com/api/auth/github/login"
echo "curl -s https://repotorpedo-backend.onrender.com/api/auth/status"

echo -e "\n${GREEN}After updating the environment variables, the OAuth login should work correctly!${NC}" 