import os
import requests
import json
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class ServiceType(Enum):
    WEB = "web"
    STATIC = "static"
    BACKGROUND = "background"
    CRON = "cron"


@dataclass
class RenderServiceConfig:
    name: str
    service_type: ServiceType
    environment: str  # python, node, static, etc.
    build_command: str
    start_command: Optional[str] = None
    root_directory: Optional[str] = None
    static_publish_path: Optional[str] = None
    env_vars: Optional[Dict[str, str]] = None
    auto_deploy: bool = True
    branch: str = "main"


class RenderDeployer:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.render.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def create_service(
        self, config: RenderServiceConfig, repo_url: str
    ) -> Dict[str, Any]:
        """Create a new service on Render"""

        service_data = {
            "name": config.name,
            "type": config.service_type.value,
            "env": config.environment,
            "buildCommand": config.build_command,
            "autoDeploy": config.auto_deploy,
            "branch": config.branch,
            "repo": repo_url,
        }

        if config.start_command:
            service_data["startCommand"] = config.start_command

        if config.root_directory:
            service_data["rootDir"] = config.root_directory

        if config.static_publish_path:
            service_data["staticPublishPath"] = config.static_publish_path

        response = requests.post(
            f"{self.base_url}/services", headers=self.headers, json=service_data
        )

        if response.status_code == 201:
            service = response.json()

            # Set environment variables if provided
            if config.env_vars:
                self.set_environment_variables(service["id"], config.env_vars)

            return service
        else:
            raise Exception(f"Failed to create service: {response.text}")

    def set_environment_variables(self, service_id: str, env_vars: Dict[str, str]):
        """Set environment variables for a service"""
        for key, value in env_vars.items():
            response = requests.post(
                f"{self.base_url}/services/{service_id}/env-vars",
                headers=self.headers,
                json={"key": key, "value": value},
            )

            if response.status_code not in [200, 201]:
                print(f"Warning: Failed to set env var {key}: {response.text}")

    def get_service(self, service_id: str) -> Dict[str, Any]:
        """Get service details"""
        response = requests.get(
            f"{self.base_url}/services/{service_id}", headers=self.headers
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get service: {response.text}")

    def list_services(self) -> List[Dict[str, Any]]:
        """List all services"""
        response = requests.get(f"{self.base_url}/services", headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to list services: {response.text}")

    def deploy_service(self, service_id: str) -> Dict[str, Any]:
        """Trigger a deployment for a service"""
        response = requests.post(
            f"{self.base_url}/services/{service_id}/deploys", headers=self.headers
        )

        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to deploy service: {response.text}")

    def get_deployment_status(self, service_id: str, deploy_id: str) -> Dict[str, Any]:
        """Get deployment status"""
        response = requests.get(
            f"{self.base_url}/services/{service_id}/deploys/{deploy_id}",
            headers=self.headers,
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get deployment status: {response.text}")

    def wait_for_deployment(
        self, service_id: str, deploy_id: str, timeout: int = 600
    ) -> str:
        """Wait for deployment to complete and return final status"""
        start_time = time.time()

        while time.time() - start_time < timeout:
            status = self.get_deployment_status(service_id, deploy_id)
            deploy_status = status.get("status", "unknown")

            if deploy_status in ["live", "failed", "canceled"]:
                return deploy_status

            time.sleep(10)  # Wait 10 seconds before checking again

        return "timeout"


class UniversalRenderDeployer:
    """Universal Render deployment system for any application"""

    def __init__(self, api_key: str):
        self.render = RenderDeployer(api_key)

    def detect_application_type(self, project_path: str) -> Dict[str, Any]:
        """Detect application type and generate appropriate configuration"""
        import os

        files = os.listdir(project_path)
        config = {"backend": None, "frontend": None, "type": "unknown"}

        # Check for common backend patterns
        backend_indicators = {
            "python": ["requirements.txt", "pyproject.toml", "main.py", "app.py"],
            "node": ["package.json", "server.js", "index.js"],
            "java": ["pom.xml", "build.gradle", "src/main/java"],
            "go": ["go.mod", "go.sum", "main.go"],
            "rust": ["Cargo.toml", "Cargo.lock", "src/main.rs"],
            "php": ["composer.json", "index.php"],
            "ruby": ["Gemfile", "config.ru"],
            "dotnet": ["*.csproj", "*.vbproj", "Program.cs"],
        }

        # Check for frontend patterns
        frontend_indicators = {
            "react": ["package.json", "src/App.js", "src/App.tsx"],
            "vue": ["package.json", "src/main.js", "src/App.vue"],
            "angular": ["package.json", "angular.json", "src/app"],
            "next": ["package.json", "next.config.js", "pages", "app"],
            "nuxt": ["package.json", "nuxt.config.js", "pages"],
            "static": ["index.html", "index.htm", "public"],
        }

        # Detect backend type
        for lang, indicators in backend_indicators.items():
            if any(indicator in files for indicator in indicators):
                config["backend"] = lang
                break

        # Detect frontend type
        for framework, indicators in frontend_indicators.items():
            if any(indicator in files for indicator in indicators):
                config["frontend"] = framework
                break

        # Determine overall type
        if config["backend"] and config["frontend"]:
            config["type"] = "fullstack"
        elif config["backend"]:
            config["type"] = "backend"
        elif config["frontend"]:
            config["type"] = "frontend"

        return config

    def generate_backend_config(
        self, app_type: str, project_name: str
    ) -> RenderServiceConfig:
        """Generate backend service configuration"""

        configs = {
            "python": RenderServiceConfig(
                name=f"{project_name}-backend",
                service_type=ServiceType.WEB,
                environment="python",
                build_command="pip install -r requirements.txt",
                start_command="uvicorn main:app --host 0.0.0.0 --port $PORT",
                root_directory=".",
                env_vars={"PYTHON_VERSION": "3.11.0", "ENVIRONMENT": "production"},
            ),
            "node": RenderServiceConfig(
                name=f"{project_name}-backend",
                service_type=ServiceType.WEB,
                environment="node",
                build_command="npm install",
                start_command="npm start",
                root_directory=".",
                env_vars={"NODE_ENV": "production", "PORT": "$PORT"},
            ),
            "java": RenderServiceConfig(
                name=f"{project_name}-backend",
                service_type=ServiceType.WEB,
                environment="java",
                build_command="./gradlew build",
                start_command="java -jar build/libs/*.jar",
                root_directory=".",
                env_vars={"JAVA_VERSION": "17", "PORT": "$PORT"},
            ),
            "go": RenderServiceConfig(
                name=f"{project_name}-backend",
                service_type=ServiceType.WEB,
                environment="go",
                build_command="go build -o main .",
                start_command="./main",
                root_directory=".",
                env_vars={"GO_VERSION": "1.21", "PORT": "$PORT"},
            ),
        }

        return configs.get(app_type, configs["python"])

    def generate_frontend_config(
        self, app_type: str, project_name: str
    ) -> RenderServiceConfig:
        """Generate frontend service configuration"""

        configs = {
            "react": RenderServiceConfig(
                name=f"{project_name}-frontend",
                service_type=ServiceType.STATIC,
                environment="static",
                build_command="npm install && npm run build",
                static_publish_path="./build",
                root_directory=".",
                env_vars={"NODE_VERSION": "18"},
            ),
            "vue": RenderServiceConfig(
                name=f"{project_name}-frontend",
                service_type=ServiceType.STATIC,
                environment="static",
                build_command="npm install && npm run build",
                static_publish_path="./dist",
                root_directory=".",
                env_vars={"NODE_VERSION": "18"},
            ),
            "angular": RenderServiceConfig(
                name=f"{project_name}-frontend",
                service_type=ServiceType.STATIC,
                environment="static",
                build_command="npm install && npm run build",
                static_publish_path="./dist",
                root_directory=".",
                env_vars={"NODE_VERSION": "18"},
            ),
            "next": RenderServiceConfig(
                name=f"{project_name}-frontend",
                service_type=ServiceType.WEB,
                environment="node",
                build_command="npm install && npm run build",
                start_command="npm start",
                root_directory=".",
                env_vars={"NODE_VERSION": "18", "PORT": "$PORT"},
            ),
            "static": RenderServiceConfig(
                name=f"{project_name}-frontend",
                service_type=ServiceType.STATIC,
                environment="static",
                build_command="echo 'Static site - no build required'",
                static_publish_path="./",
                root_directory=".",
                env_vars={},
            ),
        }

        return configs.get(app_type, configs["react"])

    def deploy_application(
        self,
        repo_url: str,
        project_name: str,
        app_config: Dict[str, Any],
        custom_env_vars: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Deploy an application to Render"""

        services = []

        # Deploy backend if present
        if app_config.get("backend"):
            backend_config = self.generate_backend_config(
                app_config["backend"], project_name
            )

            # Add custom environment variables
            if custom_env_vars:
                if backend_config.env_vars is None:
                    backend_config.env_vars = {}
                backend_config.env_vars.update(custom_env_vars)

            try:
                backend_service = self.render.create_service(backend_config, repo_url)
                services.append(
                    {
                        "type": "backend",
                        "service": backend_service,
                        "config": backend_config,
                    }
                )
                print(f"✅ Backend service created: {backend_service['service']['url']}")
            except Exception as e:
                print(f"❌ Failed to create backend service: {e}")

        # Deploy frontend if present
        if app_config.get("frontend"):
            frontend_config = self.generate_frontend_config(
                app_config["frontend"], project_name
            )

            # Add custom environment variables
            if custom_env_vars:
                if frontend_config.env_vars is None:
                    frontend_config.env_vars = {}
                frontend_config.env_vars.update(custom_env_vars)

            try:
                frontend_service = self.render.create_service(frontend_config, repo_url)
                services.append(
                    {
                        "type": "frontend",
                        "service": frontend_service,
                        "config": frontend_config,
                    }
                )
                print(
                    f"✅ Frontend service created: {frontend_service['service']['url']}"
                )
            except Exception as e:
                print(f"❌ Failed to create frontend service: {e}")

        return {
            "project_name": project_name,
            "app_type": app_config["type"],
            "services": services,
            "deployment_urls": {
                service["type"]: service["service"]["service"]["url"]
                for service in services
            },
        }

    def deploy_from_github(
        self,
        github_repo: str,
        project_name: Optional[str] = None,
        custom_env_vars: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Deploy directly from a GitHub repository"""

        if not project_name:
            project_name = github_repo.split("/")[-1].replace(".git", "")

        # For now, we'll use a default configuration
        # In a real implementation, you'd clone the repo and analyze it
        app_config = {"type": "fullstack", "backend": "python", "frontend": "react"}

        return self.deploy_application(
            f"https://github.com/{github_repo}",
            project_name,
            app_config,
            custom_env_vars,
        )
