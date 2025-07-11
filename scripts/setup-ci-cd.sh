#!/bin/bash

# CI/CD Setup Script for GitHub Uploader
# This script helps you set up automated deployment

echo "🚀 Setting up CI/CD for GitHub Uploader"
echo "========================================"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository. Please run this from the project root."
    exit 1
fi

echo ""
echo "📋 Available CI/CD Platforms:"
echo "1. Render (Recommended - Free)"
echo "2. Railway (Free tier - $5 credit/month)"
echo "3. Vercel (Frontend only - Free)"
echo "4. All platforms"

read -p "Select platform (1-4): " platform_choice

case $platform_choice in
    1)
        setup_render
        ;;
    2)
        setup_railway
        ;;
    3)
        setup_vercel
        ;;
    4)
        setup_all
        ;;
    *)
        echo "❌ Invalid choice. Exiting."
        exit 1
        ;;
esac

setup_render() {
    echo ""
    echo "🎯 Setting up Render CI/CD..."
    echo ""
    echo "📝 Steps to complete:"
    echo "1. Go to https://render.com and create an account"
    echo "2. Connect your GitHub repository"
    echo "3. Create a new Web Service for the backend:"
    echo "   - Name: github-uploader-backend"
    echo "   - Environment: Python 3"
    echo "   - Build Command: pip install -r requirements.txt"
    echo "   - Start Command: uvicorn main:app --host 0.0.0.0 --port \$PORT"
    echo "   - Root Directory: server"
    echo ""
    echo "4. Create a new Static Site for the frontend:"
    echo "   - Name: github-uploader-frontend"
    echo "   - Build Command: npm install && npm run build"
    echo "   - Publish Directory: client/build"
    echo "   - Root Directory: client"
    echo ""
    echo "5. Get your Render API token and service ID"
    echo "6. Add these GitHub secrets:"
    echo "   - RENDER_TOKEN"
    echo "   - RENDER_SERVICE_ID"
    echo ""
    echo "✅ Render setup instructions completed!"
}

setup_railway() {
    echo ""
    echo "🚂 Setting up Railway CI/CD..."
    echo ""
    echo "📝 Steps to complete:"
    echo "1. Go to https://railway.app and create an account"
    echo "2. Connect your GitHub repository"
    echo "3. Deploy your project"
    echo "4. Get your Railway token from Settings > Tokens"
    echo "5. Add this GitHub secret:"
    echo "   - RAILWAY_TOKEN"
    echo ""
    echo "✅ Railway setup instructions completed!"
}

setup_vercel() {
    echo ""
    echo "⚡ Setting up Vercel CI/CD..."
    echo ""
    echo "📝 Steps to complete:"
    echo "1. Go to https://vercel.com and create an account"
    echo "2. Import your GitHub repository"
    echo "3. Configure the project:"
    echo "   - Framework Preset: Create React App"
    echo "   - Root Directory: client"
    echo "4. Get your Vercel tokens from Settings > Tokens"
    echo "5. Add these GitHub secrets:"
    echo "   - VERCEL_TOKEN"
    echo "   - VERCEL_ORG_ID"
    echo "   - VERCEL_PROJECT_ID"
    echo ""
    echo "✅ Vercel setup instructions completed!"
}

setup_all() {
    echo ""
    echo "🌐 Setting up all CI/CD platforms..."
    setup_render
    setup_railway
    setup_vercel
}

echo ""
echo "🎉 CI/CD setup complete!"
echo ""
echo "📚 Next steps:"
echo "1. Push your code to GitHub"
echo "2. Set up the platform(s) you chose"
echo "3. Add the required secrets to your GitHub repository"
echo "4. Watch the GitHub Actions run automatically!"
echo ""
echo "📖 For detailed instructions, see DEPLOYMENT.md" 