# GitHub Uploader

A web application that automates uploading projects to GitHub with AI-powered analysis and CI/CD pipeline generation.

## Features

- **GitHub OAuth Integration**: Secure authentication with GitHub
- **Drag & Drop Upload**: Upload entire folders with ease
- **AI-Powered Analysis**: Automatic project type detection and repository naming
- **Multi-Platform CI/CD**: Support for 8 different CI/CD platforms
- **Deployment Automation**: Generate deployment configurations for 12+ platforms
- **Project Type Detection**: Auto-detect Node.js, Python, Java, Go, Rust, PHP, Ruby, and .NET projects

## CI/CD Platform Support

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

## Deployment Platform Support

Each CI/CD configuration can be customized for deployment to:

- **Vercel** - Frontend hosting
- **Railway** - Full-stack hosting
- **Netlify** - Static site hosting
- **Heroku** - Platform-as-a-Service
- **AWS** - Cloud infrastructure
- **Google Cloud Platform** - Cloud services
- **Microsoft Azure** - Cloud platform
- **DigitalOcean** - VPS hosting
- **Render** - Modern cloud platform
- **Fly.io** - Global edge deployment
- **Custom Scripts** - Custom deployment logic

## How It Works

1. **Authentication**: Login with GitHub OAuth to get secure access
2. **Upload**: Drag and drop your project folder or use the folder selector
3. **Analysis**: AI analyzes your project structure and suggests:
   - Repository name
   - Project type
   - Dependencies
   - Recommended CI/CD platform
4. **Configuration**: Choose your preferred CI/CD platform and deployment target
5. **Generation**: The app generates appropriate CI/CD configuration files
6. **Upload**: Creates GitHub repository and pushes your code with CI/CD setup

## CI/CD Pipeline Features

Each generated CI/CD configuration includes:

- **Testing**: Automated test execution
- **Security Scanning**: Dependency vulnerability checks
- **Code Quality**: Linting and code analysis
- **Building**: Project compilation and packaging
- **Deployment**: Automated deployment to chosen platform
- **Branch Protection**: Main branch deployment only
- **Parallel Jobs**: Optimized execution time

## Project Type Detection

The application automatically detects project types based on file patterns:

- **Node.js**: `package.json`, `node_modules/`
- **Python**: `requirements.txt`, `pyproject.toml`, `*.py`
- **Java**: `pom.xml`, `build.gradle`, `*.java`
- **Go**: `go.mod`, `go.sum`, `*.go`
- **Rust**: `Cargo.toml`, `Cargo.lock`, `*.rs`
- **PHP**: `composer.json`, `*.php`
- **Ruby**: `Gemfile`, `*.rb`
- **.NET**: `*.csproj`, `*.vbproj`

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- GitHub account

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd github-uploader
```

2. Set up the backend:

```bash
cd server
pip install -r requirements.txt
```

3. Set up the frontend:

```bash
cd client
npm install
```

4. Configure environment variables:

```bash
cp env.example .env
# Edit .env with your GitHub OAuth credentials
```

5. Start the development servers:

```bash
# Terminal 1 - Backend
cd server
python main.py

# Terminal 2 - Frontend
cd client
npm start
```

### Environment Variables

Create a `.env` file in the server directory:

```env
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=your_secret_key
```

## Usage

1. **Login**: Click "Login with GitHub" to authenticate
2. **Upload**: Drag your project folder or click to select
3. **Review**: Check AI suggestions for repository name and project type
4. **Configure**: Select your preferred CI/CD platform and deployment target
5. **Upload**: Click "Upload to GitHub" to create the repository

## Docker Deployment

### Quick Start with Docker Compose

```bash
docker-compose up -d
```

### Individual Containers

```bash
# Backend
docker build -t github-uploader-backend ./server
docker run -p 8000:8000 github-uploader-backend

# Frontend
docker build -t github-uploader-frontend ./client
docker run -p 3000:3000 github-uploader-frontend
```

## API Endpoints

- `GET /auth/github/login` - Initiate GitHub OAuth
- `GET /auth/github/callback` - OAuth callback handler
- `GET /auth/status` - Check authentication status
- `POST /auth/logout` - Logout user
- `POST /analyze` - Analyze uploaded files
- `POST /upload` - Upload project to GitHub

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:

- Create an issue on GitHub
- Check the documentation
- Review the troubleshooting guide

## Roadmap

- [ ] Support for more CI/CD platforms (TeamCity, Bamboo)
- [ ] Advanced deployment strategies (Blue-Green, Canary)
- [ ] Multi-environment support (Dev, Staging, Prod)
- [ ] Integration with more deployment platforms
- [ ] Custom CI/CD template support
- [ ] Team collaboration features
