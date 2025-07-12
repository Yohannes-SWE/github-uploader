#!/bin/bash

# Render Environment Variables Commands
# This script provides the exact steps to fix production environment variables

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔧 Render Environment Variables Fix${NC}"
echo "====================================="

echo -e "\n${YELLOW}Your Render Services:${NC}"
echo "====================="
echo "Backend:  srv-d1ojvk7diees73cja4e0 (repotorpedo-backend)"
echo "Frontend: srv-d1ojehruibrs73cs3g40 (repotorpedo-frontend)"

echo -e "\n${RED}🚨 OAuth 404 Error Fix Required${NC}"
echo "====================================="
echo "The OAuth callback URL is pointing to localhost instead of production."
echo "This is causing the login to fail with a 404 error."

echo -e "\n${YELLOW}📋 Method 1: Web Interface (Recommended)${NC}"
echo "============================================="
echo "1. Go to: https://dashboard.render.com"
echo "2. Click on 'repotorpedo-backend' service"
echo "3. Go to 'Environment' tab"
echo "4. Click 'Environment Variables'"
echo "5. Update these variables:"
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
echo ""
echo "6. Click 'Save Changes'"
echo "7. Go to 'Manual Deploy' tab"
echo "8. Click 'Deploy latest commit'"

echo -e "\n${YELLOW}📋 Method 2: Direct Service Management${NC}"
echo "============================================="
echo "You can also manage services directly:"
echo ""
echo "1. List services:"
echo "   render services --output text"
echo ""
echo "2. View service details:"
echo "   render services"
echo "   (Then select your service in interactive mode)"
echo ""
echo "3. Redeploy services:"
echo "   render deploys create --service-id srv-d1ojvk7diees73cja4e0"
echo "   render deploys create --service-id srv-d1ojehruibrs73cs3g40"

echo -e "\n${YELLOW}📋 Method 3: GitHub OAuth App Update${NC}"
echo "============================================="
echo "1. Go to: https://github.com/settings/developers"
echo "2. Find your OAuth App"
echo "3. Click 'Edit'"
echo "4. Update 'Authorization callback URL' to:"
echo -e "${GREEN}https://repotorpedo-backend.onrender.com/api/auth/github/callback${NC}"
echo "5. Click 'Update application'"

echo -e "\n${YELLOW}🔍 Verification Steps:${NC}"
echo "======================="
echo "After making changes, test with:"
echo ""
echo "1. Check OAuth redirect:"
echo "   curl -I https://repotorpedo-backend.onrender.com/api/auth/github/login"
echo ""
echo "2. Test frontend:"
echo "   https://repotorpedo-frontend.onrender.com"
echo ""
echo "3. Run verification script:"
echo "   ./scripts/verify-production-fix.sh"

echo -e "\n${GREEN}✅ Expected Result:${NC}"
echo "The OAuth login should now work without 404 errors!"

echo -e "\n${BLUE}💡 Quick Commands:${NC}"
echo "=================="
echo "Open Render Dashboard: open https://dashboard.render.com"
echo "Open GitHub OAuth: open https://github.com/settings/developers"
echo "Test Frontend: open https://repotorpedo-frontend.onrender.com" 