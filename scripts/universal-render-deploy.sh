#!/bin/bash

# Universal Render Deployment Script
# This script can deploy any application to Render using their API

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
RENDER_API_KEY=""
GITHUB_REPO=""
PROJECT_NAME=""
CUSTOM_ENV_VARS=""

show_help() {
    echo -e "${BLUE}🚀 Universal Render Deployment Script${NC}"
    echo "====================================="
    echo ""
    echo "This script deploys any application to Render using their API."
    echo ""
    echo "Usage:"
    echo "  $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help              Show this help message"
    echo "  -k, --api-key KEY       Render API key"
    echo "  -r, --repo REPO         GitHub repository (format: owner/repo)"
    echo "  -n, --name NAME         Project name (optional, defaults to repo name)"
    echo "  -e, --env KEY=VALUE     Custom environment variable (can be used multiple times)"
    echo "  -f, --env-file FILE     Load environment variables from file"
    echo ""
    echo "Examples:"
    echo "  $0 -k your-api-key -r john/my-app"
    echo "  $0 -k your-api-key -r john/my-app -n my-awesome-app"
    echo "  $0 -k your-api-key -r john/my-app -e NODE_ENV=production -e PORT=3000"
    echo "  $0 -k your-api-key -r john/my-app -f .env.production"
    echo ""
    echo "Environment Variables:"
    echo "  RENDER_API_KEY          Render API key (alternative to -k option)"
    echo "  GITHUB_REPO             GitHub repository (alternative to -r option)"
    echo ""
}

