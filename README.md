# GitHub Uploader - AI-Powered Project Deployment

A comprehensive web application that automates uploading projects to GitHub with AI-powered analysis, intelligent CI/CD pipeline generation, and multi-platform deployment automation.

## 🚀 Features

### Core Functionality

- **GitHub OAuth Integration**: Secure authentication with GitHub
- **Drag & Drop Upload**: Upload entire folders with ease
- **AI-Powered Analysis**: Automatic project type detection and repository naming
- **Multi-Platform CI/CD**: Support for 8 different CI/CD platforms
- **Deployment Automation**: Generate deployment configurations for 12+ platforms
- **Project Type Detection**: Auto-detect Node.js, Python, Java, Go, Rust, PHP, Ruby, and .NET projects

### Advanced Features

- **Platform Integration**: OAuth connections to deployment platforms
- **Template System**: Pre-configured templates for common project types
- **Branch Management**: Automatic branch creation and protection
- **Dependency Analysis**: AI-powered dependency detection and recommendations
- **Security Scanning**: Built-in security checks and vulnerability scanning
- **Performance Optimization**: Intelligent build and deployment optimization

## 🛠️ CI/CD Platform Support

The application supports multiple CI/CD platforms, allowing you to choose the one that best fits your workflow:

### 1. GitHub Actions

- **Best for**: GitHub-hosted projects
- **Features**: Native GitHub integration, extensive marketplace
- **File**: `.github/workflows/ci-cd.yml`

### 2. GitLab CI

- **Best for**: GitLab-hosted projects
- **Features**: Built-in container registry, comprehensive pipeline features
- **File**: `.gitlab-ci.yml`

### 3. Jenkins

- **Best for**: Self-hosted CI/CD, enterprise environments
- **Features**: Highly customizable, extensive plugin ecosystem
- **File**: `Jenkinsfile`

### 4. CircleCI

- **Best for**: Cloud-native CI/CD with Docker support
- **Features**: Parallel execution, advanced caching
- **File**: `.circleci/config.yml`

### 5. Travis CI

- **Best for**: Open source projects, simple configurations
- **Features**: Easy setup, GitHub integration
- **File**: `.travis.yml`

### 6. Azure DevOps

- **Best for**: Microsoft ecosystem, enterprise teams
- **Features**: Full DevOps platform, Azure integration
- **File**: `azure-pipelines.yml`

### 7. Drone CI

- **Best for**: Self-hosted, container-native CI/CD
- **Features**: Simple YAML configuration, Docker-native
- **File**: `.drone.yml`

### 8. Woodpecker CI

- **Best for**: Self-hosted, lightweight CI/CD
- **Features**: Simple setup, GitHub Actions compatible syntax
- **File**: `.woodpecker.yml`

## 🌐 Deployment Platform Support

Each CI/CD configuration can be customized for deployment to:

- **Vercel** - Frontend hosting with edge functions
- **Railway** - Full-stack hosting with database support
- **Netlify** - Static site hosting with serverless functions
- **Heroku** - Platform-as-a-Service with add-ons
- **AWS** - Cloud infrastructure (EC2, Lambda, S3)
- **Google Cloud Platform** - Cloud services (App Engine, Cloud Run)
- **Microsoft Azure** - Cloud platform (App Service, Functions)
- **DigitalOcean** - VPS hosting with managed databases
- **Render** - Modern cloud platform with auto-scaling
- **Fly.io** - Global edge deployment with low latency
- **Custom Scripts** - Custom deployment logic and scripts

## 🔄 How It Works

### 1. Authentication

- Login with GitHub OAuth to get secure access
- Automatic token management and refresh
- Secure credential storage

### 2. Upload & Analysis

- Drag and drop your project folder or use the folder selector
- AI analyzes your project structure and suggests:
  - Repository name (based on folder name and content)
  - Project type (Node.js, Python, Java, etc.)
  - Dependencies and requirements
  - Recommended CI/CD platform
  - Deployment strategy

### 3. Configuration

- Choose your preferred CI/CD platform
- Select deployment target platform
- Customize build and deployment settings
- Configure environment variables

### 4. Generation & Upload

- Generate appropriate CI/CD configuration files
- Create GitHub repository with proper structure
- Push your code with complete CI/CD setup
- Set up branch protection and deployment rules

## 🔧 CI/CD Pipeline Features

Each generated CI/CD configuration includes:

### Testing & Quality

- **Automated Testing**: Unit, integration, and E2E tests
- **Security Scanning**: Dependency vulnerability checks
- **Code Quality**: Linting, formatting, and analysis
- **Coverage Reports**: Test coverage tracking

### Build & Deploy

- **Building**: Project compilation and packaging
- **Deployment**: Automated deployment to chosen platform
- **Branch Protection**: Main branch deployment only
- **Parallel Jobs**: Optimized execution time
- **Caching**: Build artifact and dependency caching

### Monitoring & Notifications

- **Status Checks**: Build and deployment status
- **Notifications**: Slack, email, or webhook notifications
- **Logging**: Comprehensive build and deployment logs
- **Rollback**: Automatic rollback on deployment failure

