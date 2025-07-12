#!/bin/bash

# Example: Universal Render Deployment
# This script demonstrates how to deploy different types of applications to Render

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 Universal Render Deployment Examples${NC}"
echo "=========================================="
echo ""

# Check if script exists
if [ ! -f "../scripts/universal-render-deploy.sh" ]; then
    echo -e "${YELLOW}❌ Universal deployment script not found${NC}"
    echo "Please run this from the examples directory"
    exit 1
fi

# Example 1: Deploy a React frontend
echo -e "${GREEN}Example 1: Deploying React Frontend${NC}"
echo "----------------------------------------"
echo "Repository: facebook/create-react-app"
echo "Type: React (Frontend only)"
echo ""

# Uncomment to run (requires API key)
# ../scripts/universal-render-deploy.sh \
#     -k "your-render-api-key" \
#     -r "facebook/create-react-app" \
#     -n "my-react-demo" \
#     -e "REACT_APP_ENVIRONMENT=production"

echo "Expected result:"
echo "  Frontend: https://my-react-demo-frontend.onrender.com"
echo ""

# Example 2: Deploy a Python FastAPI backend
echo -e "${GREEN}Example 2: Deploying Python FastAPI Backend${NC}"
echo "--------------------------------------------"
echo "Repository: tiangolo/fastapi"
echo "Type: Python (Backend only)"
echo ""

# Uncomment to run (requires API key)
# ../scripts/universal-render-deploy.sh \
#     -k "your-render-api-key" \
#     -r "tiangolo/fastapi" \
#     -n "my-fastapi-demo" \
#     -e "ENVIRONMENT=production" \
#     -e "DATABASE_URL=postgresql://..."

echo "Expected result:"
echo "  Backend: https://my-fastapi-demo-backend.onrender.com"
echo ""

# Example 3: Deploy a full-stack application
echo -e "${GREEN}Example 3: Deploying Full-Stack Application${NC}"
echo "----------------------------------------"
echo "Repository: your-username/your-fullstack-app"
echo "Type: React + Node.js (Full-stack)"
echo ""

# Uncomment to run (requires API key and your repo)
# ../scripts/universal-render-deploy.sh \
#     -k "your-render-api-key" \
#     -r "your-username/your-fullstack-app" \
#     -n "my-fullstack-app" \
#     -e "NODE_ENV=production" \
#     -e "DATABASE_URL=postgresql://..." \
#     -e "JWT_SECRET=your-secret-key"

echo "Expected result:"
echo "  Backend: https://my-fullstack-app-backend.onrender.com"
echo "  Frontend: https://my-fullstack-app-frontend.onrender.com"
echo ""

# Example 4: Deploy with environment file
echo -e "${GREEN}Example 4: Deploying with Environment File${NC}"
echo "----------------------------------------"
echo "Repository: your-username/your-app"
echo "Type: Any application"
echo ""

# Create example environment file
cat > .env.example << EOF
# Production environment variables
NODE_ENV=production
DATABASE_URL=postgresql://user:pass@host:port/db
JWT_SECRET=your-super-secret-jwt-key
API_KEY=your-external-api-key
REDIS_URL=redis://localhost:6379
EOF

echo "Created .env.example file with sample variables"
echo ""

# Uncomment to run (requires API key and your repo)
# ../scripts/universal-render-deploy.sh \
#     -k "your-render-api-key" \
#     -r "your-username/your-app" \
#     -n "my-app-with-env" \
#     -f ".env.example"

echo "Expected result:"
echo "  Application deployed with all environment variables set"
echo ""

# Example 5: Deploy a static website
echo -e "${GREEN}Example 5: Deploying Static Website${NC}"
echo "----------------------------------------"
echo "Repository: your-username/portfolio"
echo "Type: Static HTML/CSS/JS"
echo ""

# Uncomment to run (requires API key and your repo)
# ../scripts/universal-render-deploy.sh \
#     -k "your-render-api-key" \
#     -r "your-username/portfolio" \
#     -n "my-portfolio"

echo "Expected result:"
echo "  Frontend: https://my-portfolio-frontend.onrender.com"
echo ""

echo -e "${BLUE}📋 How to Use These Examples${NC}"
echo "================================"
echo ""
echo "1. Get your Render API key from:"
echo "   https://dashboard.render.com/account/api-keys"
echo ""
echo "2. Replace 'your-render-api-key' with your actual API key"
echo ""
echo "3. Replace repository URLs with your own repositories"
echo ""
echo "4. Uncomment the deployment commands you want to run"
echo ""
echo "5. Run the script:"
echo "   ./deploy-example.sh"
echo ""
echo -e "${YELLOW}⚠️  Important Notes:${NC}"
echo "- Make sure your repositories are public, or Render has access to them"
echo "- Test with small repositories first"
echo "- Monitor deployment progress in Render dashboard"
echo "- Check build logs if deployment fails"
echo ""
echo -e "${GREEN}🎉 Happy Deploying!${NC}" 