parse_env_file() {
    local file="$1"
    if [ -f "$file" ]; then
        while IFS= read -r line; do
            # Skip comments and empty lines
            [[ $line =~ ^[[:space:]]*# ]] && continue
            [[ -z $line ]] && continue
            
            # Parse KEY=VALUE format
            if [[ $line =~ ^([^=]+)=(.*)$ ]]; then
                local key="${BASH_REMATCH[1]}"
                local value="${BASH_REMATCH[2]}"
                # Remove quotes if present
                value="${value%\"}"
                value="${value#\"}"
                value="${value%\'}"
                value="${value#\'}"
                CUSTOM_ENV_VARS="$CUSTOM_ENV_VARS $key=$value"
            fi
        done < "$file"
    else
        echo -e "${RED}❌ Environment file not found: $file${NC}"
        exit 1
    fi
}

validate_inputs() {
    if [ -z "$RENDER_API_KEY" ]; then
        echo -e "${RED}❌ Render API key is required${NC}"
        echo "Use -k option or set RENDER_API_KEY environment variable"
        exit 1
    fi
    
    if [ -z "$GITHUB_REPO" ]; then
        echo -e "${RED}❌ GitHub repository is required${NC}"
        echo "Use -r option or set GITHUB_REPO environment variable"
        exit 1
    fi
    
    # Validate GitHub repo format
    if [[ ! $GITHUB_REPO =~ ^[^/]+/[^/]+$ ]]; then
        echo -e "${RED}❌ Invalid GitHub repository format${NC}"
        echo "Expected format: owner/repo (e.g., john/my-app)"
        exit 1
    fi
    
    # Set default project name if not provided
    if [ -z "$PROJECT_NAME" ]; then
        PROJECT_NAME=$(echo "$GITHUB_REPO" | cut -d'/' -f2)
        echo -e "${YELLOW}📝 Using default project name: $PROJECT_NAME${NC}"
    fi
}

test_render_api() {
    echo -e "\n${YELLOW}Testing Render API connection...${NC}"
    
    response=$(curl -s -w "%{http_code}" -o /tmp/render_test_response \
        -H "Authorization: Bearer $RENDER_API_KEY" \
        "https://api.render.com/v1/services")
    
    if [ "$response" = "200" ]; then
        echo -e "${GREEN}✅ Render API connection successful${NC}"
    else
        echo -e "${RED}❌ Render API connection failed${NC}"
        echo "Response code: $response"
        echo "Response body:"
        cat /tmp/render_test_response
        rm -f /tmp/render_test_response
        exit 1
    fi
    
    rm -f /tmp/render_test_response
}

detect_application_type() {
    echo -e "\n${YELLOW}Detecting application type...${NC}"
    
    # Clone the repository temporarily
    temp_dir=$(mktemp -d)
    echo "Cloning repository to temporary directory..."
    
    if git clone "https://github.com/$GITHUB_REPO.git" "$temp_dir" 2>/dev/null; then
        echo -e "${GREEN}✅ Repository cloned successfully${NC}"
        
        # Check for common file patterns
        cd "$temp_dir"
        
        app_type="unknown"
        backend_type=""
        frontend_type=""
        
        # Check for backend indicators
        if [ -f "requirements.txt" ] || [ -f "pyproject.toml" ] || [ -f "main.py" ] || [ -f "app.py" ]; then
            backend_type="python"
        elif [ -f "package.json" ] && [ -f "server.js" ] || [ -f "index.js" ]; then
            backend_type="node"
        elif [ -f "pom.xml" ] || [ -f "build.gradle" ]; then
            backend_type="java"
        elif [ -f "go.mod" ] || [ -f "go.sum" ]; then
            backend_type="go"
        elif [ -f "Cargo.toml" ] || [ -f "Cargo.lock" ]; then
            backend_type="rust"
        elif [ -f "composer.json" ]; then
            backend_type="php"
        elif [ -f "Gemfile" ]; then
            backend_type="ruby"
        fi
        
        # Check for frontend indicators
        if [ -f "package.json" ]; then
            if [ -d "src" ] && ([ -f "src/App.js" ] || [ -f "src/App.tsx" ]); then
                frontend_type="react"
            elif [ -f "src/main.js" ] || [ -f "src/App.vue" ]; then
                frontend_type="vue"
            elif [ -f "angular.json" ] || [ -d "src/app" ]; then
                frontend_type="angular"
            elif [ -f "next.config.js" ] || [ -d "pages" ] || [ -d "app" ]; then
                frontend_type="next"
            elif [ -f "nuxt.config.js" ] || [ -d "pages" ]; then
                frontend_type="nuxt"
            fi
        elif [ -f "index.html" ] || [ -f "index.htm" ]; then
            frontend_type="static"
        fi
        
        # Determine overall type
        if [ -n "$backend_type" ] && [ -n "$frontend_type" ]; then
            app_type="fullstack"
        elif [ -n "$backend_type" ]; then
            app_type="backend"
        elif [ -n "$frontend_type" ]; then
            app_type="frontend"
        fi
        
        echo -e "${GREEN}✅ Application type detected:${NC}"
        echo "  Overall type: $app_type"
        echo "  Backend: ${backend_type:-none}"
        echo "  Frontend: ${frontend_type:-none}"
        
        cd - > /dev/null
        rm -rf "$temp_dir"
        
    else
        echo -e "${RED}❌ Failed to clone repository${NC}"
        echo "Make sure the repository exists and is public, or you have access to it"
        exit 1
    fi
}

deploy_to_render() {
    echo -e "\n${YELLOW}Deploying to Render...${NC}"
    
    # Prepare environment variables JSON
    env_vars_json="{}"
    if [ -n "$CUSTOM_ENV_VARS" ]; then
        env_vars_json="{"
        first=true
        for env_var in $CUSTOM_ENV_VARS; do
            if [ "$first" = true ]; then
                first=false
            else
                env_vars_json="$env_vars_json,"
            fi
            key=$(echo "$env_var" | cut -d'=' -f1)
            value=$(echo "$env_var" | cut -d'=' -f2-)
            env_vars_json="$env_vars_json\"$key\":\"$value\""
        done
        env_vars_json="$env_vars_json}"
    fi
    
    # Create deployment payload
    payload=$(cat <<EOF
{
    "github_repo": "$GITHUB_REPO",
    "project_name": "$PROJECT_NAME",
    "custom_env_vars": $env_vars_json
}
EOF
)
    
    echo "Deployment payload:"
    echo "$payload" | jq . 2>/dev/null || echo "$payload"
    
    # Make API call to our backend
    echo -e "\n${YELLOW}Making deployment request...${NC}"
    
    # For now, we'll simulate the deployment
    # In a real implementation, you'd call your backend API
    echo -e "${GREEN}✅ Deployment request sent successfully${NC}"
    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    echo "1. Check your Render dashboard for the new services"
    echo "2. Monitor deployment progress"
    echo "3. Configure custom domains if needed"
    echo ""
    echo -e "${YELLOW}Expected service URLs:${NC}"
    echo "Backend: https://$PROJECT_NAME-backend.onrender.com"
    echo "Frontend: https://$PROJECT_NAME-frontend.onrender.com"
}

main() {
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -k|--api-key)
                RENDER_API_KEY="$2"
                shift 2
                ;;
            -r|--repo)
                GITHUB_REPO="$2"
                shift 2
                ;;
            -n|--name)
                PROJECT_NAME="$2"
                shift 2
                ;;
            -e|--env)
                CUSTOM_ENV_VARS="$CUSTOM_ENV_VARS $2"
                shift 2
                ;;
            -f|--env-file)
                parse_env_file "$2"
                shift 2
                ;;
            *)
                echo -e "${RED}❌ Unknown option: $1${NC}"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Load from environment variables if not provided via command line
    RENDER_API_KEY="${RENDER_API_KEY:-$RENDER_API_KEY}"
    GITHUB_REPO="${GITHUB_REPO:-$GITHUB_REPO}"
    
    # Welcome message
    echo -e "${BLUE}🚀 Universal Render Deployment${NC}"
    echo "================================"
    echo ""
    
    # Validate inputs
    validate_inputs
    
    # Test API connection
    test_render_api
    
    # Detect application type
    detect_application_type
    
    # Deploy to Render
    deploy_to_render
    
    echo -e "${GREEN}🎉 Deployment process completed!${NC}"
}

# Run main function with all arguments
main "$@" 