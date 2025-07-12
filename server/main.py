import os
import shutil
import tempfile
from fastapi import FastAPI, Request, UploadFile, File, Form, Response, Depends, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2AuthorizationCodeBearer
from starlette.middleware.sessions import SessionMiddleware
import requests
import openai
import git
from dotenv import load_dotenv
from typing import List
import uuid
import time

load_dotenv()

app = FastAPI()

# Get allowed origins from environment or use defaults
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
if os.getenv("ENVIRONMENT") == "production":
    # Add common production frontend URLs
    production_origins = [
        "https://github-uploader-frontend.onrender.com",
        "https://repotorpedo-frontend.onrender.com",
        "https://github-uploader.vercel.app",
        "https://github-uploader.netlify.app"
    ]
    ALLOWED_ORIGINS.extend(production_origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY", "supersecret"),
    session_cookie="ghuploader_session",
    https_only=False,
)

# Environment variables
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")

# Determine URLs based on environment
if os.getenv("ENVIRONMENT") == "production":
    BASE_URL = os.getenv("BASE_URL", "https://repotorpedo-backend.onrender.com")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "https://repotorpedo-frontend.onrender.com")
else:
    BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
    # Determine frontend URL - use PORT env var if set (from dev dashboard), otherwise use FRONTEND_URL
    CLIENT_PORT = os.getenv("PORT")
    if CLIENT_PORT:
        FRONTEND_URL = f"http://localhost:{CLIENT_PORT}"
    else:
        FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

# GitHub API endpoints
GITHUB_API_REPOS_URL = "https://api.github.com/user/repos"
GITHUB_API_USER_URL = "https://api.github.com/user"

GITHUB_OAUTH_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_OAUTH_ACCESS_TOKEN_URL = "https://github.com/login/oauth/access_token"

openai.api_key = OPENAI_API_KEY

# --- Health Check Endpoint ---
@app.get("/health")
def health_check():
    from datetime import datetime
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "2.0.0",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

# --- OAuth Endpoints ---
@app.get("/api/auth/github/login")
def github_login():
    # Use production callback URL if in production environment
    callback_url = os.getenv("GITHUB_CALLBACK_URL", f"{BASE_URL}/api/auth/github/callback")
    
    params = {
        "client_id": GITHUB_CLIENT_ID,
        "scope": "repo user",
        "redirect_uri": callback_url
    }
    url = requests.Request('GET', GITHUB_OAUTH_AUTHORIZE_URL, params=params).prepare().url
    return RedirectResponse(url)

@app.get("/api/auth/github/callback")
def github_callback(request: Request, code: str, redirect_to: str = None):
    print(f"Received OAuth code: {code}")
    data = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code,
    }
    headers = {"Accept": "application/json"}
    print(f"Making request to GitHub with data: {data}")
    r = requests.post(GITHUB_OAUTH_ACCESS_TOKEN_URL, data=data, headers=headers)
    print(f"GitHub response status: {r.status_code}")
    print(f"GitHub response: {r.text}")
    
    response_data = r.json()
    token = response_data.get("access_token")
    
    if not token:
        error_msg = response_data.get("error_description", "Unknown OAuth error")
        print(f"OAuth failed: {error_msg}")
        return JSONResponse({"error": f"OAuth failed: {error_msg}"}, status_code=400)
    
    print(f"Successfully obtained access token")
    request.session["github_token"] = token
    print(f"Redirecting to: {FRONTEND_URL}")
    return RedirectResponse(FRONTEND_URL, status_code=302)

@app.get("/api/auth/status")
def auth_status(request: Request):
    token = request.session.get("github_token")
    if token:
        try:
            username = get_github_username(token)
            return {"authenticated": True, "message": "Successfully logged in with GitHub", "username": username}
        except Exception as e:
            print(f"Error getting GitHub username: {e}")
            return {"authenticated": True, "message": "Successfully logged in with GitHub", "username": "GitHub User"}
    else:
        return {"authenticated": False, "message": "Not authenticated"}

@app.post("/api/auth/logout")
def logout(request: Request):
    request.session.clear()
    return {"message": "Logged out successfully"}

