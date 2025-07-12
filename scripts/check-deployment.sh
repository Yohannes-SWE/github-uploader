#!/bin/bash

# Check deployment status for repotorpedo.com
echo "🔍 Checking deployment status..."

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Backend check
echo -e "\n${YELLOW}Backend (repotorpedo-backend.onrender.com):${NC}"
if curl -s -f https://repotorpedo-backend.onrender.com/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend is healthy${NC}"
    curl -s https://repotorpedo-backend.onrender.com/health | jq . 2>/dev/null || curl -s https://repotorpedo-backend.onrender.com/health
else
    echo -e "${RED}❌ Backend is not responding${NC}"
    echo "   Status code: $(curl -s -o /dev/null -w "%{http_code}" https://repotorpedo-backend.onrender.com/health)"
fi

# Frontend check
echo -e "\n${YELLOW}Frontend (repotorpedo-frontend.onrender.com):${NC}"
if curl -s -f https://repotorpedo-frontend.onrender.com > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Frontend is accessible${NC}"
else
    echo -e "${RED}❌ Frontend is not accessible${NC}"
    echo "   Status code: $(curl -s -o /dev/null -w "%{http_code}" https://repotorpedo-frontend.onrender.com)"
fi

# API endpoint check
echo -e "\n${YELLOW}API Endpoint Test:${NC}"
if curl -s -f https://repotorpedo-backend.onrender.com/api/auth/status > /dev/null 2>&1; then
    echo -e "${GREEN}✅ API endpoint is working${NC}"
else
    echo -e "${RED}❌ API endpoint is not working${NC}"
    echo "   Status code: $(curl -s -o /dev/null -w "%{http_code}" https://repotorpedo-backend.onrender.com/api/auth/status)"
fi

echo -e "\n${YELLOW}Next Steps:${NC}"
echo "1. Check Render dashboard for deployment status"
echo "2. Verify environment variables are set correctly"
echo "3. Check service logs for errors"
echo "4. Redeploy if necessary" 