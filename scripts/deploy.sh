#!/bin/bash

# GitHub Uploader Production Deployment Script
# This script automates the deployment process for production environments

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to validate environment variables
validate_env_vars() {
    print_status "Validating environment variables..."
    
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

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check Python
    if ! command_exists python; then
        print_error "Python is not installed"
        exit 1
    fi
    
    # Check Node.js
    if ! command_exists node; then
        print_error "Node.js is not installed"
        exit 1
    fi
    
    # Check npm
    if ! command_exists npm; then
        print_error "npm is not installed"
        exit 1
    fi
    
    # Check git
    if ! command_exists git; then
        print_error "git is not installed"
        exit 1
    fi
    
    print_success "All prerequisites are installed"
}

# Function to build backend
build_backend() {
    print_status "Building backend..."
    
    cd server
    
    # Install Python dependencies
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        python -m venv venv
    fi
    
    source venv/bin/activate
    
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    
    # Test backend
    print_status "Testing backend..."
    python -c "import fastapi; print('Backend dependencies OK')"
    
    cd ..
    print_success "Backend build completed"
}

# Function to build frontend
build_frontend() {
    print_status "Building frontend..."
    
    cd client
    
    # Install Node.js dependencies
    print_status "Installing Node.js dependencies..."
    npm install
    
    # Build for production
    print_status "Building for production..."
    npm run build
    
    # Check if build was successful
    if [ ! -d "build" ]; then
        print_error "Frontend build failed - build directory not found"
        exit 1
    fi
    
    cd ..
    print_success "Frontend build completed"
}

# Function to test application
test_application() {
    print_status "Testing application..."
    
    # Test backend health endpoint
    print_status "Testing backend health endpoint..."
    cd server
    source venv/bin/activate
    
    # Start backend in background
    python -m uvicorn main:app --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
    
    # Wait for backend to start
    sleep 5
    
    # Test health endpoint
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_success "Backend health check passed"
    else
        print_error "Backend health check failed"
        kill $BACKEND_PID 2>/dev/null || true
        exit 1
    fi
    
    # Stop backend
    kill $BACKEND_PID 2>/dev/null || true
    
    cd ..
    print_success "Application testing completed"
}

# Function to deploy to Render
deploy_render() {
    print_status "Deploying to Render..."
    
    # Check if render CLI is installed
    if ! command_exists render; then
        print_warning "Render CLI not found. Please deploy manually:"
        echo "1. Go to https://render.com"
        echo "2. Connect your GitHub repository"
        echo "3. Deploy backend and frontend services"
        echo "4. Set environment variables"
        return
    fi
    
    # Deploy using render CLI
    print_status "Deploying backend..."
    render deploy --service github-uploader-backend
    
    print_status "Deploying frontend..."
    render deploy --service github-uploader-frontend
    
    print_success "Render deployment completed"
}

# Function to deploy with Docker
deploy_docker() {
    print_status "Deploying with Docker..."
    
    # Check if Docker is installed
    if ! command_exists docker; then
        print_error "Docker is not installed"
        exit 1
    fi
    
    if ! command_exists docker-compose; then
        print_error "Docker Compose is not installed"
        exit 1
    fi
    
    # Build and start services
    print_status "Building Docker images..."
    docker-compose -f docker-compose.prod.yml build
    
    print_status "Starting services..."
    docker-compose -f docker-compose.prod.yml up -d
    
    # Wait for services to be ready
    print_status "Waiting for services to be ready..."
    sleep 10
    
    # Check health
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_success "Backend is healthy"
    else
        print_error "Backend health check failed"
        exit 1
    fi
    
    if curl -f http://localhost:3000 > /dev/null 2>&1; then
        print_success "Frontend is accessible"
    else
        print_error "Frontend is not accessible"
        exit 1
    fi
    
    print_success "Docker deployment completed"
}

# Function to show help
show_help() {
    echo "GitHub Uploader Production Deployment Script"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help          Show this help message"
    echo "  -t, --test          Run tests only"
    echo "  -b, --build         Build only"
    echo "  -d, --docker        Deploy with Docker"
    echo "  -r, --render        Deploy to Render"
    echo "  -a, --all           Full deployment (build, test, deploy)"
    echo ""
    echo "Environment Variables:"
    echo "  GITHUB_CLIENT_ID      GitHub OAuth Client ID"
    echo "  GITHUB_CLIENT_SECRET  GitHub OAuth Client Secret"
    echo "  OPENAI_API_KEY        OpenAI API Key"
    echo "  SECRET_KEY            Application Secret Key"
    echo ""
    echo "Examples:"
    echo "  $0 --test             Run tests only"
    echo "  $0 --docker           Deploy with Docker"
    echo "  $0 --render           Deploy to Render"
    echo "  $0 --all              Full deployment"
}

# Main script logic
main() {
    # Parse command line arguments
    TEST_ONLY=false
    BUILD_ONLY=false
    DOCKER_DEPLOY=false
    RENDER_DEPLOY=false
    FULL_DEPLOY=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -t|--test)
                TEST_ONLY=true
                shift
                ;;
            -b|--build)
                BUILD_ONLY=true
                shift
                ;;
            -d|--docker)
                DOCKER_DEPLOY=true
                shift
                ;;
            -r|--render)
                RENDER_DEPLOY=true
                shift
                ;;
            -a|--all)
                FULL_DEPLOY=true
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
    print_status "🚀 GitHub Uploader Production Deployment"
    echo ""
    
    # Check prerequisites
    check_prerequisites
    
    # Validate environment variables
    validate_env_vars
    
    # Run based on options
    if [ "$TEST_ONLY" = true ]; then
        build_backend
        test_application
    elif [ "$BUILD_ONLY" = true ]; then
        build_backend
        build_frontend
    elif [ "$DOCKER_DEPLOY" = true ]; then
        build_backend
        build_frontend
        deploy_docker
    elif [ "$RENDER_DEPLOY" = true ]; then
        build_backend
        build_frontend
        deploy_render
    elif [ "$FULL_DEPLOY" = true ]; then
        build_backend
        build_frontend
        test_application
        deploy_docker
    else
        print_warning "No deployment option specified. Use --help for options."
        show_help
        exit 1
    fi
    
    print_success "Deployment process completed successfully! 🎉"
}

# Run main function with all arguments
main "$@" 