# --- Analyze Endpoint ---
@app.post("/analyze")
def analyze(request: Request, files: List[UploadFile] = File(...)):
    temp_dir = tempfile.mkdtemp()
    
    # Save all files to temp directory, stripping the root directory name
    for file in files:
        # Remove the root directory from the path
        path_parts = file.filename.split('/')
        if len(path_parts) > 1:
            # Remove the first part (root directory) and join the rest
            relative_path = '/'.join(path_parts[1:])
        else:
            relative_path = file.filename
        
        file_path = os.path.join(temp_dir, relative_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
    
    # AI: Suggest repo name and dependencies
    summary = analyze_project_with_ai(temp_dir)
    shutil.rmtree(temp_dir)
    return summary

def analyze_project_with_ai(project_path):
    # Heuristic: look for package.json, requirements.txt, etc.
    files = os.listdir(project_path)
    deps = []
    if "package.json" in files:
        deps.append("Node.js (package.json)")
    if "requirements.txt" in files:
        deps.append("Python (requirements.txt)")
    # AI: suggest name and README
    prompt = f"Analyze the following project files: {files}. Suggest a repository name and a list of dependencies."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        ai_suggestion = response.choices[0].message.content
    except Exception as e:
        ai_suggestion = "AI analysis unavailable."
    return {"dependencies": deps, "ai": ai_suggestion}

# --- Upload Endpoint ---
@app.post("/upload")
def upload(request: Request, files: List[UploadFile] = File(...), repo_name: str = Form(...), commit_message: str = Form(...), project_type: str = Form("auto"), deployment_platform: str = Form(""), cicd_platform: str = Form("github-actions"), platform_config: str = Form("{}")):
    # Clean up repository name (remove spaces, special chars)
    clean_repo_name = repo_name.replace(" ", "-").replace("_", "-").lower()
    # Remove any non-alphanumeric characters except hyphens
    import re
    clean_repo_name = re.sub(r'[^a-z0-9-]', '', clean_repo_name)
    # Ensure it starts with a letter
    if clean_repo_name and not clean_repo_name[0].isalpha():
        clean_repo_name = "repo-" + clean_repo_name
    
    print(f"Upload request received:")
    print(f"  - Number of files: {len(files)}")
    print(f"  - Original repo name: {repo_name}")
    print(f"  - Cleaned repo name: {clean_repo_name}")
    print(f"  - Commit message: {commit_message}")
    
    token = request.session.get("github_token")
    if not token:
        print("  - ERROR: No GitHub token found in session")
        raise HTTPException(status_code=401, detail="Not authenticated with GitHub.")
    
    print(f"  - GitHub token found: {token[:10]}...")
    
    temp_dir = tempfile.mkdtemp()
    print(f"  - Created temp directory: {temp_dir}")
    
    # Save all files to temp directory, stripping the root directory name
    for file in files:
        # Remove the root directory from the path
        path_parts = file.filename.split('/')
        if len(path_parts) > 1:
            # Remove the first part (root directory) and join the rest
            relative_path = '/'.join(path_parts[1:])
        else:
            relative_path = file.filename
        
        file_path = os.path.join(temp_dir, relative_path)
        print(f"  - Saving file: {file.filename} -> {relative_path}")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
    
    # Parse platform configuration
    import json
    try:
        parsed_config = json.loads(platform_config)
    except:
        parsed_config = {}
    
    # Auto-detect project type if needed
    if project_type == "auto":
        detected_type = detect_project_type(temp_dir)
        print(f"  - Auto-detected project type: {detected_type}")
        actual_project_type = detected_type
    else:
        actual_project_type = project_type
    
    # Set up platform configuration
    platform_config = {
        "project_type": actual_project_type,
        "deployment_platform": deployment_platform,
        "cicd_platform": cicd_platform,
        **parsed_config
    }
    
    # Generate CI/CD configuration
    print(f"  - Generating CI/CD configuration for {project_type} -> {deployment_platform}...")
    cicd_configs = generate_platform_agnostic_cicd(temp_dir, platform_config)
    for config_name, config in cicd_configs.items():
        config_path = os.path.join(temp_dir, config["filename"])
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w") as f:
            f.write(config["content"])
        print(f"  - Created {config['filename']}")
    
    # Create repo via GitHub API
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    repo_data = {"name": clean_repo_name, "private": False}
    print(f"  - Creating GitHub repo: {clean_repo_name}")
    r = requests.post(GITHUB_API_REPOS_URL, json=repo_data, headers=headers)
    print(f"  - GitHub API response status: {r.status_code}")
    print(f"  - GitHub API response: {r.text}")
    
    if r.status_code not in (201, 422):
        print(f"  - ERROR: Failed to create repo")
        shutil.rmtree(temp_dir)
        raise HTTPException(status_code=400, detail="Failed to create repo.")
    
    # Git init, add, commit, push
    repo_url = f"https://{token}:x-oauth-basic@github.com/{get_github_username(token)}/{clean_repo_name}.git"
    print(f"  - Git repo URL: {repo_url}")
    repo = git.Repo.init(temp_dir)
    repo.git.add(A=True)
    repo.index.commit(commit_message)
    origin = repo.create_remote('origin', repo_url)
    try:
        print(f"  - Pushing to GitHub...")
        # Try main branch first, then master
        try:
            origin.push(refspec='main:main')
            print(f"  - SUCCESS: Push completed to main branch")
        except Exception as main_error:
            print(f"  - Main branch failed, trying master: {main_error}")
            origin.push(refspec='master:master')
            print(f"  - SUCCESS: Push completed to master branch")
    except Exception as e:
        print(f"  - ERROR: Git push failed: {e}")
        shutil.rmtree(temp_dir)
        raise HTTPException(status_code=400, detail=f"Git push failed: {e}")
    shutil.rmtree(temp_dir)
    return {"status": "success"}

def get_github_username(token):
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    r = requests.get(GITHUB_API_USER_URL, headers=headers)
    return r.json().get("login", "user") 

def detect_project_type(project_path):
    """Auto-detect project type based on files in the project"""
    files = os.listdir(project_path)
    
    # Check for Node.js
    if "package.json" in files:
        return "nodejs"
    
    # Check for Python
    if "requirements.txt" in files or "pyproject.toml" in files or any(f.endswith('.py') for f in files):
        return "python"
    
    # Check for Java
    if "pom.xml" in files or "build.gradle" in files or any(f.endswith('.java') for f in files):
        return "java"
    
    # Check for Go
    if "go.mod" in files or "go.sum" in files or any(f.endswith('.go') for f in files):
        return "go"
    
    # Check for Rust
    if "Cargo.toml" in files or "Cargo.lock" in files or any(f.endswith('.rs') for f in files):
        return "rust"
    
    # Check for PHP
    if "composer.json" in files or any(f.endswith('.php') for f in files):
        return "php"
    
    # Check for Ruby
    if "Gemfile" in files or any(f.endswith('.rb') for f in files):
        return "ruby"
    
    # Check for .NET
    if any(f.endswith('.csproj') for f in files) or any(f.endswith('.vbproj') for f in files):
        return "dotnet"
    
    # Default to Node.js if no clear indicators
    return "nodejs"

def generate_platform_agnostic_cicd(project_path, platform_config):
    """Generate CI/CD configuration for any platform"""
    files = os.listdir(project_path)
    configs = {}
    
    # Get the CI/CD platform preference
    cicd_platform = platform_config.get("cicd_platform", "github-actions")
    
    # Generate CI/CD configuration based on platform choice
    if cicd_platform == "github-actions":
        configs["github-actions"] = generate_base_workflow(platform_config)
    elif cicd_platform == "gitlab-ci":
        configs["gitlab-ci"] = generate_gitlab_ci(platform_config)
    elif cicd_platform == "jenkins":
        configs["jenkins"] = generate_jenkins_pipeline(platform_config)
    elif cicd_platform == "circleci":
        configs["circleci"] = generate_circleci_config(platform_config)
    elif cicd_platform == "travis-ci":
        configs["travis-ci"] = generate_travis_config(platform_config)
    elif cicd_platform == "azure-devops":
        configs["azure-devops"] = generate_azure_devops_pipeline(platform_config)
    elif cicd_platform == "drone":
        configs["drone"] = generate_drone_config(platform_config)
    elif cicd_platform == "woodpecker":
        configs["woodpecker"] = generate_woodpecker_config(platform_config)
    
    # Platform-specific configurations
    if platform_config.get("deployment_platform"):
        platform = platform_config["deployment_platform"].lower()
        if platform == "vercel":
            configs["vercel"] = generate_vercel_config()
        elif platform == "railway":
            configs["railway"] = generate_railway_config()
        elif platform == "netlify":
            configs["netlify"] = generate_netlify_config()
        elif platform == "heroku":
            configs["heroku"] = generate_heroku_config()
        elif platform == "aws":
            configs["aws"] = generate_aws_config(platform_config)
        elif platform == "gcp":
            configs["gcp"] = generate_gcp_config(platform_config)
        elif platform == "azure":
            configs["azure"] = generate_azure_config(platform_config)
        elif platform == "digitalocean":
            configs["digitalocean"] = generate_digitalocean_config(platform_config)
        elif platform == "render":
            configs["render"] = generate_render_config()
        elif platform == "fly.io":
            configs["fly"] = generate_fly_config()
        elif platform == "custom":
            configs["custom"] = generate_custom_config(platform_config)
    
    return configs

def generate_base_workflow(platform_config):
    """Generate a flexible base GitHub Actions workflow"""
    project_type = platform_config.get("project_type", "auto")
    deployment_platform = platform_config.get("deployment_platform", "none")
    
    workflow_content = f"""name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup {project_type.title()}
      {get_setup_step(project_type)}
    
    - name: Install dependencies
      {get_install_step(project_type)}
    
    - name: Run linter
      {get_lint_step(project_type)}
    
    - name: Run tests
      {get_test_step(project_type)}
    
    - name: Build project
      {get_build_step(project_type)}
    
  security:
    runs-on: ubuntu-latest
    needs: test
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Run security scan
      {get_security_step(project_type)}
    
  deploy:
    runs-on: ubuntu-latest
    needs: [test, security]
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    {get_deploy_step(deployment_platform, platform_config)}
"""
    
    return {
        "filename": ".github/workflows/ci.yml",
        "content": workflow_content
    }

def get_setup_step(project_type):
    """Get the setup step based on project type"""
    if project_type == "nodejs":
        return """uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'"""
    elif project_type == "python":
        return """uses: actions/setup-python@v4
      with:
        python-version: '3.11'"""
    elif project_type == "java":
        return """uses: actions/setup-java@v3
      with:
        java-version: '17'
        distribution: 'temurin'"""
    elif project_type == "go":
        return """uses: actions/setup-go@v4
      with:
        go-version: '1.21'"""
    elif project_type == "rust":
        return """uses: actions-rs/toolchain@v1
      with:
        toolchain: stable"""
    elif project_type == "php":
        return """uses: shivammathur/setup-php@v2
      with:
        php-version: '8.2'"""
    elif project_type == "ruby":
        return """uses: ruby/setup-ruby@v1
      with:
        ruby-version: '3.2'"""
    elif project_type == "dotnet":
        return """uses: actions/setup-dotnet@v3
      with:
        dotnet-version: '7.0.x'"""
    else:
        return """uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'"""

def get_install_step(project_type):
    """Get the install dependencies step"""
    if project_type == "nodejs":
        return "run: npm ci"
    elif project_type == "python":
        return """run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest flake8 black"""
    elif project_type == "java":
        return "run: ./gradlew build"
    elif project_type == "go":
        return "run: go mod download"
    elif project_type == "rust":
        return "run: cargo build"
    elif project_type == "php":
        return "run: composer install"
    elif project_type == "ruby":
        return "run: bundle install"
    elif project_type == "dotnet":
        return "run: dotnet restore"
    else:
        return "run: npm ci"

def get_lint_step(project_type):
    """Get the linting step"""
    if project_type == "nodejs":
        return "run: npm run lint"
    elif project_type == "python":
        return """run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        black . --check"""
    elif project_type == "java":
        return "run: ./gradlew checkstyleMain"
    elif project_type == "go":
        return "run: golangci-lint run"
    elif project_type == "rust":
        return "run: cargo clippy"
    elif project_type == "php":
        return "run: composer run-script lint"
    elif project_type == "ruby":
        return "run: bundle exec rubocop"
    elif project_type == "dotnet":
        return "run: dotnet format --verify-no-changes"
    else:
        return "run: npm run lint"

def get_test_step(project_type):
    """Get the testing step"""
    if project_type == "nodejs":
        return "run: npm test"
    elif project_type == "python":
        return "run: pytest"
    elif project_type == "java":
        return "run: ./gradlew test"
    elif project_type == "go":
        return "run: go test ./..."
    elif project_type == "rust":
        return "run: cargo test"
    elif project_type == "php":
        return "run: composer test"
    elif project_type == "ruby":
        return "run: bundle exec rspec"
    elif project_type == "dotnet":
        return "run: dotnet test"
    else:
        return "run: npm test"

def get_build_step(project_type):
    """Get the build step"""
    if project_type == "nodejs":
        return "run: npm run build"
    elif project_type == "python":
        return "run: echo 'Python build completed'"
    elif project_type == "java":
        return "run: ./gradlew build"
    elif project_type == "go":
        return "run: go build -o app ."
    elif project_type == "rust":
        return "run: cargo build --release"
    elif project_type == "php":
        return "run: echo 'PHP build completed'"
    elif project_type == "ruby":
        return "run: echo 'Ruby build completed'"
    elif project_type == "dotnet":
        return "run: dotnet build --configuration Release"
    else:
        return "run: npm run build"

def get_security_step(project_type):
    """Get the security scanning step"""
    if project_type == "nodejs":
        return """uses: snyk/actions/node@master
      env:
        SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}"""
    elif project_type == "python":
        return """uses: snyk/actions/python@master
      env:
        SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}"""
    elif project_type == "java":
        return """uses: snyk/actions/maven@master
      env:
        SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}"""
    else:
        return """uses: snyk/actions/node@master
      env:
        SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}"""

def get_deploy_step(platform, config):
    """Get the deployment step based on platform"""
    if platform == "vercel":
        return """- name: Deploy to Vercel
      uses: amondnet/vercel-action@v25
      with:
        vercel-token: ${{ secrets.VERCEL_TOKEN }}
        vercel-org-id: ${{ secrets.ORG_ID }}
        vercel-project-id: ${{ secrets.PROJECT_ID }}
        vercel-args: '--prod'"""
    
    elif platform == "railway":
        return """- name: Deploy to Railway
      run: |
        curl -X POST https://api.railway.app/v2/projects/${{ secrets.RAILWAY_PROJECT_ID }}/deployments \\
          -H "Authorization: Bearer ${{ secrets.RAILWAY_TOKEN }}" """
    
    elif platform == "netlify":
        return """- name: Deploy to Netlify
      uses: nwtgck/actions-netlify@v2.0
      with:
        publish-dir: './dist'
        production-branch: main
        github-token: ${{ secrets.GITHUB_TOKEN }}
        deploy-message: "Deploy from GitHub Actions"
      env:
        NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
        NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}"""
    
    elif platform == "heroku":
        return """- name: Deploy to Heroku
      uses: akhileshns/heroku-deploy@v3.12.14
      with:
        heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
        heroku_app_name: ${{ secrets.HEROKU_APP_NAME }}
        heroku_email: ${{ secrets.HEROKU_EMAIL }}"""
    
    elif platform == "aws":
        return generate_aws_deploy_step(config)
    
    elif platform == "gcp":
        return generate_gcp_deploy_step(config)
    
    elif platform == "azure":
        return generate_azure_deploy_step(config)
    
    elif platform == "digitalocean":
        return generate_digitalocean_deploy_step(config)
    
    elif platform == "render":
        return """- name: Deploy to Render
      run: |
        curl -X POST https://api.render.com/v1/services/${{ secrets.RENDER_SERVICE_ID }}/deploys \\
          -H "Authorization: Bearer ${{ secrets.RENDER_API_KEY }}" """
    
    elif platform == "fly.io":
        return """- name: Deploy to Fly.io
      uses: superfly/flyctl-actions/setup-flyctl@master
      - name: Deploy app
      run: flyctl deploy --remote-only"""
    
    elif platform == "custom":
        return generate_custom_deploy_step(config)
    
    else:
        return """- name: Deploy (Manual)
      run: echo 'Deployment step not configured. Please set up deployment manually.'"""

def generate_vercel_config():
    """Generate Vercel configuration for Node.js projects"""
    return {
        "filename": "vercel.json",
        "content": """{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/node"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/"
    }
  ]
}"""
    }

def generate_railway_config():
    """Generate Railway configuration for Python projects"""
    return {
        "filename": "railway.json",
        "content": """{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python main.py",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}"""
    }

def generate_docker_compose():
    """Generate Docker Compose configuration"""
    return {
        "filename": "docker-compose.yml",
        "content": """version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - app
    restart: unless-stopped"""
    } 

def generate_netlify_config():
    """Generate Netlify configuration"""
    return {
        "filename": "netlify.toml",
        "content": """[build]
  publish = "dist"
  command = "npm run build"

[build.environment]
  NODE_VERSION = "18"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200"""
    }

def generate_heroku_config():
    """Generate Heroku configuration"""
    return {
        "filename": "Procfile",
        "content": "web: npm start"
    }

def generate_aws_config(config):
    """Generate AWS configuration"""
    return {
        "filename": "aws-deploy.yml",
        "content": f"""name: Deploy to AWS
uses: aws-actions/configure-aws-credentials@v1
with:
  aws-access-key-id: ${{{{ secrets.AWS_ACCESS_KEY_ID }}}}
  aws-secret-access-key: ${{{{ secrets.AWS_SECRET_ACCESS_KEY }}}}
  aws-region: {config.get('aws_region', 'us-east-1')}

- name: Deploy to AWS
  run: |
    aws s3 sync dist/ s3://${{{{ secrets.S3_BUCKET }}}}/
    aws cloudfront create-invalidation --distribution-id ${{{{ secrets.CLOUDFRONT_DISTRIBUTION_ID }}}} --paths "/*" """
    }

def generate_gcp_config(config):
    """Generate Google Cloud Platform configuration"""
    return {
        "filename": "gcp-deploy.yml",
        "content": f"""name: Deploy to GCP
uses: google-github-actions/setup-gcloud@v0
with:
  project_id: ${{{{ secrets.GCP_PROJECT_ID }}}}
  service_account_key: ${{{{ secrets.GCP_SA_KEY }}}}
  export_default_credentials: true

- name: Deploy to Cloud Run
  run: |
    gcloud run deploy {config.get('service_name', 'myapp')} \\
      --source . \\
      --platform managed \\
      --region {config.get('gcp_region', 'us-central1')} \\
      --allow-unauthenticated"""
    }

def generate_azure_config(config):
    """Generate Azure configuration"""
    return {
        "filename": "azure-deploy.yml",
        "content": f"""name: Deploy to Azure
uses: azure/login@v1
with:
  creds: ${{{{ secrets.AZURE_CREDENTIALS }}}}

- name: Deploy to Azure Web App
  uses: azure/webapps-deploy@v2
  with:
    app-name: {config.get('app_name', 'myapp')}
    package: ."""
    }

def generate_digitalocean_config(config):
    """Generate DigitalOcean configuration"""
    return {
        "filename": "do-deploy.yml",
        "content": f"""name: Deploy to DigitalOcean
run: |
  doctl kubernetes cluster kubeconfig save {config.get('cluster_name', 'my-cluster')}
  kubectl set image deployment/{config.get('deployment_name', 'myapp')} \\
    {config.get('container_name', 'app')}=${{{{ secrets.DOCKER_IMAGE }}}}:${{{{ github.sha }}}}"""
    }

def generate_render_config():
    """Generate Render configuration"""
    return {
        "filename": "render.yaml",
        "content": """services:
  - type: web
    name: myapp
    env: node
    buildCommand: npm install && npm run build
    startCommand: npm start
    envVars:
      - key: NODE_ENV
        value: production"""
    }

def generate_fly_config():
    """Generate Fly.io configuration"""
    return {
        "filename": "fly.toml",
        "content": """app = "myapp"
primary_region = "iad"

[build]

[env]
  PORT = "8080"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  processes = ["app"]

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 256"""
    }

def generate_custom_config(config):
    """Generate custom deployment configuration"""
    custom_script = config.get('custom_script', 'echo "Custom deployment not configured"')
    return {
        "filename": "custom-deploy.sh",
        "content": f"""#!/bin/bash
{custom_script}"""
    }

def generate_aws_deploy_step(config):
    """Generate AWS deployment step"""
    return f"""- name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v1
      with:
        aws-access-key-id: ${{{{ secrets.AWS_ACCESS_KEY_ID }}}}
        aws-secret-access-key: ${{{{ secrets.AWS_SECRET_ACCESS_KEY }}}}
        aws-region: {config.get('aws_region', 'us-east-1')}
    
    - name: Deploy to AWS
      run: |
        aws s3 sync dist/ s3://${{{{ secrets.S3_BUCKET }}}}/
        aws cloudfront create-invalidation --distribution-id ${{{{ secrets.CLOUDFRONT_DISTRIBUTION_ID }}}} --paths "/*" """

def generate_gcp_deploy_step(config):
    """Generate GCP deployment step"""
    return f"""- name: Setup GCP
      uses: google-github-actions/setup-gcloud@v0
      with:
        project_id: ${{{{ secrets.GCP_PROJECT_ID }}}}
        service_account_key: ${{{{ secrets.GCP_SA_KEY }}}}
        export_default_credentials: true
    
    - name: Deploy to Cloud Run
      run: |
        gcloud run deploy {config.get('service_name', 'myapp')} \\
          --source . \\
          --platform managed \\
          --region {config.get('gcp_region', 'us-central1')} \\
          --allow-unauthenticated"""

def generate_azure_deploy_step(config):
    """Generate Azure deployment step"""
    return f"""- name: Login to Azure
      uses: azure/login@v1
      with:
        creds: ${{{{ secrets.AZURE_CREDENTIALS }}}}
    
    - name: Deploy to Azure Web App
      uses: azure/webapps-deploy@v2
      with:
        app-name: {config.get('app_name', 'myapp')}
        package: ."""

def generate_digitalocean_deploy_step(config):
    """Generate DigitalOcean deployment step"""
    return f"""- name: Deploy to DigitalOcean
      run: |
        doctl kubernetes cluster kubeconfig save {config.get('cluster_name', 'my-cluster')}
        kubectl set image deployment/{config.get('deployment_name', 'myapp')} \\
          {config.get('container_name', 'app')}=${{{{ secrets.DOCKER_IMAGE }}}}:${{{{ github.sha }}}}"""

def generate_custom_deploy_step(config):
    """Generate custom deployment step"""
    custom_script = config.get('custom_script', 'echo "Custom deployment not configured"')
    return f"""- name: Custom Deployment
      run: |
        {custom_script}""" 

def generate_gitlab_ci(platform_config):
    """Generate GitLab CI configuration"""
    project_type = platform_config.get("project_type", "nodejs")
    deployment_platform = platform_config.get("deployment_platform", "")
    
    stages = ["test", "security", "build"]
    if deployment_platform:
        stages.append("deploy")
    
    content = f"""stages:
  - {' - '.join(stages)}

variables:
  NODE_VERSION: "18"

test:
  stage: test
  image: node:{get_node_version(project_type)}
  script:
    {get_gitlab_install_step(project_type)}
    {get_gitlab_test_step(project_type)}
  only:
    - main
    - develop
    - merge_requests

security:
  stage: security
  image: node:{get_node_version(project_type)}
  script:
    {get_gitlab_security_step(project_type)}
  only:
    - main
    - develop
    - merge_requests

build:
  stage: build
  image: node:{get_node_version(project_type)}
  script:
    {get_gitlab_build_step(project_type)}
  artifacts:
    paths:
      - dist/
    expire_in: 1 week
  only:
    - main
    - develop
    - merge_requests"""

    if deployment_platform:
        content += f"""

deploy:
  stage: deploy
  image: alpine:latest
  script:
    {get_gitlab_deploy_step(deployment_platform, platform_config)}
  only:
    - main
  when: manual"""
    
    return {
        "filename": ".gitlab-ci.yml",
        "content": content
    }

def generate_jenkins_pipeline(platform_config):
    """Generate Jenkins pipeline configuration"""
    project_type = platform_config.get("project_type", "nodejs")
    deployment_platform = platform_config.get("deployment_platform", "")
    
    content = f"""pipeline {{
    agent any
    
    environment {{
        NODE_VERSION = '{get_node_version(project_type)}'
    }}
    
    stages {{
        stage('Test') {{
            steps {{
                {get_jenkins_test_step(project_type)}
            }}
        }}
        
        stage('Security') {{
            steps {{
                {get_jenkins_security_step(project_type)}
            }}
        }}
        
        stage('Build') {{
            steps {{
                {get_jenkins_build_step(project_type)}
            }}
        }}"""
    
    if deployment_platform:
        content += f"""
        
        stage('Deploy') {{
            when {{
                branch 'main'
            }}
            steps {{
                {get_jenkins_deploy_step(deployment_platform, platform_config)}
            }}
        }}"""
    
    content += """
    }
}"""
    
    return {
        "filename": "Jenkinsfile",
        "content": content
    }

def generate_circleci_config(platform_config):
    """Generate CircleCI configuration"""
    project_type = platform_config.get("project_type", "nodejs")
    deployment_platform = platform_config.get("deployment_platform", "")
    
    content = f"""version: 2.1

orbs:
  node: circleci/node@5.1.0

jobs:
  test:
    docker:
      - image: cimg/node:{get_node_version(project_type)}
    steps:
      - checkout
      - node/install-packages:
          pkg-manager: npm
      - run:
          name: Run tests
          command: {get_circleci_test_step(project_type)}
  
  security:
    docker:
      - image: cimg/node:{get_node_version(project_type)}
    steps:
      - checkout
      - node/install-packages:
          pkg-manager: npm
      - run:
          name: Security scan
          command: {get_circleci_security_step(project_type)}
  
  build:
    docker:
      - image: cimg/node:{get_node_version(project_type)}
    steps:
      - checkout
      - node/install-packages:
          pkg-manager: npm
      - run:
          name: Build project
          command: {get_circleci_build_step(project_type)}
      - persist_to_workspace:
          root: .
          paths:
            - dist/"""
    
    if deployment_platform:
        content += f"""
  
  deploy:
    docker:
      - image: cimg/node:{get_node_version(project_type)}
    steps:
      - checkout
      - attach_workspace:
          at: .
      - run:
          name: Deploy
          command: {get_circleci_deploy_step(deployment_platform, platform_config)}"""
    
    content += f"""

workflows:
  version: 2
  build-test-deploy:
    jobs:
      - test
      - security
      - build"""
    
    if deployment_platform:
        content += """
      - deploy:
          requires:
            - test
            - security
            - build
          filters:
            branches:
              only: main"""
    
    return {
        "filename": ".circleci/config.yml",
        "content": content
    }

def generate_travis_config(platform_config):
    """Generate Travis CI configuration"""
    project_type = platform_config.get("project_type", "nodejs")
    deployment_platform = platform_config.get("deployment_platform", "")
    
    content = f"""language: {get_travis_language(project_type)}
{get_travis_node_version(project_type)}

script:
  - {get_travis_test_step(project_type)}

after_success:
  - {get_travis_security_step(project_type)}
  - {get_travis_build_step(project_type)}"""
    
    if deployment_platform:
        content += f"""

deploy:
  provider: script
  script: {get_travis_deploy_step(deployment_platform, platform_config)}
  on:
    branch: main"""
    
    return {
        "filename": ".travis.yml",
        "content": content
    }

def generate_azure_devops_pipeline(platform_config):
    """Generate Azure DevOps pipeline configuration"""
    project_type = platform_config.get("project_type", "nodejs")
    deployment_platform = platform_config.get("deployment_platform", "")
    
    content = f"""trigger:
  - main
  - develop

pool:
  vmImage: 'ubuntu-latest'

variables:
  nodeVersion: '{get_node_version(project_type)}'

stages:
- stage: Test
  displayName: 'Test Stage'
  jobs:
  - job: Test
    displayName: 'Run Tests'
    steps:
    - task: NodeTool@0
      inputs:
        versionSpec: '$(nodeVersion)'
      displayName: 'Install Node.js'
    
    - script: |
        {get_azure_test_step(project_type)}
      displayName: 'Run Tests'
    
    - script: |
        {get_azure_security_step(project_type)}
      displayName: 'Security Scan'
    
    - script: |
        {get_azure_build_step(project_type)}
      displayName: 'Build Project'"""
    
    if deployment_platform:
        content += f"""

- stage: Deploy
  displayName: 'Deploy Stage'
  dependsOn: Test
  condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
  jobs:
  - job: Deploy
    displayName: 'Deploy Application'
    steps:
    - script: |
        {get_azure_deploy_step(deployment_platform, platform_config)}
      displayName: 'Deploy to {deployment_platform.title()}'"""
    
    return {
        "filename": "azure-pipelines.yml",
        "content": content
    }

def generate_drone_config(platform_config):
    """Generate Drone CI configuration"""
    project_type = platform_config.get("project_type", "nodejs")
    deployment_platform = platform_config.get("deployment_platform", "")
    
    content = f"""kind: pipeline
type: docker
name: build-and-test

steps:
- name: test
  image: node:{get_node_version(project_type)}
  commands:
    - {get_drone_test_step(project_type)}

- name: security
  image: node:{get_node_version(project_type)}
  commands:
    - {get_drone_security_step(project_type)}

- name: build
  image: node:{get_node_version(project_type)}
  commands:
    - {get_drone_build_step(project_type)}"""
    
    if deployment_platform:
        content += f"""

- name: deploy
  image: alpine:latest
  commands:
    - {get_drone_deploy_step(deployment_platform, platform_config)}
  when:
    branch:
      - main"""
    
    return {
        "filename": ".drone.yml",
        "content": content
    }

def generate_woodpecker_config(platform_config):
    """Generate Woodpecker CI configuration"""
    project_type = platform_config.get("project_type", "nodejs")
    deployment_platform = platform_config.get("deployment_platform", "")
    
    content = f"""pipeline:
  test:
    image: node:{get_node_version(project_type)}
    commands:
      - {get_woodpecker_test_step(project_type)}
  
  security:
    image: node:{get_node_version(project_type)}
    commands:
      - {get_woodpecker_security_step(project_type)}
  
  build:
    image: node:{get_node_version(project_type)}
    commands:
      - {get_woodpecker_build_step(project_type)}"""
    
    if deployment_platform:
        content += f"""
  
  deploy:
    image: alpine:latest
    commands:
      - {get_woodpecker_deploy_step(deployment_platform, platform_config)}
    when:
      branch: main"""
    
    return {
        "filename": ".woodpecker.yml",
        "content": content
    } 

def get_node_version(project_type):
    """Get appropriate Node.js version for project type"""
    if project_type == "nodejs":
        return "18"
    elif project_type == "python":
        return "18"  # For frontend tools
    else:
        return "18"

def get_gitlab_install_step(project_type):
    """Get GitLab CI install step"""
    if project_type == "nodejs":
        return "npm ci"
    elif project_type == "python":
        return """python -m pip install --upgrade pip
        pip install -r requirements.txt"""
    else:
        return "npm ci"

def get_gitlab_test_step(project_type):
    """Get GitLab CI test step"""
    if project_type == "nodejs":
        return "npm test"
    elif project_type == "python":
        return "pytest"
    else:
        return "npm test"

def get_gitlab_security_step(project_type):
    """Get GitLab CI security step"""
    if project_type == "nodejs":
        return "npm audit"
    elif project_type == "python":
        return "safety check"
    else:
        return "npm audit"

def get_gitlab_build_step(project_type):
    """Get GitLab CI build step"""
    if project_type == "nodejs":
        return "npm run build"
    elif project_type == "python":
        return "echo 'Python build completed'"
    else:
        return "npm run build"

def get_gitlab_deploy_step(platform, config):
    """Get GitLab CI deploy step"""
    if platform == "vercel":
        return "npx vercel --prod --token $VERCEL_TOKEN"
    elif platform == "railway":
        return "curl -X POST https://api.railway.app/v2/projects/$RAILWAY_PROJECT_ID/deployments -H 'Authorization: Bearer $RAILWAY_TOKEN'"
    else:
        return "echo 'Deployment not configured'"

def get_jenkins_test_step(project_type):
    """Get Jenkins test step"""
    if project_type == "nodejs":
        return """sh 'npm ci'
        sh 'npm test'"""
    elif project_type == "python":
        return """sh 'pip install -r requirements.txt'
        sh 'pytest'"""
    else:
        return """sh 'npm ci'
        sh 'npm test'"""

def get_jenkins_security_step(project_type):
    """Get Jenkins security step"""
    if project_type == "nodejs":
        return "sh 'npm audit'"
    elif project_type == "python":
        return "sh 'safety check'"
    else:
        return "sh 'npm audit'"

def get_jenkins_build_step(project_type):
    """Get Jenkins build step"""
    if project_type == "nodejs":
        return "sh 'npm run build'"
    elif project_type == "python":
        return "echo 'Python build completed'"
    else:
        return "sh 'npm run build'"

def get_jenkins_deploy_step(platform, config):
    """Get Jenkins deploy step"""
    if platform == "vercel":
        return "sh 'npx vercel --prod --token $VERCEL_TOKEN'"
    else:
        return "echo 'Deployment not configured'"

def get_circleci_test_step(project_type):
    """Get CircleCI test step"""
    if project_type == "nodejs":
        return "npm test"
    elif project_type == "python":
        return "pytest"
    else:
        return "npm test"

def get_circleci_security_step(project_type):
    """Get CircleCI security step"""
    if project_type == "nodejs":
        return "npm audit"
    elif project_type == "python":
        return "safety check"
    else:
        return "npm audit"

def get_circleci_build_step(project_type):
    """Get CircleCI build step"""
    if project_type == "nodejs":
        return "npm run build"
    elif project_type == "python":
        return "echo 'Python build completed'"
    else:
        return "npm run build"

def get_circleci_deploy_step(platform, config):
    """Get CircleCI deploy step"""
    if platform == "vercel":
        return "npx vercel --prod --token $VERCEL_TOKEN"
    else:
        return "echo 'Deployment not configured'"

def get_travis_language(project_type):
    """Get Travis CI language"""
    if project_type == "nodejs":
        return "node_js"
    elif project_type == "python":
        return "python"
    else:
        return "node_js"

def get_travis_node_version(project_type):
    """Get Travis CI Node.js version"""
    if project_type == "nodejs":
        return "node_js:\n  - 18"
    else:
        return ""

def get_travis_test_step(project_type):
    """Get Travis CI test step"""
    if project_type == "nodejs":
        return "npm test"
    elif project_type == "python":
        return "pytest"
    else:
        return "npm test"

def get_travis_security_step(project_type):
    """Get Travis CI security step"""
    if project_type == "nodejs":
        return "npm audit"
    elif project_type == "python":
        return "safety check"
    else:
        return "npm audit"

def get_travis_build_step(project_type):
    """Get Travis CI build step"""
    if project_type == "nodejs":
        return "npm run build"
    elif project_type == "python":
        return "echo 'Python build completed'"
    else:
        return "npm run build"

def get_travis_deploy_step(platform, config):
    """Get Travis CI deploy step"""
    if platform == "vercel":
        return "npx vercel --prod --token $VERCEL_TOKEN"
    else:
        return "echo 'Deployment not configured'"

def get_azure_test_step(project_type):
    """Get Azure DevOps test step"""
    if project_type == "nodejs":
        return "npm ci && npm test"
    elif project_type == "python":
        return "pip install -r requirements.txt && pytest"
    else:
        return "npm ci && npm test"

def get_azure_security_step(project_type):
    """Get Azure DevOps security step"""
    if project_type == "nodejs":
        return "npm audit"
    elif project_type == "python":
        return "safety check"
    else:
        return "npm audit"

def get_azure_build_step(project_type):
    """Get Azure DevOps build step"""
    if project_type == "nodejs":
        return "npm run build"
    elif project_type == "python":
        return "echo 'Python build completed'"
    else:
        return "npm run build"

def get_azure_deploy_step(platform, config):
    """Get Azure DevOps deploy step"""
    if platform == "vercel":
        return "npx vercel --prod --token $(VERCEL_TOKEN)"
    else:
        return "echo 'Deployment not configured'"

def get_drone_test_step(project_type):
    """Get Drone CI test step"""
    if project_type == "nodejs":
        return "npm ci && npm test"
    elif project_type == "python":
        return "pip install -r requirements.txt && pytest"
    else:
        return "npm ci && npm test"

def get_drone_security_step(project_type):
    """Get Drone CI security step"""
    if project_type == "nodejs":
        return "npm audit"
    elif project_type == "python":
        return "safety check"
    else:
        return "npm audit"

def get_drone_build_step(project_type):
    """Get Drone CI build step"""
    if project_type == "nodejs":
        return "npm run build"
    elif project_type == "python":
        return "echo 'Python build completed'"
    else:
        return "npm run build"

def get_drone_deploy_step(platform, config):
    """Get Drone CI deploy step"""
    if platform == "vercel":
        return "npx vercel --prod --token $VERCEL_TOKEN"
    else:
        return "echo 'Deployment not configured'"

def get_woodpecker_test_step(project_type):
    """Get Woodpecker CI test step"""
    if project_type == "nodejs":
        return "npm ci && npm test"
    elif project_type == "python":
        return "pip install -r requirements.txt && pytest"
    else:
        return "npm ci && npm test"

def get_woodpecker_security_step(project_type):
    """Get Woodpecker CI security step"""
    if project_type == "nodejs":
        return "npm audit"
    elif project_type == "python":
        return "safety check"
    else:
        return "npm audit"

def get_woodpecker_build_step(project_type):
    """Get Woodpecker CI build step"""
    if project_type == "nodejs":
        return "npm run build"
    elif project_type == "python":
        return "echo 'Python build completed'"
    else:
        return "npm run build"

def get_woodpecker_deploy_step(platform, config):
    """Get Woodpecker CI deploy step"""
    if platform == "vercel":
        return "npx vercel --prod --token $VERCEL_TOKEN"
    else:
        return "echo 'Deployment not configured'" 

# Platform Integration Endpoints
@app.get("/api/platforms/connect/{platform}")
def connect_platform(request: Request, platform: str):
    """Initiate OAuth connection to a platform"""
    platform_configs = {
        "vercel": {
            "auth_url": "https://vercel.com/oauth/authorize",
            "client_id": os.getenv("VERCEL_CLIENT_ID"),
            "scope": "read:user,read:email,deploy",
            "redirect_uri": f"{BASE_URL}/platforms/callback/vercel"
        },
        "railway": {
            "auth_url": "https://railway.app/oauth/authorize",
            "client_id": os.getenv("RAILWAY_CLIENT_ID"),
            "scope": "read:user,read:email,deploy",
            "redirect_uri": f"{BASE_URL}/platforms/callback/railway"
        },
        "netlify": {
            "auth_url": "https://app.netlify.com/authorize",
            "client_id": os.getenv("NETLIFY_CLIENT_ID"),
            "scope": "read:user,read:email,deploy",
            "redirect_uri": f"{BASE_URL}/platforms/callback/netlify"
        },
        "heroku": {
            "auth_url": "https://id.heroku.com/oauth/authorize",
            "client_id": os.getenv("HEROKU_CLIENT_ID"),
            "scope": "read,write",
            "redirect_uri": f"{BASE_URL}/platforms/callback/heroku"
        },
        "circleci": {
            "auth_url": "https://circleci.com/oauth/authorize",
            "client_id": os.getenv("CIRCLECI_CLIENT_ID"),
            "scope": "read:user,read:email,write:project",
            "redirect_uri": f"{BASE_URL}/platforms/callback/circleci"
        },
        "travis": {
            "auth_url": "https://api.travis-ci.com/auth/authorize",
            "client_id": os.getenv("TRAVIS_CLIENT_ID"),
            "scope": "read:user,read:email,write:repo",
            "redirect_uri": f"{BASE_URL}/platforms/callback/travis"
        }
    }
    
    if platform not in platform_configs:
        raise HTTPException(status_code=400, detail=f"Platform {platform} not supported")
    
    config = platform_configs[platform]
    if not config["client_id"]:
        raise HTTPException(status_code=400, detail=f"{platform.title()} integration not configured")
    
    # Store platform connection state
    request.session[f"{platform}_connect_state"] = str(uuid.uuid4())
    
    auth_url = f"{config['auth_url']}?client_id={config['client_id']}&redirect_uri={config['redirect_uri']}&scope={config['scope']}&state={request.session[f'{platform}_connect_state']}"
    
    return {"auth_url": auth_url}

@app.get("/api/platforms/callback/{platform}")
def platform_callback(request: Request, platform: str, code: str, state: str):
    """Handle OAuth callback from platforms"""
    # Verify state
    stored_state = request.session.get(f"{platform}_connect_state")
    if not stored_state or stored_state != state:
        raise HTTPException(status_code=400, detail="Invalid state parameter")
    
    # Exchange code for token
    token = exchange_platform_token(platform, code)
    
    # Store token securely
    request.session[f"{platform}_token"] = token
    
    # Redirect back to frontend
    return RedirectResponse(url=f"{FRONTEND_URL}?platform_connected={platform}")

@app.get("/api/platforms/status")
def get_platform_status(request: Request):
    """Get status of connected platforms"""
    connected_platforms = {}
    
    platforms = ["vercel", "railway", "netlify", "heroku", "circleci", "travis", "github"]
    
    for platform in platforms:
        token = request.session.get(f"{platform}_token")
        if token:
            # Verify token is still valid
            if verify_platform_token(platform, token):
                connected_platforms[platform] = {
                    "connected": True,
                    "username": get_platform_username(platform, token)
                }
            else:
                # Token expired, remove it
                request.session.pop(f"{platform}_token", None)
                connected_platforms[platform] = {"connected": False}
        else:
            connected_platforms[platform] = {"connected": False}
    
    return connected_platforms

@app.post("/api/platforms/disconnect/{platform}")
def disconnect_platform(request: Request, platform: str):
    """Disconnect from a platform"""
    request.session.pop(f"{platform}_token", None)
    request.session.pop(f"{platform}_connect_state", None)
    return {"status": "disconnected"}

@app.post("/api/platforms/setup/{platform}")
def setup_platform(request: Request, platform: str, project_config: dict):
    """Set up a platform for a specific project"""
    token = request.session.get(f"{platform}_token")
    if not token:
        raise HTTPException(status_code=401, detail=f"Not connected to {platform}")
    
    # Platform-specific setup
    if platform == "vercel":
        return setup_vercel_project(token, project_config)
    elif platform == "railway":
        return setup_railway_project(token, project_config)
    elif platform == "netlify":
        return setup_netlify_project(token, project_config)
    elif platform == "heroku":
        return setup_heroku_project(token, project_config)
    elif platform == "circleci":
        return setup_circleci_project(token, project_config)
    elif platform == "travis":
        return setup_travis_project(token, project_config)
    else:
        raise HTTPException(status_code=400, detail=f"Platform {platform} setup not implemented")

def exchange_platform_token(platform: str, code: str) -> str:
    """Exchange authorization code for access token"""
    platform_configs = {
        "vercel": {
            "token_url": "https://api.vercel.com/v2/oauth/access_token",
            "client_id": os.getenv("VERCEL_CLIENT_ID"),
            "client_secret": os.getenv("VERCEL_CLIENT_SECRET")
        },
        "railway": {
            "token_url": "https://railway.app/oauth/token",
            "client_id": os.getenv("RAILWAY_CLIENT_ID"),
            "client_secret": os.getenv("RAILWAY_CLIENT_SECRET")
        },
        "netlify": {
            "token_url": "https://api.netlify.com/oauth/token",
            "client_id": os.getenv("NETLIFY_CLIENT_ID"),
            "client_secret": os.getenv("NETLIFY_CLIENT_SECRET")
        },
        "heroku": {
            "token_url": "https://id.heroku.com/oauth/token",
            "client_id": os.getenv("HEROKU_CLIENT_ID"),
            "client_secret": os.getenv("HEROKU_CLIENT_SECRET")
        },
        "circleci": {
            "token_url": "https://circleci.com/oauth/token",
            "client_id": os.getenv("CIRCLECI_CLIENT_ID"),
            "client_secret": os.getenv("CIRCLECI_CLIENT_SECRET")
        },
        "travis": {
            "token_url": "https://api.travis-ci.com/auth/token",
            "client_id": os.getenv("TRAVIS_CLIENT_ID"),
            "client_secret": os.getenv("TRAVIS_CLIENT_SECRET")
        }
    }
    
    config = platform_configs[platform]
    data = {
        "client_id": config["client_id"],
        "client_secret": config["client_secret"],
        "code": code,
        "grant_type": "authorization_code"
    }
    
    response = requests.post(config["token_url"], data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise HTTPException(status_code=400, detail=f"Failed to get {platform} token")

def verify_platform_token(platform: str, token: str) -> bool:
    """Verify if a platform token is still valid"""
    try:
        if platform == "vercel":
            response = requests.get("https://api.vercel.com/v2/user", headers={"Authorization": f"Bearer {token}"})
        elif platform == "railway":
            response = requests.get("https://railway.app/api/v2/user", headers={"Authorization": f"Bearer {token}"})
        elif platform == "netlify":
            response = requests.get("https://api.netlify.com/api/v1/user", headers={"Authorization": f"Bearer {token}"})
        elif platform == "heroku":
            response = requests.get("https://api.heroku.com/account", headers={"Authorization": f"Bearer {token}"})
        elif platform == "circleci":
            response = requests.get("https://circleci.com/api/v2/me", headers={"Authorization": f"Bearer {token}"})
        elif platform == "travis":
            response = requests.get("https://api.travis-ci.com/user", headers={"Authorization": f"Bearer {token}"})
        else:
            return False
        
        return response.status_code == 200
    except:
        return False

def get_platform_username(platform: str, token: str) -> str:
    """Get username from platform API"""
    try:
        if platform == "vercel":
            response = requests.get("https://api.vercel.com/v2/user", headers={"Authorization": f"Bearer {token}"})
            return response.json().get("user", {}).get("username", "Unknown")
        elif platform == "railway":
            response = requests.get("https://railway.app/api/v2/user", headers={"Authorization": f"Bearer {token}"})
            return response.json().get("user", {}).get("name", "Unknown")
        elif platform == "netlify":
            response = requests.get("https://api.netlify.com/api/v1/user", headers={"Authorization": f"Bearer {token}"})
            return response.json().get("full_name", "Unknown")
        elif platform == "heroku":
            response = requests.get("https://api.heroku.com/account", headers={"Authorization": f"Bearer {token}"})
            return response.json().get("email", "Unknown")
        elif platform == "circleci":
            response = requests.get("https://circleci.com/api/v2/me", headers={"Authorization": f"Bearer {token}"})
            return response.json().get("login", "Unknown")
        elif platform == "travis":
            response = requests.get("https://api.travis-ci.com/user", headers={"Authorization": f"Bearer {token}"})
            return response.json().get("login", "Unknown")
        else:
            return "Unknown"
    except:
        return "Unknown"

def setup_vercel_project(token: str, config: dict) -> dict:
    """Set up Vercel project"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create project
    project_data = {
        "name": config.get("name"),
        "framework": config.get("framework", "other"),
        "public": config.get("public", False)
    }
    
    response = requests.post("https://api.vercel.com/v9/projects", json=project_data, headers=headers)
    
    if response.status_code == 200:
        project = response.json()
        return {
            "status": "success",
            "project_id": project["id"],
            "url": project["url"],
            "deployment_url": f"https://{project['name']}.vercel.app"
        }
    else:
        raise HTTPException(status_code=400, detail="Failed to create Vercel project")

def setup_railway_project(token: str, config: dict) -> dict:
    """Set up Railway project"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create project
    project_data = {
        "name": config.get("name"),
        "description": config.get("description", "")
    }
    
    response = requests.post("https://railway.app/api/v2/projects", json=project_data, headers=headers)
    
    if response.status_code == 200:
        project = response.json()
        return {
            "status": "success",
            "project_id": project["id"],
            "url": project["url"]
        }
    else:
        raise HTTPException(status_code=400, detail="Failed to create Railway project")

def setup_netlify_project(token: str, config: dict) -> dict:
    """Set up Netlify project"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create site
    site_data = {
        "name": config.get("name"),
        "custom_domain": config.get("custom_domain")
    }
    
    response = requests.post("https://api.netlify.com/api/v1/sites", json=site_data, headers=headers)
    
    if response.status_code == 200:
        site = response.json()
        return {
            "status": "success",
            "site_id": site["id"],
            "url": site["url"],
            "admin_url": site["admin_url"]
        }
    else:
        raise HTTPException(status_code=400, detail="Failed to create Netlify site")

def setup_heroku_project(token: str, config: dict) -> dict:
    """Set up Heroku app"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create app
    app_data = {
        "name": config.get("name"),
        "region": config.get("region", "us")
    }
    
    response = requests.post("https://api.heroku.com/apps", json=app_data, headers=headers)
    
    if response.status_code == 200:
        app = response.json()
        return {
            "status": "success",
            "app_id": app["id"],
            "name": app["name"],
            "url": f"https://{app['name']}.herokuapp.com"
        }
    else:
        raise HTTPException(status_code=400, detail="Failed to create Heroku app")

def setup_circleci_project(token: str, config: dict) -> dict:
    """Set up CircleCI project"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Enable project
    project_slug = f"github/{config.get('username')}/{config.get('name')}"
    
    response = requests.post(f"https://circleci.com/api/v2/project/{project_slug}/enable", headers=headers)
    
    if response.status_code == 200:
        return {
            "status": "success",
            "project_slug": project_slug,
            "url": f"https://circleci.com/gh/{config.get('username')}/{config.get('name')}"
        }
    else:
        raise HTTPException(status_code=400, detail="Failed to enable CircleCI project")

def setup_travis_project(token: str, config: dict) -> dict:
    """Set up Travis CI project"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Sync repositories
    response = requests.post("https://api.travis-ci.com/user/sync", headers=headers)
    
    if response.status_code == 200:
        return {
            "status": "success",
            "message": "Travis CI synced with GitHub repositories"
        }
    else:
        raise HTTPException(status_code=400, detail="Failed to sync Travis CI")

# --- Render API Deployment Endpoints ---

@app.post("/api/render/setup")
def setup_render_credentials(request: Request, api_key: str):
    """Store user's Render API key in session for deployment"""
    
    # Check if user is authenticated with GitHub
    github_token = request.session.get("github_token")
    if not github_token:
        raise HTTPException(status_code=401, detail="GitHub authentication required")
    
    # Validate the Render API key by testing it
    try:
        test_response = requests.get(
            "https://api.render.com/v1/services",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        
        if test_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Invalid Render API key")
        
        # Store API key in session (encrypted/secure)
        request.session["render_api_key"] = api_key
        request.session["render_verified"] = True
        
        return {
            "status": "success",
            "message": "Render API key verified and stored securely"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to verify Render API key: {str(e)}")

@app.get("/api/render/status")
def get_render_status(request: Request):
    """Check if user has Render credentials set up"""
    
    # Check if user is authenticated with GitHub
    github_token = request.session.get("github_token")
    if not github_token:
        raise HTTPException(status_code=401, detail="GitHub authentication required")
    
    render_api_key = request.session.get("render_api_key")
    render_verified = request.session.get("render_verified", False)
    
    return {
        "render_configured": bool(render_api_key and render_verified),
        "github_configured": bool(github_token)
    }

@app.post("/api/render/deploy")
def deploy_to_render(request: Request, github_repo: str, project_name: str = None, 
                    custom_env_vars: dict = None):
    """Deploy any application to Render using user's API key"""
    
    # Check if user is authenticated with GitHub
    github_token = request.session.get("github_token")
    if not github_token:
        raise HTTPException(status_code=401, detail="GitHub authentication required")
    
    # Get user's Render API key from session
    render_api_key = request.session.get("render_api_key")
    if not render_api_key:
        raise HTTPException(status_code=400, detail="Render API key not configured. Please set up your Render credentials first.")
    
    # Verify the API key is still valid
    if not request.session.get("render_verified"):
        raise HTTPException(status_code=400, detail="Render API key not verified. Please set up your Render credentials again.")
    
    try:
        from render_deployer import UniversalRenderDeployer
        
        deployer = UniversalRenderDeployer(render_api_key)
        
        # Deploy the application
        result = deployer.deploy_from_github(
            github_repo=github_repo,
            project_name=project_name,
            custom_env_vars=custom_env_vars
        )
        
        # Store deployment info in session for user to track
        user_deployments = request.session.get("user_deployments", [])
        deployment_info = {
            "id": str(uuid.uuid4()),
            "timestamp": time.time(),
            "github_repo": github_repo,
            "project_name": project_name,
            "result": result
        }
        user_deployments.append(deployment_info)
        request.session["user_deployments"] = user_deployments[-10:]  # Keep last 10 deployments
        
        return {
            "status": "success",
            "message": "Application deployed successfully",
            "deployment": result,
            "deployment_id": deployment_info["id"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deployment failed: {str(e)}")

@app.post("/api/render/deploy-analyzed")
def deploy_analyzed_project(request: Request, repo_url: str, project_name: str, 
                           app_config: dict, custom_env_vars: dict = None):
    """Deploy a project with pre-analyzed configuration using user's API key"""
    
    # Check if user is authenticated with GitHub
    github_token = request.session.get("github_token")
    if not github_token:
        raise HTTPException(status_code=401, detail="GitHub authentication required")
    
    # Get user's Render API key from session
    render_api_key = request.session.get("render_api_key")
    if not render_api_key:
        raise HTTPException(status_code=400, detail="Render API key not configured. Please set up your Render credentials first.")
    
    try:
        from render_deployer import UniversalRenderDeployer
        
        deployer = UniversalRenderDeployer(render_api_key)
        
        # Deploy the application with custom configuration
        result = deployer.deploy_application(
            repo_url=repo_url,
            project_name=project_name,
            app_config=app_config,
            custom_env_vars=custom_env_vars
        )
        
        # Store deployment info in session
        user_deployments = request.session.get("user_deployments", [])
        deployment_info = {
            "id": str(uuid.uuid4()),
            "timestamp": time.time(),
            "repo_url": repo_url,
            "project_name": project_name,
            "result": result
        }
        user_deployments.append(deployment_info)
        request.session["user_deployments"] = user_deployments[-10:]
        
        return {
            "status": "success",
            "message": "Application deployed successfully",
            "deployment": result,
            "deployment_id": deployment_info["id"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deployment failed: {str(e)}")

@app.get("/api/render/services")
def list_render_services(request: Request):
    """List all Render services for the authenticated user"""
    
    # Check if user is authenticated with GitHub
    github_token = request.session.get("github_token")
    if not github_token:
        raise HTTPException(status_code=401, detail="GitHub authentication required")
    
    # Get user's Render API key from session
    render_api_key = request.session.get("render_api_key")
    if not render_api_key:
        raise HTTPException(status_code=400, detail="Render API key not configured. Please set up your Render credentials first.")
    
    try:
        from render_deployer import RenderDeployer
        
        deployer = RenderDeployer(render_api_key)
        services = deployer.list_services()
        
        return {
            "status": "success",
            "services": services
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list services: {str(e)}")

@app.get("/api/render/services/{service_id}")
def get_render_service(request: Request, service_id: str):
    """Get details of a specific Render service for the authenticated user"""
    
    # Check if user is authenticated with GitHub
    github_token = request.session.get("github_token")
    if not github_token:
        raise HTTPException(status_code=401, detail="GitHub authentication required")
    
    # Get user's Render API key from session
    render_api_key = request.session.get("render_api_key")
    if not render_api_key:
        raise HTTPException(status_code=400, detail="Render API key not configured. Please set up your Render credentials first.")
    
    try:
        from render_deployer import RenderDeployer
        
        deployer = RenderDeployer(render_api_key)
        service = deployer.get_service(service_id)
        
        return {
            "status": "success",
            "service": service
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get service: {str(e)}")

@app.post("/api/render/services/{service_id}/deploy")
def deploy_render_service(request: Request, service_id: str):
    """Trigger a deployment for a specific Render service"""
    
    # Check if user is authenticated with GitHub
    github_token = request.session.get("github_token")
    if not github_token:
        raise HTTPException(status_code=401, detail="GitHub authentication required")
    
    # Get user's Render API key from session
    render_api_key = request.session.get("render_api_key")
    if not render_api_key:
        raise HTTPException(status_code=400, detail="Render API key not configured. Please set up your Render credentials first.")
    
    try:
        from render_deployer import RenderDeployer
        
        deployer = RenderDeployer(render_api_key)
        deployment = deployer.deploy_service(service_id)
        
        return {
            "status": "success",
            "message": "Deployment triggered successfully",
            "deployment": deployment
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to trigger deployment: {str(e)}")

@app.get("/api/render/deployments/{service_id}/{deploy_id}")
def get_deployment_status(request: Request, service_id: str, deploy_id: str):
    """Get the status of a specific deployment"""
    
    # Check if user is authenticated with GitHub
    github_token = request.session.get("github_token")
    if not github_token:
        raise HTTPException(status_code=401, detail="GitHub authentication required")
    
    # Get user's Render API key from session
    render_api_key = request.session.get("render_api_key")
    if not render_api_key:
        raise HTTPException(status_code=400, detail="Render API key not configured. Please set up your Render credentials first.")
    
    try:
        from render_deployer import RenderDeployer
        
        deployer = RenderDeployer(render_api_key)
        status = deployer.get_deployment_status(service_id, deploy_id)
        
        return {
            "status": "success",
            "deployment_status": status
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get deployment status: {str(e)}")

@app.get("/api/render/my-deployments")
def get_user_deployments(request: Request):
    """Get deployment history for the current user"""
    
    # Check if user is authenticated with GitHub
    github_token = request.session.get("github_token")
    if not github_token:
        raise HTTPException(status_code=401, detail="GitHub authentication required")
    
    user_deployments = request.session.get("user_deployments", [])
    
    return {
        "status": "success",
        "deployments": user_deployments
    }

@app.post("/api/render/analyze")
def analyze_for_render_deployment(request: Request, files: List[UploadFile] = File(...)):
    """Analyze uploaded files to determine optimal Render deployment configuration"""
    
    # Check if user is authenticated with GitHub
    github_token = request.session.get("github_token")
    if not github_token:
        raise HTTPException(status_code=401, detail="GitHub authentication required")
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Save all files to temp directory
        for file in files:
            path_parts = file.filename.split('/')
            if len(path_parts) > 1:
                relative_path = '/'.join(path_parts[1:])
            else:
                relative_path = file.filename
            
            file_path = os.path.join(temp_dir, relative_path)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "wb") as f:
                shutil.copyfileobj(file.file, f)
        
        # Analyze the project
        from render_deployer import UniversalRenderDeployer
        
        deployer = UniversalRenderDeployer("dummy_key")  # We only need analysis, not deployment
        app_config = deployer.detect_application_type(temp_dir)
        
        # Generate suggested configurations
        backend_config = None
        frontend_config = None
        
        if app_config.get("backend"):
            backend_config = deployer.generate_backend_config(app_config["backend"], "project-name")
        
        if app_config.get("frontend"):
            frontend_config = deployer.generate_frontend_config(app_config["frontend"], "project-name")
        
        return {
            "status": "success",
            "analysis": app_config,
            "suggested_configs": {
                "backend": backend_config.__dict__ if backend_config else None,
                "frontend": frontend_config.__dict__ if frontend_config else None
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    
    finally:
        # Clean up temp directory
        shutil.rmtree(temp_dir, ignore_errors=True)

@app.post("/api/render/clear-credentials")
def clear_render_credentials(request: Request):
    """Clear user's Render API key from session"""
    
    # Check if user is authenticated with GitHub
    github_token = request.session.get("github_token")
    if not github_token:
        raise HTTPException(status_code=401, detail="GitHub authentication required")
    
    # Clear Render credentials from session
    request.session.pop("render_api_key", None)
    request.session.pop("render_verified", None)
    
    return {
        "status": "success",
        "message": "Render credentials cleared from session"
    }

# --- Render OAuth-like Authentication Endpoints ---

@app.get("/api/auth/render/login")
def render_login():
    """Initiate Render authentication flow - redirects to Render dashboard"""
    # Redirect to Render API key page with instructions
    render_api_url = "https://dashboard.render.com/account/api-keys"
    
    # Store state for verification
    state = str(uuid.uuid4())
    
    return {
        "auth_url": render_api_url,
        "state": state,
        "instructions": {
            "title": "Get Your Render API Key",
            "steps": [
                "1. Click the link above to go to your Render dashboard",
                "2. Navigate to Account → API Keys",
                "3. Click 'Create API Key'",
                "4. Give it a name like 'GitHub Uploader'",
                "5. Copy the generated API key (starts with 'rnd_')",
                "6. Return here and paste it in the setup form"
            ]
        }
    }

@app.post("/api/auth/render/verify")
def verify_render_api_key(request: Request, api_key: str):
    """Verify and store Render API key (OAuth-like flow)"""
    
    # Check if user is authenticated with GitHub
    github_token = request.session.get("github_token")
    if not github_token:
        raise HTTPException(status_code=401, detail="GitHub authentication required")
    
    # Validate the Render API key format
    if not api_key.startswith("rnd_"):
        raise HTTPException(status_code=400, detail="Invalid API key format. Render API keys start with 'rnd_'")
    
    # Test the API key by making a request to Render API
    try:
        test_response = requests.get(
            "https://api.render.com/v1/services",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        
        if test_response.status_code == 401:
            raise HTTPException(status_code=400, detail="Invalid API key. Please check your key and try again.")
        elif test_response.status_code == 403:
            raise HTTPException(status_code=400, detail="API key doesn't have required permissions. Please create a new key with full access.")
        elif test_response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"API key validation failed. Status: {test_response.status_code}")
        
        # Get user info from Render API
        user_response = requests.get(
            "https://api.render.com/v1/user",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        
        user_info = {}
        if user_response.status_code == 200:
            user_data = user_response.json()
            user_info = {
                "email": user_data.get("email"),
                "name": user_data.get("name"),
                "account_id": user_data.get("account_id")
            }
        
        # Store API key and user info in session
        request.session["render_api_key"] = api_key
        request.session["render_verified"] = True
        request.session["render_user_info"] = user_info
        
        return {
            "status": "success",
            "message": "Render authentication successful!",
            "user_info": user_info
        }
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to verify API key: {str(e)}")

@app.get("/api/auth/render/status")
def get_render_auth_status(request: Request):
    """Check Render authentication status"""
    
    # Check if user is authenticated with GitHub
    github_token = request.session.get("github_token")
    if not github_token:
        raise HTTPException(status_code=401, detail="GitHub authentication required")
    
    render_api_key = request.session.get("render_api_key")
    render_verified = request.session.get("render_verified", False)
    render_user_info = request.session.get("render_user_info", {})
    
    return {
        "render_authenticated": bool(render_api_key and render_verified),
        "github_authenticated": bool(github_token),
        "user_info": render_user_info if render_verified else None
    }

@app.post("/api/auth/render/logout")
def render_logout(request: Request):
    """Clear Render authentication"""
    
    # Check if user is authenticated with GitHub
    github_token = request.session.get("github_token")
    if not github_token:
        raise HTTPException(status_code=401, detail="GitHub authentication required")
    
    # Clear Render credentials
    request.session.pop("render_api_key", None)
    request.session.pop("render_verified", None)
    request.session.pop("render_user_info", None)
    
    return {
        "status": "success",
        "message": "Render authentication cleared"
    }