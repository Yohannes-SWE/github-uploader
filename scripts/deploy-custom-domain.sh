#!/bin/bash

# Custom Domain Deployment Script for repotorpedo.com
# This script automates deployment with custom domain configuration

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Domain configuration
FRONTEND_DOMAIN="repotorpedo.com"
BACKEND_DOMAIN="api.repotorpedo.com"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to validate environment variables
validate_custom_domain_env() {
    print_status "Validating custom domain environment variables..."
    
    required_vars=(
        "GITHUB_CLIENT_ID"
        "GITHUB_CLIENT_SECRET"
        "OPENAI_API_KEY"
        "SECRET_KEY"
    )
    
    missing_vars=()
    
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            missing_vars+=("$var")
        fi
    done
    
    if [ ${#missing_vars[@]} -ne 0 ]; then
        print_error "Missing required environment variables:"
        for var in "${missing_vars[@]}"; do
            echo "  - $var"
        done
        exit 1
    fi
    
    print_success "All required environment variables are set"
}

# Function to check DNS configuration
check_dns_configuration() {
    print_status "Checking DNS configuration for $FRONTEND_DOMAIN and $BACKEND_DOMAIN..."
    
    # Check if domains resolve
    if nslookup $FRONTEND_DOMAIN > /dev/null 2>&1; then
        print_success "$FRONTEND_DOMAIN resolves correctly"
    else
        print_warning "$FRONTEND_DOMAIN does not resolve yet (DNS propagation may take time)"
    fi
    
    if nslookup $BACKEND_DOMAIN > /dev/null 2>&1; then
        print_success "$BACKEND_DOMAIN resolves correctly"
    else
        print_warning "$BACKEND_DOMAIN does not resolve yet (DNS propagation may take time)"
    fi
}

# Function to generate production environment file
generate_production_env() {
    print_status "Generating production environment configuration..."
    
    cat > .env.production << EOF
# Production Environment for repotorpedo.com
ENVIRONMENT=production

# GitHub OAuth
GITHUB_CLIENT_ID=$GITHUB_CLIENT_ID
GITHUB_CLIENT_SECRET=$GITHUB_CLIENT_SECRET

# OpenAI API
OPENAI_API_KEY=$OPENAI_API_KEY

# Security
SECRET_KEY=$SECRET_KEY

# Custom Domain URLs
BASE_URL=https://$BACKEND_DOMAIN
FRONTEND_URL=https://$FRONTEND_DOMAIN
GITHUB_CALLBACK_URL=https://$BACKEND_DOMAIN/api/auth/github/callback
ALLOWED_ORIGINS=https://$FRONTEND_DOMAIN,https://www.$FRONTEND_DOMAIN
EOF

    print_success "Production environment file created: .env.production"
}

# Function to deploy to Render
deploy_render() {
    print_status "Deploying to Render with custom domain configuration..."
    
    # Check if render CLI is installed
    if ! command -v render > /dev/null 2>&1; then
        print_warning "Render CLI not found. Please deploy manually:"
        echo ""
        echo "1. Go to https://render.com"
        echo "2. Create new Web Service for backend:"
        echo "   - Name: repotorpedo-backend"
        echo "   - Root Directory: server"
        echo "   - Build Command: pip install -r requirements.txt"
        echo "   - Start Command: uvicorn main:app --host 0.0.0.0 --port \$PORT"
        echo ""
        echo "3. Create new Static Site for frontend:"
        echo "   - Name: repotorpedo-frontend"
        echo "   - Root Directory: client"
        echo "   - Build Command: npm install && npm run build"
        echo "   - Publish Directory: client/build"
        echo ""
        echo "4. Set environment variables from .env.production"
        echo "5. Configure custom domains in Render dashboard"
        return
    fi
    
    # Deploy backend
    print_status "Deploying backend..."
    render deploy --service repotorpedo-backend
    
    # Deploy frontend
    print_status "Deploying frontend..."
    render deploy --service repotorpedo-frontend
    
    print_success "Render deployment completed"
}

# Function to deploy to Railway
deploy_railway() {
    print_status "Deploying to Railway with custom domain configuration..."
    
    # Check if Railway CLI is installed
    if ! command -v railway > /dev/null 2>&1; then
        print_warning "Railway CLI not found. Please deploy manually:"
        echo ""
        echo "1. Go to https://railway.app"
        echo "2. Deploy your repository"
        echo "3. Set environment variables from .env.production"
        echo "4. Configure custom domain: $BACKEND_DOMAIN"
        return
    fi
    
    # Deploy backend
    print_status "Deploying backend to Railway..."
    railway up
    
    print_success "Railway deployment completed"
}

# Function to deploy to Vercel
deploy_vercel() {
    print_status "Deploying to Vercel with custom domain configuration..."
    
    # Check if Vercel CLI is installed
    if ! command -v vercel > /dev/null 2>&1; then
        print_warning "Vercel CLI not found. Please deploy manually:"
        echo ""
        echo "1. Go to https://vercel.com"
        echo "2. Import your repository"
        echo "3. Configure:"
        echo "   - Framework Preset: Create React App"
        echo "   - Root Directory: client"
        echo "   - Build Command: npm run build"
        echo "   - Output Directory: build"
        echo "4. Set environment variables from .env.production"
        echo "5. Configure custom domain: $FRONTEND_DOMAIN"
        return
    fi
    
    # Deploy frontend
    print_status "Deploying frontend to Vercel..."
    cd client
    vercel --prod
    cd ..
    
    print_success "Vercel deployment completed"
}

# Function to test deployment
test_deployment() {
    print_status "Testing deployment..."
    
    # Test backend health
    print_status "Testing backend health endpoint..."
    if curl -f https://$BACKEND_DOMAIN/health > /dev/null 2>&1; then
        print_success "Backend health check passed"
    else
        print_warning "Backend health check failed (may still be deploying)"
    fi
    
    # Test frontend
    print_status "Testing frontend..."
    if curl -f https://$FRONTEND_DOMAIN > /dev/null 2>&1; then
        print_success "Frontend is accessible"
    else
        print_warning "Frontend is not accessible yet (may still be deploying)"
    fi
}

# Function to show DNS configuration
show_dns_config() {
    print_status "DNS Configuration for $FRONTEND_DOMAIN:"
    echo ""
    echo "For Render deployment:"
    echo "Type: CNAME"
    echo "Name: @"
    echo "Value: your-frontend-service.onrender.com"
    echo ""
    echo "Type: CNAME"
    echo "Name: api"
    echo "Value: your-backend-service.onrender.com"
    echo ""
    echo "For Railway deployment:"
    echo "Type: CNAME"
    echo "Name: @"
    echo "Value: your-frontend-service.railway.app"
    echo ""
    echo "Type: CNAME"
    echo "Name: api"
    echo "Value: your-backend-service.railway.app"
    echo ""
    echo "For Vercel deployment:"
    echo "Type: CNAME"
    echo "Name: @"
    echo "Value: cname.vercel-dns.com"
    echo ""
    echo "Type: CNAME"
    echo "Name: api"
    echo "Value: your-backend-service.railway.app"
    echo ""
}

# Function to show help
show_help() {
    echo "Custom Domain Deployment Script for repotorpedo.com"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help          Show this help message"
    echo "  -r, --render        Deploy to Render"
    echo "  -l, --railway       Deploy to Railway"
    echo "  -v, --vercel        Deploy to Vercel"
    echo "  -d, --dns           Show DNS configuration"
    echo "  -t, --test          Test deployment"
    echo "  -a, --all           Deploy to all platforms"
    echo ""
    echo "Environment Variables:"
    echo "  GITHUB_CLIENT_ID      GitHub OAuth Client ID"
    echo "  GITHUB_CLIENT_SECRET  GitHub OAuth Client Secret"
    echo "  OPENAI_API_KEY        OpenAI API Key"
    echo "  SECRET_KEY            Application Secret Key"
    echo ""
    echo "Examples:"
    echo "  $0 --render           Deploy to Render"
    echo "  $0 --dns              Show DNS configuration"
    echo "  $0 --test             Test deployment"
}

# Main script logic
main() {
    # Parse command line arguments
    RENDER_DEPLOY=false
    RAILWAY_DEPLOY=false
    VERCEL_DEPLOY=false
    SHOW_DNS=false
    TEST_DEPLOY=false
    ALL_PLATFORMS=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -r|--render)
                RENDER_DEPLOY=true
                shift
                ;;
            -l|--railway)
                RAILWAY_DEPLOY=true
                shift
                ;;
            -v|--vercel)
                VERCEL_DEPLOY=true
                shift
                ;;
            -d|--dns)
                SHOW_DNS=true
                shift
                ;;
            -t|--test)
                TEST_DEPLOY=true
                shift
                ;;
            -a|--all)
                ALL_PLATFORMS=true
                shift
                ;;
            *)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Welcome message
    echo ""
    print_status "🚀 Custom Domain Deployment for repotorpedo.com"
    echo ""
    
    # Validate environment variables
    validate_custom_domain_env
    
    # Generate production environment file
    generate_production_env
    
    # Show DNS configuration if requested
    if [ "$SHOW_DNS" = true ]; then
        show_dns_config
        exit 0
    fi
    
    # Check DNS configuration
    check_dns_configuration
    
    # Deploy based on options
    if [ "$RENDER_DEPLOY" = true ] || [ "$ALL_PLATFORMS" = true ]; then
        deploy_render
    fi
    
    if [ "$RAILWAY_DEPLOY" = true ] || [ "$ALL_PLATFORMS" = true ]; then
        deploy_railway
    fi
    
    if [ "$VERCEL_DEPLOY" = true ] || [ "$ALL_PLATFORMS" = true ]; then
        deploy_vercel
    fi
    
    # Test deployment if requested
    if [ "$TEST_DEPLOY" = true ]; then
        test_deployment
    fi
    
    print_success "Custom domain deployment process completed! 🎉"
    echo ""
    print_status "Your app will be available at:"
    echo "  Frontend: https://$FRONTEND_DOMAIN"
    echo "  Backend:  https://$BACKEND_DOMAIN"
    echo ""
    print_status "Remember to:"
    echo "  1. Configure DNS records in Squarespace"
    echo "  2. Update GitHub OAuth app callback URL"
    echo "  3. Wait for DNS propagation (up to 48 hours)"
}

# Run main function with all arguments
main "$@" 