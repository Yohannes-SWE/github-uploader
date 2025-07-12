#!/bin/bash

# Production OAuth Fix Verification Script
# This script verifies that the OAuth 404 error has been fixed

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔍 Production OAuth Fix Verification${NC}"
echo "====================================="

echo -e "\n${YELLOW}Testing Backend Health:${NC}"
echo "========================"

# Test backend health
if curl -s -f https://repotorpedo-backend.onrender.com/api/auth/status > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend is responding${NC}"
else
    echo -e "${RED}❌ Backend is not responding${NC}"
    exit 1
fi

echo -e "\n${YELLOW}Testing OAuth Login Redirect:${NC}"
echo "============================="

# Test OAuth login redirect
OAUTH_RESPONSE=$(curl -s -I https://repotorpedo-backend.onrender.com/api/auth/github/login 2>/dev/null | grep -i "location" || echo "")

if echo "$OAUTH_RESPONSE" | grep -q "github.com"; then
    echo -e "${GREEN}✅ OAuth redirect is working${NC}"
    
    # Check if callback URL is correct
    if echo "$OAUTH_RESPONSE" | grep -q "repotorpedo-backend.onrender.com"; then
        echo -e "${GREEN}✅ Callback URL is pointing to production${NC}"
    else
        echo -e "${RED}❌ Callback URL is still pointing to localhost${NC}"
        echo "   Current redirect: $OAUTH_RESPONSE"
        echo -e "\n${YELLOW}You still need to update the environment variables in Render!${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ OAuth redirect is not working${NC}"
    echo "   Response: $OAUTH_RESPONSE"
    exit 1
fi

echo -e "\n${YELLOW}Testing Frontend Accessibility:${NC}"
echo "============================="

# Test frontend
if curl -s -f https://repotorpedo-frontend.onrender.com > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Frontend is accessible${NC}"
else
    echo -e "${RED}❌ Frontend is not accessible${NC}"
    exit 1
fi

echo -e "\n${GREEN}🎉 All Tests Passed!${NC}"
echo "====================="
echo "The OAuth 404 error should now be fixed."
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Go to: https://repotorpedo-frontend.onrender.com"
echo "2. Try clicking 'Login with GitHub'"
echo "3. You should be redirected to GitHub for authorization"
echo "4. After authorization, you should be redirected back to the app"

echo -e "\n${BLUE}If you still get errors:${NC}"
echo "1. Clear your browser cache"
echo "2. Try in an incognito/private window"
echo "3. Check that you've updated the GitHub OAuth app callback URL" 