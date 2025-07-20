#!/usr/bin/env python3
"""
Test Setup and Configuration
============================

This script sets up the testing environment for the RepoTorpedo application.
It installs dependencies, configures test data, and provides utilities for
running comprehensive user flow tests.
"""

import os
import sys
import subprocess
import json
import time
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TestSetup:
    """Test environment setup and configuration"""
    
    def __init__(self, project_root: str = None):
        self.project_root = project_root or Path(__file__).parent.parent
        self.test_dir = Path(__file__).parent  # Current directory (tests)
        self.config_file = self.test_dir / "test_config.json"
        self.env_file = self.test_dir / ".env.test"
        
    def check_python_version(self) -> bool:
        """Check if Python version is compatible"""
        logger.info("Checking Python version...")
        
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 7):
            logger.error(f"Python 3.7+ required, found {version.major}.{version.minor}")
            return False
        
        logger.info(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    
    def install_dependencies(self) -> bool:
        """Install test dependencies"""
        logger.info("Installing test dependencies...")
        
        dependencies = [
            "pytest",
            "pytest-cov",
            "pytest-html",
            "pytest-xdist",
            "requests",
            "flask",
            "flask-cors",
            "coverage",
            "pytest-mock",
            "pytest-asyncio"
        ]
        
        try:
            for dep in dependencies:
                logger.info(f"Installing {dep}...")
                subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                             check=True, capture_output=True)
            
            logger.info("✅ All test dependencies installed")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to install dependencies: {e}")
            return False
    
    def create_test_config(self) -> bool:
        """Create test configuration file"""
        logger.info("Creating test configuration...")
        
        config = {
            "test_environment": {
                "base_url": "http://localhost:5000",
                "mock_server_port": 5000,
                "timeout": 30,
                "retry_attempts": 3
            },
            "providers": {
                "render": {
                    "api_key": "test_render_api_key_123",
                    "config": {}
                },
                "vercel": {
                    "api_key": "test_vercel_api_key_123",
                    "config": {
                        "team_id": "test_team_id"
                    }
                },
                "netlify": {
                    "api_key": "test_netlify_api_key_123",
                    "config": {}
                },
                "railway": {
                    "api_key": "test_railway_api_key_123",
                    "config": {}
                }
            },
            "test_data": {
                "users": [
                    {
                        "email": "testuser1@example.com",
                        "password": "TestPassword123!",
                        "name": "Test User 1"
                    },
                    {
                        "email": "testuser2@example.com",
                        "password": "TestPassword456!",
                        "name": "Test User 2"
                    }
                ],
                "repositories": [
                    {
                        "url": "https://github.com/testuser/simple-react-app",
                        "type": "react",
                        "framework": "create-react-app"
                    },
                    {
                        "url": "https://github.com/testuser/node-api",
                        "type": "node",
                        "framework": "express"
                    },
                    {
                        "url": "https://github.com/testuser/python-flask-app",
                        "type": "python",
                        "framework": "flask"
                    },
                    {
                        "url": "https://github.com/testuser/static-site",
                        "type": "static",
                        "framework": "html"
                    }
                ],
                "deployments": [
                    {
                        "name": "test-app-1",
                        "environment": "node",
                        "build_command": "npm install && npm run build",
                        "start_command": "npm start",
                        "env_vars": {
                            "NODE_ENV": "production",
                            "PORT": "3000"
                        }
                    },
                    {
                        "name": "test-app-2",
                        "environment": "python",
                        "build_command": "pip install -r requirements.txt",
                        "start_command": "python app.py",
                        "env_vars": {
                            "FLASK_ENV": "production",
                            "PORT": "5000"
                        }
                    }
                ]
            },
            "test_scenarios": {
                "quick_tests": [
                    "AuthenticationFlowTests",
                    "ProviderConfigurationFlowTests",
                    "DeploymentFlowTests"
                ],
                "full_tests": [
                    "AuthenticationFlowTests",
                    "ProviderConfigurationFlowTests",
                    "DeploymentFlowTests",
                    "DeploymentStatusFlowTests",
                    "CustomDomainFlowTests",
                    "ErrorHandlingFlowTests",
                    "PerformanceFlowTests",
                    "SecurityFlowTests",
                    "IntegrationFlowTests"
                ]
            }
        }
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            logger.info(f"✅ Test configuration created: {self.config_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to create test configuration: {e}")
            return False
    
    def create_env_file(self) -> bool:
        """Create test environment file"""
        logger.info("Creating test environment file...")
        
        env_content = """# Test Environment Variables
TEST_BASE_URL=http://localhost:5000
TEST_MOCK_SERVER_PORT=5000
TEST_TIMEOUT=30
TEST_RETRY_ATTEMPTS=3

# Mock API Keys (for testing only)
TEST_RENDER_API_KEY=test_render_api_key_123
TEST_VERCEL_API_KEY=test_vercel_api_key_123
TEST_NETLIFY_API_KEY=test_netlify_api_key_123
TEST_RAILWAY_API_KEY=test_railway_api_key_123

# Test Data
TEST_USER_EMAIL=testuser@example.com
TEST_USER_PASSWORD=TestPassword123!
TEST_REPO_URL=https://github.com/testuser/test-app
TEST_PROJECT_NAME=test-project

# Test Configuration
TEST_VERBOSE=true
TEST_GENERATE_REPORTS=true
TEST_COVERAGE=true
"""
        
        try:
            with open(self.env_file, 'w') as f:
                f.write(env_content)
            
            logger.info(f"✅ Test environment file created: {self.env_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to create environment file: {e}")
            return False
    
    def create_test_repositories(self) -> bool:
        """Create test repositories for deployment testing"""
        logger.info("Creating test repositories...")
        
        test_repos_dir = self.test_dir / "test_repositories"
        test_repos_dir.mkdir(exist_ok=True)
        
        # Simple React App
        react_app_dir = test_repos_dir / "simple-react-app"
        react_app_dir.mkdir(exist_ok=True)
        
        react_files = {
            "package.json": """{
  "name": "simple-react-app",
  "version": "1.0.0",
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test"
  },
  "dependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "react-scripts": "5.0.1"
  }
}""",
            "public/index.html": """<!DOCTYPE html>
<html>
<head>
    <title>Simple React App</title>
</head>
<body>
    <div id="root"></div>
</body>
</html>""",
            "src/App.js": """import React from 'react';

function App() {
  return (
    <div>
      <h1>Hello from React!</h1>
    </div>
  );
}

export default App;""",
            "src/index.js": """import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

ReactDOM.render(<App />, document.getElementById('root'));"""
        }
        
        for file_path, content in react_files.items():
            full_path = react_app_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(content)
        
        # Simple Node.js API
        node_api_dir = test_repos_dir / "node-api"
        node_api_dir.mkdir(exist_ok=True)
        
        node_files = {
            "package.json": """{
  "name": "node-api",
  "version": "1.0.0",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "express": "^4.18.0"
  }
}""",
            "server.js": """const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.json({ message: 'Hello from Node.js API!' });
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});"""
        }
        
        for file_path, content in node_files.items():
            full_path = node_api_dir / file_path
            with open(full_path, 'w') as f:
                f.write(content)
        
        # Simple Python Flask App
        python_app_dir = test_repos_dir / "python-flask-app"
        python_app_dir.mkdir(exist_ok=True)
        
        python_files = {
            "requirements.txt": """Flask==2.0.1
gunicorn==20.1.0""",
            "app.py": """from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return {'message': 'Hello from Python Flask!'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))"""
        }
        
        for file_path, content in python_files.items():
            full_path = python_app_dir / file_path
            with open(full_path, 'w') as f:
                f.write(content)
        
        logger.info("✅ Test repositories created")
        return True
    
    def create_test_scripts(self) -> bool:
        """Create test execution scripts"""
        logger.info("Creating test execution scripts...")
        
        # Create run_tests.sh
        run_tests_sh = self.test_dir / "run_tests.sh"
        run_tests_content = """#!/bin/bash

# Test Execution Script
# Usage: ./run_tests.sh [options]

set -e

# Default values
BASE_URL="http://localhost:5000"
TEST_TYPE="quick"
VERBOSE=""
COVERAGE=""
REPORT=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --base-url)
            BASE_URL="$2"
            shift 2
            ;;
        --full)
            TEST_TYPE="full"
            shift
            ;;
        --verbose)
            VERBOSE="--verbose"
            shift
            ;;
        --coverage)
            COVERAGE="--coverage"
            shift
            ;;
        --report)
            REPORT="--report"
            shift
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --base-url URL     Base URL for testing (default: http://localhost:5000)"
            echo "  --full             Run full test suite"
            echo "  --verbose          Verbose output"
            echo "  --coverage         Run with coverage"
            echo "  --report           Generate HTML report"
            echo "  --help             Show this help"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo "🚀 Starting tests..."
echo "📍 Base URL: $BASE_URL"
echo "📋 Test Type: $TEST_TYPE"

# Check if server is running
echo "🔍 Checking server health..."
if ! curl -s "$BASE_URL/health" > /dev/null; then
    echo "❌ Server not responding at $BASE_URL"
    echo "💡 Start the server first: python3 server/main.py"
    exit 1
fi

echo "✅ Server is healthy"

# Run tests
python3 run_tests.py --base-url "$BASE_URL" $VERBOSE $COVERAGE $REPORT

echo "✅ Tests completed"
"""
        
        with open(run_tests_sh, 'w') as f:
            f.write(run_tests_content)
        
        # Make executable
        os.chmod(run_tests_sh, 0o755)
        
        # Create start_mock_server.sh
        start_mock_sh = self.test_dir / "start_mock_server.sh"
        start_mock_content = """#!/bin/bash

# Start Mock Server Script

echo "🚀 Starting mock server..."

# Check if port is available
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Port 5000 is already in use"
    echo "💡 Stopping existing process..."
    pkill -f "mock_server.py"
    sleep 2
fi

# Start mock server
python3 mock_server.py --host localhost --port 5000 &

# Wait for server to start
echo "⏳ Waiting for server to start..."
sleep 3

# Check if server is running
if curl -s "http://localhost:5000/health" > /dev/null; then
    echo "✅ Mock server is running on http://localhost:5000"
    echo "📋 Server PID: $!"
else
    echo "❌ Failed to start mock server"
    exit 1
fi

# Keep script running
wait
"""
        
        with open(start_mock_sh, 'w') as f:
            f.write(start_mock_content)
        
        os.chmod(start_mock_sh, 0o755)
        
        logger.info("✅ Test execution scripts created")
        return True
    
    def create_ci_config(self) -> bool:
        """Create CI/CD configuration for tests"""
        logger.info("Creating CI/CD configuration...")
        
        # GitHub Actions workflow
        workflows_dir = self.project_root / ".github" / "workflows"
        workflows_dir.mkdir(parents=True, exist_ok=True)
        
        workflow_file = workflows_dir / "test.yml"
        workflow_content = """name: User Flow Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10", "3.11"]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        cd tests
        python setup_tests.py --install-deps
    
    - name: Start mock server
      run: |
        cd tests
        python mock_server.py --host 0.0.0.0 --port 5000 &
        sleep 5
    
    - name: Run tests
      run: |
        cd tests
        python run_tests.py --base-url http://localhost:5000 --full --coverage --report
    
    - name: Upload test results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: test-results-${{ matrix.python-version }}
        path: |
          tests/test_report.html
          tests/htmlcov/
          tests/.coverage
"""
        
        with open(workflow_file, 'w') as f:
            f.write(workflow_content)
        
        logger.info("✅ CI/CD configuration created")
        return True
    
    def validate_setup(self) -> bool:
        """Validate the test setup"""
        logger.info("Validating test setup...")
        
        checks = [
            ("Python version", self.check_python_version()),
            ("Test configuration", self.config_file.exists()),
            ("Environment file", self.env_file.exists()),
            ("Test repositories", (self.test_dir / "test_repositories").exists()),
            ("Test scripts", (self.test_dir / "run_tests.sh").exists()),
            ("Mock server", (self.test_dir / "mock_server.py").exists()),
            ("User flow tests", (self.test_dir / "user_flows.py").exists())
        ]
        
        all_passed = True
        for check_name, passed in checks:
            status = "✅ PASS" if passed else "❌ FAIL"
            logger.info(f"{status} {check_name}")
            if not passed:
                all_passed = False
        
        if all_passed:
            logger.info("🎉 All setup checks passed!")
        else:
            logger.error("❌ Some setup checks failed")
        
        return all_passed
    
    def run_setup(self, install_deps: bool = True) -> bool:
        """Run complete test setup"""
        logger.info("🚀 Starting test setup...")
        
        steps = [
            ("Checking Python version", self.check_python_version),
            ("Installing dependencies", self.install_dependencies if install_deps else lambda: True),
            ("Creating test configuration", self.create_test_config),
            ("Creating environment file", self.create_env_file),
            ("Creating test repositories", self.create_test_repositories),
            ("Creating test scripts", self.create_test_scripts),
            ("Creating CI configuration", self.create_ci_config),
            ("Validating setup", self.validate_setup)
        ]
        
        for step_name, step_func in steps:
            logger.info(f"📋 {step_name}...")
            if not step_func():
                logger.error(f"❌ {step_name} failed")
                return False
        
        logger.info("🎉 Test setup completed successfully!")
        return True


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Setup Test Environment")
    parser.add_argument("--no-deps", action="store_true", 
                       help="Skip dependency installation")
    parser.add_argument("--validate-only", action="store_true",
                       help="Only validate existing setup")
    parser.add_argument("--project-root", 
                       help="Project root directory")
    
    args = parser.parse_args()
    
    setup = TestSetup(project_root=args.project_root)
    
    if args.validate_only:
        success = setup.validate_setup()
    else:
        success = setup.run_setup(install_deps=not args.no_deps)
    
    if success:
        print("\n📋 Next steps:")
        print("1. Start the mock server: cd tests && ./start_mock_server.sh")
        print("2. Run tests: cd tests && ./run_tests.sh")
        print("3. View test results: open tests/test_report.html")
        print("\n📚 Documentation: tests/test_scenarios.md")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main()) 