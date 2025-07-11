#!/bin/bash

# GitHub Uploader - Platform Integration Setup Script
# This script helps you set up OAuth applications for seamless platform integration

echo "🚀 GitHub Uploader - Platform Integration Setup"
echo "================================================"
echo ""
echo "This script will help you set up OAuth applications for seamless platform integration."
echo "Follow the steps below to enable automatic deployment and CI/CD setup."
echo ""

# Check if .env file exists
if [ ! -f "server/.env" ]; then
    echo "❌ No .env file found. Please copy env.example to .env first:"
    echo "   cp env.example server/.env"
    echo ""
    exit 1
fi

echo "✅ .env file found"
echo ""

# Function to add OAuth app instructions
add_oauth_instructions() {
    local platform=$1
    local name=$2
    local url=$3
    local callback_url=$4
    
    echo "📋 Setting up $name OAuth Application"
    echo "----------------------------------------"
    echo "1. Go to: $url"
    echo "2. Create a new OAuth application"
    echo "3. Set callback URL to: $callback_url"
    echo "4. Copy the Client ID and Client Secret"
    echo "5. Add them to your .env file:"
    echo ""
    echo "   ${platform^^}_CLIENT_ID=your_client_id_here"
    echo "   ${platform^^}_CLIENT_SECRET=your_client_secret_here"
    echo ""
    read -p "Press Enter when you've completed the $name setup..."
    echo ""
}

# GitHub OAuth (Required)
echo "🔑 GitHub OAuth Setup (Required)"
echo "================================"
echo "1. Go to: https://github.com/settings/developers"
echo "2. Click 'New OAuth App'"
echo "3. Fill in the details:"
echo "   - Application name: GitHub Uploader"
echo "   - Homepage URL: http://localhost:3000"
echo "   - Authorization callback URL: http://localhost:8000/auth/github/callback"
echo "4. Copy the Client ID and Client Secret"
echo "5. Add them to your .env file:"
echo ""
echo "   GITHUB_CLIENT_ID=your_github_client_id"
echo "   GITHUB_CLIENT_SECRET=your_github_client_secret"
echo ""
read -p "Press Enter when you've completed the GitHub setup..."
echo ""

# Optional platform setups
echo "🔗 Optional Platform Integrations"
echo "=================================="
echo "The following platforms can be set up for automatic deployment and CI/CD."
echo "You can skip any that you don't want to use."
echo ""

# Vercel
read -p "Do you want to set up Vercel integration? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    add_oauth_instructions "vercel" "Vercel" "https://vercel.com/account/tokens" "http://localhost:8000/platforms/callback/vercel"
fi

# Railway
read -p "Do you want to set up Railway integration? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    add_oauth_instructions "railway" "Railway" "https://railway.app/account/tokens" "http://localhost:8000/platforms/callback/railway"
fi

# Netlify
read -p "Do you want to set up Netlify integration? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    add_oauth_instructions "netlify" "Netlify" "https://app.netlify.com/user/applications" "http://localhost:8000/platforms/callback/netlify"
fi

# Heroku
read -p "Do you want to set up Heroku integration? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    add_oauth_instructions "heroku" "Heroku" "https://dashboard.heroku.com/account/applications" "http://localhost:8000/platforms/callback/heroku"
fi

# CircleCI
read -p "Do you want to set up CircleCI integration? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    add_oauth_instructions "circleci" "CircleCI" "https://circleci.com/account/api" "http://localhost:8000/platforms/callback/circleci"
fi

# Travis CI
read -p "Do you want to set up Travis CI integration? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    add_oauth_instructions "travis" "Travis CI" "https://travis-ci.com/account/preferences" "http://localhost:8000/platforms/callback/travis"
fi

echo "🎉 Platform Setup Complete!"
echo "==========================="
echo ""
echo "Next steps:"
echo "1. Start the backend: cd server && python main.py"
echo "2. Start the frontend: cd client && npm start"
echo "3. Login with GitHub"
echo "4. Go to 'Platform Connections' tab to connect your accounts"
echo "5. Upload your first project!"
echo ""
echo "For detailed instructions, see: PLATFORM_SETUP_GUIDE.md"
echo ""
echo "Happy coding! 🚀" 