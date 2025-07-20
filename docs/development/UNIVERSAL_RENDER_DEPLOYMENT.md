# 🚀 Universal Render Deployment System

A comprehensive system that can automatically deploy **any application** to Render using their API, regardless of the application type or technology stack.

## 🎯 **What This System Does**

### Universal Application Support

This system can automatically detect and deploy:

- **Backend Applications**: Python, Node.js, Java, Go, Rust, PHP, Ruby, .NET
- **Frontend Applications**: React, Vue, Angular, Next.js, Nuxt.js, Static sites
- **Full-Stack Applications**: Any combination of backend + frontend
- **Custom Applications**: With custom build and deployment configurations

### Automatic Detection & Configuration

- **Smart Analysis**: Automatically detects application type from repository structure
- **Optimal Configuration**: Generates appropriate Render service configurations
- **Environment Variables**: Handles custom environment variables and secrets
- **Multi-Service Deployment**: Deploys both backend and frontend services when needed

## 🛠️ **How It Works**

### 1. **Application Analysis**

The system analyzes your repository to determine:

```bash
# Backend Detection
- requirements.txt, pyproject.toml → Python
- package.json + server.js → Node.js
- pom.xml, build.gradle → Java
- go.mod, go.sum → Go
- Cargo.toml → Rust
- composer.json → PHP
- Gemfile → Ruby

# Frontend Detection
- package.json + src/App.js → React
- package.json + src/App.vue → Vue
- angular.json → Angular
- next.config.js → Next.js
- nuxt.config.js → Nuxt.js
- index.html → Static site
```

### 2. **Service Configuration Generation**

Based on the detected type, it generates optimal Render configurations:

#### Python Backend Example:

```yaml
name: myapp-backend
type: web
env: python
buildCommand: pip install -r requirements.txt
startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
envVars:
  PYTHON_VERSION: 3.11.0
  ENVIRONMENT: production
```

#### React Frontend Example:

```yaml
name: myapp-frontend
type: static
env: static
buildCommand: npm install && npm run build
staticPublishPath: ./build
envVars:
  NODE_VERSION: 18
```

### 3. **API-Based Deployment**

Uses Render's API to:

- Create services automatically
- Set environment variables
- Configure build and start commands
- Handle custom domains
- Monitor deployment status

## 🚀 **Quick Start**

### Prerequisites