## 🔍 Project Type Detection

The application automatically detects project types based on file patterns:

### Web Development

- **React**: `package.json` with React dependencies, `src/` structure
- **Vue**: `package.json` with Vue dependencies, `src/` structure
- **Angular**: `package.json` with Angular dependencies, `src/` structure
- **Next.js**: `next.config.js`, `pages/` or `app/` directory
- **Nuxt.js**: `nuxt.config.js`, `pages/` directory

### Backend Development

- **Node.js**: `package.json`, `node_modules/`, Express/Fastify patterns
- **Python**: `requirements.txt`, `pyproject.toml`, `*.py` files
- **Java**: `pom.xml`, `build.gradle`, `*.java` files
- **Go**: `go.mod`, `go.sum`, `*.go` files
- **Rust**: `Cargo.toml`, `Cargo.lock`, `*.rs` files
- **PHP**: `composer.json`, `*.php` files
- **Ruby**: `Gemfile`, `*.rb` files
- **.NET**: `*.csproj`, `*.vbproj` files

### DevOps & Infrastructure

- **Docker**: `Dockerfile`, `docker-compose.yml`
- **Kubernetes**: `*.yaml` files with K8s manifests
- **Terraform**: `*.tf` files
- **Ansible**: `*.yml` files with Ansible playbooks

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- GitHub account
- OpenAI API key (for AI features)

### Quick Installation

1. **Clone the repository:**

```bash
git clone <repository-url>
cd github-uploader
```

2. **Set up environment:**

```bash
cp env.example .env
# Edit .env with your credentials
```

3. **Start with Docker (Recommended):**

```bash
docker-compose up -d
```

4. **Or start manually:**

```bash
# Backend
cd server && pip install -r requirements.txt && python main.py

# Frontend (new terminal)
cd client && npm install && npm start
```

### Environment Variables

Create a `.env` file in the server directory:

```env
# GitHub OAuth
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

# OpenAI API (for AI features)
OPENAI_API_KEY=your_openai_api_key

# Security
SECRET_KEY=your_secret_key

# Optional: Platform integrations
VERCEL_TOKEN=your_vercel_token
RAILWAY_TOKEN=your_railway_token
NETLIFY_TOKEN=your_netlify_token
HEROKU_API_KEY=your_heroku_api_key
```

## 📖 Usage Guide

### 1. Initial Setup

1. **Login**: Click "Login with GitHub" to authenticate
2. **Connect Platforms**: Set up OAuth connections to deployment platforms
3. **Configure Settings**: Set default preferences for CI/CD and deployment

### 2. Project Upload

1. **Upload**: Drag your project folder or click to select
2. **Review Analysis**: Check AI suggestions for repository name and project type
3. **Customize**: Modify repository name, description, and settings
4. **Configure CI/CD**: Select your preferred CI/CD platform and deployment target

### 3. Deployment

1. **Generate**: The app generates appropriate CI/CD configuration files
2. **Upload**: Creates GitHub repository and pushes your code
3. **Monitor**: Track build and deployment progress
4. **Access**: Get deployment URLs and access credentials

## 🐳 Docker Deployment

### Quick Start

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Deployment

```bash
# Use production configuration
docker-compose -f docker-compose.prod.yml up -d
```

## 🔧 Platform Integration Setup

### Vercel Integration

1. Create Vercel account and get API token
2. Add `VERCEL_TOKEN` to environment variables
3. Connect through the dashboard

### Railway Integration

1. Create Railway account and get API token
2. Add `RAILWAY_TOKEN` to environment variables
3. Connect through the dashboard

### Netlify Integration

1. Create Netlify account and get API token
2. Add `NETLIFY_TOKEN` to environment variables
3. Connect through the dashboard

## 🛡️ Security Features

- **OAuth Authentication**: Secure GitHub login
- **Token Management**: Automatic token refresh and secure storage
- **Input Validation**: Comprehensive input sanitization
- **Rate Limiting**: API rate limiting to prevent abuse
- **CORS Protection**: Cross-origin request protection
- **Environment Variables**: Secure credential management

## 🔍 Troubleshooting

### Common Issues

**OAuth Authentication Fails:**

- Verify GitHub OAuth app configuration
- Check redirect URI settings
- Ensure client ID and secret are correct

**Upload Fails:**

- Check file size limits
- Verify GitHub repository permissions
- Ensure valid project structure

**CI/CD Generation Issues:**

- Verify project type detection
- Check for required configuration files
- Ensure platform tokens are valid

### Debug Mode

Enable debug logging:

```bash
DEBUG=true python main.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - feel free to use and modify for your own projects.

## 🆕 Recent Updates (v2.0.0)

- **Enhanced AI Analysis**: Improved project type detection and naming
- **Platform Integrations**: OAuth connections to deployment platforms
- **Template System**: Pre-configured templates for common projects
- **Security Enhancements**: Better token management and validation
- **UI Improvements**: Modern interface with better UX
- **Performance Optimizations**: Faster upload and processing
- **Error Handling**: Better error messages and recovery
- **Documentation**: Comprehensive guides and examples
