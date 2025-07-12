#!/bin/bash

# Manual Production Environment Fix Script
# This script provides detailed steps to fix the OAuth 404 error

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔧 Manual Production Environment Fix${NC}"
echo "====================================="

echo -e "\n${RED}🚨 URGENT: OAuth 404 Error Detected${NC}"
echo "The OAuth callback URL is pointing to localhost instead of production."
echo "This is causing the login to fail with a 404 error."

echo -e "\n${YELLOW}📋 Step-by-Step Fix Instructions:${NC}"
echo "====================================="

echo -e "\n${BLUE}Step 1: Access Render Dashboard${NC}"
echo "1. Open your browser and go to: https://dashboard.render.com"
echo "2. Sign in to your Render account"
echo "3. Find your project/team"

echo -e "\n${BLUE}Step 2: Update Backend Environment Variables${NC}"
echo "1. Click on the 'repotorpedo-backend' service"
echo "2. Go to the 'Environment' tab"
echo "3. Click 'Environment Variables'"
echo "4. Update or add these variables:"
echo ""
echo -e "${GREEN}Variable Name:${NC} BASE_URL"
echo -e "${GREEN}Value:${NC} https://repotorpedo-backend.onrender.com"
echo ""
echo -e "${GREEN}Variable Name:${NC} GITHUB_CALLBACK_URL"
echo -e "${GREEN}Value:${NC} https://repotorpedo-backend.onrender.com/api/auth/github/callback"
echo ""
echo -e "${GREEN}Variable Name:${NC} ALLOWED_ORIGINS"
echo -e "${GREEN}Value:${NC} https://repotorpedo-frontend.onrender.com"
echo ""
echo -e "${GREEN}Variable Name:${NC} ENVIRONMENT"
echo -e "${GREEN}Value:${NC} production"

echo -e "\n${BLUE}Step 3: Update Frontend Environment Variables${NC}"
echo "1. Go back to your services list"
echo "2. Click on the 'repotorpedo-frontend' service"
echo "3. Go to the 'Environment' tab"
echo "4. Click 'Environment Variables'"
echo "5. Update or add these variables:"
echo ""
echo -e "${GREEN}Variable Name:${NC} REACT_APP_API_URL"
echo -e "${GREEN}Value:${NC} https://repotorpedo-backend.onrender.com"
echo ""
echo -e "${GREEN}Variable Name:${NC} REACT_APP_ENVIRONMENT"
echo -e "${GREEN}Value:${NC} production"

echo -e "\n${BLUE}Step 4: Redeploy Services${NC}"
echo "1. After updating environment variables, go to the 'Manual Deploy' tab"
echo "2. Click 'Deploy latest commit' for both services"
echo "3. Wait for deployment to complete (usually 2-3 minutes)"

echo -e "\n${BLUE}Step 5: Update GitHub OAuth App${NC}"
echo "1. Go to: https://github.com/settings/developers"
echo "2. Find your OAuth App (likely named 'Repo Torpedo' or similar)"
echo "3. Click 'Edit'"
echo "4. Update the 'Authorization callback URL' to:"
echo -e "${GREEN}https://repotorpedo-backend.onrender.com/api/auth/github/callback${NC}"
echo "5. Click 'Update application'"

echo -e "\n${BLUE}Step 6: Test the Fix${NC}"
echo "1. Go to: https://repotorpedo-frontend.onrender.com"
echo "2. Try clicking the 'Login with GitHub' button"
echo "3. You should be redirected to GitHub for authorization"
echo "4. After authorization, you should be redirected back to the app"

echo -e "\n${YELLOW}🔍 Verification Commands:${NC}"
echo "=========================="
echo "Run these commands to verify the fix:"
echo ""
echo "curl -v https://repotorpedo-backend.onrender.com/api/auth/github/login"
echo "curl -s https://repotorpedo-backend.onrender.com/api/auth/status"

echo -e "\n${GREEN}✅ Expected Result:${NC}"
echo "The OAuth login should now work without 404 errors!"

echo -e "\n${YELLOW}⚠️  Troubleshooting:${NC}"
echo "=================="
echo "If you still get errors:"
echo "1. Check that all environment variables are saved"
echo "2. Ensure both services are redeployed"
echo "3. Verify the GitHub OAuth callback URL is updated"
echo "4. Clear your browser cache and try again"

echo -e "\n${BLUE}📞 Need Help?${NC}"
echo "If you encounter issues, check the Render service logs for error messages." 