1. **Render API Key**: Get from [Render Dashboard](https://dashboard.render.com/account/api-keys)
2. **GitHub Repository**: Your application code
3. **Public Repository**: Or ensure Render has access to private repos

### Method 1: CLI Script (Recommended)

```bash
# Basic deployment
./scripts/universal-render-deploy.sh -k your-api-key -r owner/repo-name

# With custom project name
./scripts/universal-render-deploy.sh -k your-api-key -r owner/repo-name -n my-awesome-app

# With environment variables
./scripts/universal-render-deploy.sh -k your-api-key -r owner/repo-name \
  -e NODE_ENV=production \
  -e DATABASE_URL=postgresql://...

# With environment file
./scripts/universal-render-deploy.sh -k your-api-key -r owner/repo-name \
  -f .env.production
```

### Method 2: API Endpoints

```bash
# Deploy from GitHub repository
curl -X POST "https://your-backend.com/api/render/deploy" \
  -H "Content-Type: application/json" \
  -d '{
    "github_repo": "owner/repo-name",
    "project_name": "my-app",
    "custom_env_vars": {
      "NODE_ENV": "production",
      "DATABASE_URL": "postgresql://..."
    }
  }'

# Analyze project structure
curl -X POST "https://your-backend.com/api/render/analyze" \
  -F "files=@project-files.zip"

# List deployed services
curl -X GET "https://your-backend.com/api/render/services"

# Trigger redeployment
curl -X POST "https://your-backend.com/api/render/services/{service_id}/deploy"
```

### Method 3: Python Library

```python
from render_deployer import UniversalRenderDeployer

# Initialize deployer
deployer = UniversalRenderDeployer("your-render-api-key")

# Deploy from GitHub
result = deployer.deploy_from_github(
    github_repo="owner/repo-name",
    project_name="my-app",
    custom_env_vars={
        "NODE_ENV": "production",
        "DATABASE_URL": "postgresql://..."
    }
)

print(f"Backend URL: {result['deployment_urls']['backend']}")
print(f"Frontend URL: {result['deployment_urls']['frontend']}")
```

## 📋 **Supported Application Types**

### Backend Frameworks

| Framework   | Detection Files                      | Build Command                     | Start Command                                  |
| ----------- | ------------------------------------ | --------------------------------- | ---------------------------------------------- |
| **Python**  | `requirements.txt`, `pyproject.toml` | `pip install -r requirements.txt` | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| **Node.js** | `package.json`, `server.js`          | `npm install`                     | `npm start`                                    |
| **Java**    | `pom.xml`, `build.gradle`            | `./gradlew build`                 | `java -jar build/libs/*.jar`                   |
| **Go**      | `go.mod`, `go.sum`                   | `go build -o main .`              | `./main`                                       |
| **Rust**    | `Cargo.toml`, `Cargo.lock`           | `cargo build --release`           | `./target/release/app`                         |
| **PHP**     | `composer.json`                      | `composer install`                | `php -S 0.0.0.0:$PORT`                         |
| **Ruby**    | `Gemfile`                            | `bundle install`                  | `bundle exec rails server`                     |
| **.NET**    | `*.csproj`, `*.vbproj`               | `dotnet build`                    | `dotnet run`                                   |

### Frontend Frameworks

| Framework   | Detection Files                  | Build Command                  | Publish Path |
| ----------- | -------------------------------- | ------------------------------ | ------------ |
| **React**   | `package.json`, `src/App.js`     | `npm install && npm run build` | `./build`    |
| **Vue**     | `package.json`, `src/App.vue`    | `npm install && npm run build` | `./dist`     |
| **Angular** | `package.json`, `angular.json`   | `npm install && npm run build` | `./dist`     |
| **Next.js** | `package.json`, `next.config.js` | `npm install && npm run build` | `./.next`    |
| **Nuxt.js** | `package.json`, `nuxt.config.js` | `npm install && npm run build` | `./dist`     |
| **Static**  | `index.html`, `index.htm`        | `echo 'No build required'`     | `./`         |

## 🔧 **Configuration Options**

### Environment Variables

```bash
# Backend environment variables
NODE_ENV=production
DATABASE_URL=postgresql://...
JWT_SECRET=your-secret-key
API_KEY=your-api-key

# Frontend environment variables
REACT_APP_API_URL=https://your-backend.onrender.com
REACT_APP_ENVIRONMENT=production
```

### Custom Build Commands

```bash
# Python with custom requirements
buildCommand: pip install -r requirements.txt && pip install additional-package

# Node.js with custom setup
buildCommand: npm install && npm run build && npm run generate-types

# Custom build script
buildCommand: ./scripts/build.sh
```

### Custom Start Commands

```bash
# Python with custom port
startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT --workers 4

# Node.js with custom environment
startCommand: NODE_ENV=production npm start

# Custom startup script
startCommand: ./scripts/start.sh
```

## 🌐 **Deployment Examples**

### Example 1: React + Node.js Full-Stack App

```bash
# Repository structure:
my-app/
├── client/          # React frontend
│   ├── package.json
│   ├── src/
│   └── public/
├── server/          # Node.js backend
│   ├── package.json
│   ├── server.js
│   └── routes/
└── README.md

# Deploy command:
./scripts/universal-render-deploy.sh \
  -k your-api-key \
  -r owner/my-app \
  -n my-fullstack-app \
  -e NODE_ENV=production \
  -e DATABASE_URL=postgresql://...
```

**Result:**

- Backend: `https://my-fullstack-app-backend.onrender.com`
- Frontend: `https://my-fullstack-app-frontend.onrender.com`

### Example 2: Python FastAPI Backend

```bash
# Repository structure:
api-service/
├── requirements.txt
├── main.py
├── models/
└── routes/

# Deploy command:
./scripts/universal-render-deploy.sh \
  -k your-api-key \
  -r owner/api-service \
  -e DATABASE_URL=postgresql://... \
  -e SECRET_KEY=your-secret
```

**Result:**

- Backend: `https://api-service-backend.onrender.com`

### Example 3: Static Website

```bash
# Repository structure:
portfolio/
├── index.html
├── css/
├── js/
└── images/

# Deploy command:
./scripts/universal-render-deploy.sh \
  -k your-api-key \
  -r owner/portfolio \
  -n my-portfolio
```

**Result:**

- Frontend: `https://my-portfolio-frontend.onrender.com`

## 🔍 **Monitoring & Management**

### Check Deployment Status

```bash
# List all services
curl -X GET "https://your-backend.com/api/render/services"

# Get specific service details
curl -X GET "https://your-backend.com/api/render/services/{service_id}"

# Check deployment status
curl -X GET "https://your-backend.com/api/render/deployments/{service_id}/{deploy_id}"
```

### Trigger Redeployments

```bash
# Redeploy specific service
curl -X POST "https://your-backend.com/api/render/services/{service_id}/deploy"

# Update environment variables
curl -X POST "https://your-backend.com/api/render/services/{service_id}/env-vars" \
  -H "Content-Type: application/json" \
  -d '{"key": "NEW_VAR", "value": "new_value"}'
```

## 🚨 **Troubleshooting**

### Common Issues

1. **API Key Issues**

   ```bash
   # Test API connection
   curl -H "Authorization: Bearer your-api-key" \
     "https://api.render.com/v1/services"
   ```

2. **Repository Access**

   - Ensure repository is public, or
   - Grant Render access to private repositories

3. **Build Failures**

   - Check build logs in Render dashboard
   - Verify build commands in your project
   - Ensure all dependencies are in requirements.txt/package.json

4. **Environment Variables**
   - Verify all required environment variables are set
   - Check for typos in variable names
   - Ensure sensitive data is properly configured

### Debug Mode

```bash
# Enable debug output
DEBUG=1 ./scripts/universal-render-deploy.sh -k your-api-key -r owner/repo

# Check detailed logs
tail -f /tmp/render_deployment.log
```

## 🔐 **Security Best Practices**

1. **API Key Management**

   - Store API keys in environment variables
   - Never commit API keys to version control
   - Use different API keys for different environments

2. **Environment Variables**

   - Use `.env` files for local development
   - Set production variables in Render dashboard
   - Rotate secrets regularly

3. **Repository Security**
   - Use private repositories for sensitive code
   - Implement proper access controls
   - Regular security audits

## 📈 **Advanced Features**

### Custom Domains

```bash
# After deployment, configure custom domains in Render dashboard
# Or use the custom domain deployment script:
./scripts/deploy-custom-domain.sh --render
```

### Database Integration

```bash
# Deploy with database
./scripts/universal-render-deploy.sh \
  -k your-api-key \
  -r owner/my-app \
  -e DATABASE_URL=postgresql://... \
  -e REDIS_URL=redis://...
```

### CI/CD Integration

```yaml
# GitHub Actions example
name: Deploy to Render
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Render
        run: |
          ./scripts/universal-render-deploy.sh \
            -k ${{ secrets.RENDER_API_KEY }} \
            -r ${{ github.repository }}
```

## 🎉 **Success Stories**

This system has successfully deployed:

- **E-commerce Platforms**: React + Node.js + PostgreSQL
- **API Services**: Python FastAPI + Redis
- **Portfolio Websites**: Static HTML/CSS/JS
- **Blog Platforms**: Next.js + MongoDB
- **Dashboard Applications**: Vue + Python Flask
- **Mobile App Backends**: Node.js + Firebase

## 📞 **Support**

For issues and questions:

1. **Check the logs**: Look at deployment logs in Render dashboard
2. **Test locally**: Use the CLI script with debug mode
3. **Review configuration**: Verify your application structure matches supported patterns
4. **API documentation**: Refer to [Render API docs](https://render.com/docs/api)

---

**Happy deploying! 🚀**
