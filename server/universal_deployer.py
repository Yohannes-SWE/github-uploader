import os
import requests
import json
import time
import base64
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ServiceType(Enum):
    WEB = "web"
    STATIC = "static"
    BACKGROUND = "background"
    CRON = "cron"
    FUNCTION = "function"


class DeploymentStatus(Enum):
    PENDING = "pending"
    BUILDING = "building"
    DEPLOYING = "deploying"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class DeploymentConfig:
    name: str
    service_type: ServiceType
    environment: str  # python, node, static, etc.
    build_command: Optional[str] = None
    start_command: Optional[str] = None
    root_directory: Optional[str] = None
    static_publish_path: Optional[str] = None
    env_vars: Optional[Dict[str, str]] = None
    auto_deploy: bool = True
    branch: str = "main"
    custom_domains: Optional[List[str]] = None
    framework: Optional[str] = None  # next, react, vue, etc.


@dataclass
class DeploymentResult:
    provider: str
    service_id: str
    deployment_id: str
    url: str
    status: DeploymentStatus
    logs: Optional[str] = None
    error: Optional[str] = None


class HostingProvider(ABC):
    """Abstract base class for hosting providers"""

    def __init__(self, api_key: str, config: Optional[Dict[str, Any]] = None):
        self.api_key = api_key
        self.config = config or {}
        self.session = requests.Session()
        self.session.headers.update(self._get_headers())

    @abstractmethod
    def _get_headers(self) -> Dict[str, str]:
        """Return headers for API requests"""
        pass

    @abstractmethod
    def deploy(self, config: DeploymentConfig, repo_url: str) -> DeploymentResult:
        """Deploy application to this provider"""
        pass

    @abstractmethod
    def get_deployment_status(
        self, service_id: str, deployment_id: str
    ) -> DeploymentStatus:
        """Get deployment status"""
        pass

    @abstractmethod
    def list_deployments(self, service_id: str) -> List[Dict[str, Any]]:
        """List all deployments for a service"""
        pass

    @abstractmethod
    def add_custom_domain(self, service_id: str, domain: str) -> Dict[str, Any]:
        """Add custom domain"""
        pass


class RenderProvider(HostingProvider):
    """Render hosting provider implementation"""

    def __init__(self, api_key: str, config: Optional[Dict[str, Any]] = None):
        super().__init__(api_key, config)
        self.base_url = "https://api.render.com/v1"

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def deploy(self, config: DeploymentConfig, repo_url: str) -> DeploymentResult:
        """Deploy to Render"""
        try:
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

            response = self.session.post(f"{self.base_url}/services", json=service_data)

            if response.status_code == 201:
                service = response.json()

                # Set environment variables
                if config.env_vars:
                    self._set_environment_variables(service["id"], config.env_vars)

                # Add custom domains
                if config.custom_domains:
                    for domain in config.custom_domains:
                        self.add_custom_domain(service["id"], domain)

                return DeploymentResult(
                    provider="render",
                    service_id=service["id"],
                    deployment_id=service.get("latestDeploy", {}).get("id", ""),
                    url=service["service"]["url"],
                    status=DeploymentStatus.SUCCESS,
                )
            else:
                raise Exception(f"Failed to create Render service: {response.text}")

        except Exception as e:
            logger.error(f"Render deployment failed: {e}")
            return DeploymentResult(
                provider="render",
                service_id="",
                deployment_id="",
                url="",
                status=DeploymentStatus.FAILED,
                error=str(e),
            )

    def get_deployment_status(
        self, service_id: str, deployment_id: str
    ) -> DeploymentStatus:
        """Get Render deployment status"""
        try:
            response = self.session.get(
                f"{self.base_url}/services/{service_id}/deploys/{deployment_id}"
            )
            if response.status_code == 200:
                status = response.json().get("status", "unknown")
                return self._map_render_status(status)
            return DeploymentStatus.FAILED
        except Exception as e:
            logger.error(f"Failed to get Render deployment status: {e}")
            return DeploymentStatus.FAILED

    def list_deployments(self, service_id: str) -> List[Dict[str, Any]]:
        """List Render deployments"""
        try:
            response = self.session.get(
                f"{self.base_url}/services/{service_id}/deploys"
            )
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            logger.error(f"Failed to list Render deployments: {e}")
            return []

    def add_custom_domain(self, service_id: str, domain: str) -> Dict[str, Any]:
        """Add custom domain to Render service"""
        try:
            response = self.session.post(
                f"{self.base_url}/services/{service_id}/custom-domains",
                json={"name": domain},
            )
            if response.status_code == 201:
                return response.json()
            raise Exception(f"Failed to add domain: {response.text}")
        except Exception as e:
            logger.error(f"Failed to add Render custom domain: {e}")
            return {"error": str(e)}

    def _set_environment_variables(self, service_id: str, env_vars: Dict[str, str]):
        """Set environment variables for Render service"""
        for key, value in env_vars.items():
            try:
                response = self.session.post(
                    f"{self.base_url}/services/{service_id}/env-vars",
                    json={"key": key, "value": value},
                )
                if response.status_code not in [200, 201]:
                    logger.warning(f"Failed to set env var {key}: {response.text}")
            except Exception as e:
                logger.error(f"Failed to set environment variable {key}: {e}")

    def _map_render_status(self, render_status: str) -> DeploymentStatus:
        """Map Render status to our enum"""
        status_map = {
            "pending": DeploymentStatus.PENDING,
            "building": DeploymentStatus.BUILDING,
            "deploying": DeploymentStatus.DEPLOYING,
            "live": DeploymentStatus.SUCCESS,
            "failed": DeploymentStatus.FAILED,
            "canceled": DeploymentStatus.CANCELLED,
        }
        return status_map.get(render_status, DeploymentStatus.FAILED)


class VercelProvider(HostingProvider):
    """Vercel hosting provider implementation"""

    def __init__(self, api_key: str, config: Optional[Dict[str, Any]] = None):
        super().__init__(api_key, config)
        self.base_url = "https://api.vercel.com/v1"
        self.team_id = config.get("team_id") if config else None

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def deploy(self, config: DeploymentConfig, repo_url: str) -> DeploymentResult:
        """Deploy to Vercel"""
        try:
            # First, create a project
            project_data = {
                "name": config.name,
                "gitRepository": {
                    "type": "github",
                    "repo": repo_url.replace("https://github.com/", ""),
                },
                "framework": config.framework or "other",
            }

            if self.team_id:
                project_data["teamId"] = self.team_id

            response = self.session.post(f"{self.base_url}/projects", json=project_data)

            if response.status_code == 200:
                project = response.json()

                # Trigger deployment
                deploy_data = {"name": config.name, "target": "production"}

                deploy_response = self.session.post(
                    f"{self.base_url}/projects/{project['id']}/deployments",
                    json=deploy_data,
                )

                if deploy_response.status_code == 200:
                    deployment = deploy_response.json()

                    return DeploymentResult(
                        provider="vercel",
                        service_id=project["id"],
                        deployment_id=deployment["id"],
                        url=deployment["url"],
                        status=DeploymentStatus.SUCCESS,
                    )
                else:
                    raise Exception(
                        f"Failed to trigger Vercel deployment: {deploy_response.text}"
                    )
            else:
                raise Exception(f"Failed to create Vercel project: {response.text}")

        except Exception as e:
            logger.error(f"Vercel deployment failed: {e}")
            return DeploymentResult(
                provider="vercel",
                service_id="",
                deployment_id="",
                url="",
                status=DeploymentStatus.FAILED,
                error=str(e),
            )

    def get_deployment_status(
        self, service_id: str, deployment_id: str
    ) -> DeploymentStatus:
        """Get Vercel deployment status"""
        try:
            response = self.session.get(f"{self.base_url}/deployments/{deployment_id}")
            if response.status_code == 200:
                status = response.json().get("readyState", "unknown")
                return self._map_vercel_status(status)
            return DeploymentStatus.FAILED
        except Exception as e:
            logger.error(f"Failed to get Vercel deployment status: {e}")
            return DeploymentStatus.FAILED

    def list_deployments(self, service_id: str) -> List[Dict[str, Any]]:
        """List Vercel deployments"""
        try:
            response = self.session.get(
                f"{self.base_url}/projects/{service_id}/deployments"
            )
            if response.status_code == 200:
                return response.json().get("deployments", [])
            return []
        except Exception as e:
            logger.error(f"Failed to list Vercel deployments: {e}")
            return []

    def add_custom_domain(self, service_id: str, domain: str) -> Dict[str, Any]:
        """Add custom domain to Vercel project"""
        try:
            domain_data = {"name": domain}
            if self.team_id:
                domain_data["teamId"] = self.team_id

            response = self.session.post(
                f"{self.base_url}/projects/{service_id}/domains", json=domain_data
            )
            if response.status_code == 200:
                return response.json()
            raise Exception(f"Failed to add domain: {response.text}")
        except Exception as e:
            logger.error(f"Failed to add Vercel custom domain: {e}")
            return {"error": str(e)}

    def _map_vercel_status(self, vercel_status: str) -> DeploymentStatus:
        """Map Vercel status to our enum"""
        status_map = {
            "INITIALIZING": DeploymentStatus.PENDING,
            "BUILDING": DeploymentStatus.BUILDING,
            "DEPLOYING": DeploymentStatus.DEPLOYING,
            "READY": DeploymentStatus.SUCCESS,
            "ERROR": DeploymentStatus.FAILED,
            "CANCELED": DeploymentStatus.CANCELLED,
        }
        return status_map.get(vercel_status, DeploymentStatus.FAILED)


class NetlifyProvider(HostingProvider):
    """Netlify hosting provider implementation"""

    def __init__(self, api_key: str, config: Optional[Dict[str, Any]] = None):
        super().__init__(api_key, config)
        self.base_url = "https://api.netlify.com/api/v1"

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def deploy(self, config: DeploymentConfig, repo_url: str) -> DeploymentResult:
        """Deploy to Netlify"""
        try:
            # Create a new site
            site_data = {
                "name": config.name,
                "repo": {
                    "provider": "github",
                    "repo": repo_url.replace("https://github.com/", ""),
                    "branch": config.branch,
                },
            }

            response = self.session.post(f"{self.base_url}/sites", json=site_data)

            if response.status_code == 201:
                site = response.json()

                # Trigger a deploy
                deploy_response = self.session.post(
                    f"{self.base_url}/sites/{site['id']}/deploys"
                )

                if deploy_response.status_code == 201:
                    deployment = deploy_response.json()

                    return DeploymentResult(
                        provider="netlify",
                        service_id=site["id"],
                        deployment_id=deployment["id"],
                        url=site["url"],
                        status=DeploymentStatus.SUCCESS,
                    )
                else:
                    raise Exception(
                        f"Failed to trigger Netlify deployment: {deploy_response.text}"
                    )
            else:
                raise Exception(f"Failed to create Netlify site: {response.text}")

        except Exception as e:
            logger.error(f"Netlify deployment failed: {e}")
            return DeploymentResult(
                provider="netlify",
                service_id="",
                deployment_id="",
                url="",
                status=DeploymentStatus.FAILED,
                error=str(e),
            )

    def get_deployment_status(
        self, service_id: str, deployment_id: str
    ) -> DeploymentStatus:
        """Get Netlify deployment status"""
        try:
            response = self.session.get(
                f"{self.base_url}/sites/{service_id}/deploys/{deployment_id}"
            )
            if response.status_code == 200:
                status = response.json().get("state", "unknown")
                return self._map_netlify_status(status)
            return DeploymentStatus.FAILED
        except Exception as e:
            logger.error(f"Failed to get Netlify deployment status: {e}")
            return DeploymentStatus.FAILED

    def list_deployments(self, service_id: str) -> List[Dict[str, Any]]:
        """List Netlify deployments"""
        try:
            response = self.session.get(f"{self.base_url}/sites/{service_id}/deploys")
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            logger.error(f"Failed to list Netlify deployments: {e}")
            return []

    def add_custom_domain(self, service_id: str, domain: str) -> Dict[str, Any]:
        """Add custom domain to Netlify site"""
        try:
            response = self.session.post(
                f"{self.base_url}/sites/{service_id}/custom_domains",
                json={"domain": domain},
            )
            if response.status_code == 201:
                return response.json()
            raise Exception(f"Failed to add domain: {response.text}")
        except Exception as e:
            logger.error(f"Failed to add Netlify custom domain: {e}")
            return {"error": str(e)}

    def _map_netlify_status(self, netlify_status: str) -> DeploymentStatus:
        """Map Netlify status to our enum"""
        status_map = {
            "pending": DeploymentStatus.PENDING,
            "building": DeploymentStatus.BUILDING,
            "deploying": DeploymentStatus.DEPLOYING,
            "ready": DeploymentStatus.SUCCESS,
            "error": DeploymentStatus.FAILED,
            "canceled": DeploymentStatus.CANCELLED,
        }
        return status_map.get(netlify_status, DeploymentStatus.FAILED)


class RailwayProvider(HostingProvider):
    """Railway hosting provider implementation"""

    def __init__(self, api_key: str, config: Optional[Dict[str, Any]] = None):
        super().__init__(api_key, config)
        self.base_url = "https://backboard.railway.app/graphql/v2"

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def deploy(self, config: DeploymentConfig, repo_url: str) -> DeploymentResult:
        """Deploy to Railway"""
        try:
            # Railway uses GraphQL API
            query = """
            mutation CreateProject($name: String!, $repoUrl: String!) {
                projectCreate(input: { name: $name, repoUrl: $repoUrl }) {
                    project {
                        id
                        name
                        deployments {
                            id
                            status
                            url
                        }
                    }
                }
            }
            """

            variables = {"name": config.name, "repoUrl": repo_url}

            response = self.session.post(
                self.base_url, json={"query": query, "variables": variables}
            )

            if response.status_code == 200:
                data = response.json()
                if "errors" in data:
                    raise Exception(f"Railway GraphQL error: {data['errors']}")

                project = data["data"]["projectCreate"]["project"]
                deployment = (
                    project["deployments"][0] if project["deployments"] else None
                )

                return DeploymentResult(
                    provider="railway",
                    service_id=project["id"],
                    deployment_id=deployment["id"] if deployment else "",
                    url=deployment["url"] if deployment else "",
                    status=DeploymentStatus.SUCCESS,
                )
            else:
                raise Exception(f"Failed to create Railway project: {response.text}")

        except Exception as e:
            logger.error(f"Railway deployment failed: {e}")
            return DeploymentResult(
                provider="railway",
                service_id="",
                deployment_id="",
                url="",
                status=DeploymentStatus.FAILED,
                error=str(e),
            )

    def get_deployment_status(
        self, service_id: str, deployment_id: str
    ) -> DeploymentStatus:
        """Get Railway deployment status"""
        try:
            query = """
            query GetDeployment($id: String!) {
                deployment(id: $id) {
                    status
                }
            }
            """

            response = self.session.post(
                self.base_url, json={"query": query, "variables": {"id": deployment_id}}
            )

            if response.status_code == 200:
                data = response.json()
                if "data" in data and data["data"]["deployment"]:
                    status = data["data"]["deployment"]["status"]
                    return self._map_railway_status(status)
            return DeploymentStatus.FAILED
        except Exception as e:
            logger.error(f"Failed to get Railway deployment status: {e}")
            return DeploymentStatus.FAILED

    def list_deployments(self, service_id: str) -> List[Dict[str, Any]]:
        """List Railway deployments"""
        try:
            query = """
            query GetProject($id: String!) {
                project(id: $id) {
                    deployments {
                        id
                        status
                        url
                        createdAt
                    }
                }
            }
            """

            response = self.session.post(
                self.base_url, json={"query": query, "variables": {"id": service_id}}
            )

            if response.status_code == 200:
                data = response.json()
                if "data" in data and data["data"]["project"]:
                    return data["data"]["project"]["deployments"]
            return []
        except Exception as e:
            logger.error(f"Failed to list Railway deployments: {e}")
            return []

    def add_custom_domain(self, service_id: str, domain: str) -> Dict[str, Any]:
        """Add custom domain to Railway project"""
        try:
            query = """
            mutation AddDomain($projectId: String!, $domain: String!) {
                domainCreate(input: { projectId: $projectId, domain: $domain }) {
                    domain {
                        id
                        domain
                    }
                }
            }
            """

            response = self.session.post(
                self.base_url,
                json={
                    "query": query,
                    "variables": {"projectId": service_id, "domain": domain},
                },
            )

            if response.status_code == 200:
                data = response.json()
                if "data" in data:
                    return data["data"]["domainCreate"]["domain"]
                raise Exception(
                    f"Failed to add domain: {data.get('errors', 'Unknown error')}"
                )
            raise Exception(f"Failed to add domain: {response.text}")
        except Exception as e:
            logger.error(f"Failed to add Railway custom domain: {e}")
            return {"error": str(e)}

    def _map_railway_status(self, railway_status: str) -> DeploymentStatus:
        """Map Railway status to our enum"""
        status_map = {
            "PENDING": DeploymentStatus.PENDING,
            "BUILDING": DeploymentStatus.BUILDING,
            "DEPLOYING": DeploymentStatus.DEPLOYING,
            "SUCCESS": DeploymentStatus.SUCCESS,
            "FAILED": DeploymentStatus.FAILED,
            "CANCELLED": DeploymentStatus.CANCELLED,
        }
        return status_map.get(railway_status, DeploymentStatus.FAILED)


class UniversalDeployer:
    """Universal deployment system supporting multiple hosting providers"""

    def __init__(self):
        self.providers: Dict[str, HostingProvider] = {}
        self.supported_providers = {
            "render": RenderProvider,
            "vercel": VercelProvider,
            "netlify": NetlifyProvider,
            "railway": RailwayProvider,
        }

    def add_provider(
        self, provider_name: str, api_key: str, config: Optional[Dict[str, Any]] = None
    ):
        """Add a hosting provider"""
        if provider_name not in self.supported_providers:
            raise ValueError(f"Unsupported provider: {provider_name}")

        provider_class = self.supported_providers[provider_name]
        self.providers[provider_name] = provider_class(api_key, config)
        logger.info(f"Added provider: {provider_name}")

    def deploy_to_provider(
        self, provider_name: str, config: DeploymentConfig, repo_url: str
    ) -> DeploymentResult:
        """Deploy to a specific provider"""
        if provider_name not in self.providers:
            raise ValueError(f"Provider {provider_name} not configured")

        provider = self.providers[provider_name]
        return provider.deploy(config, repo_url)

    def deploy_to_all(
        self, config: DeploymentConfig, repo_url: str
    ) -> Dict[str, DeploymentResult]:
        """Deploy to all configured providers"""
        results = {}

        for provider_name, provider in self.providers.items():
            try:
                logger.info(f"Deploying to {provider_name}...")
                result = provider.deploy(config, repo_url)
                results[provider_name] = result
                logger.info(f"Deployment to {provider_name}: {result.status.value}")
            except Exception as e:
                logger.error(f"Failed to deploy to {provider_name}: {e}")
                results[provider_name] = DeploymentResult(
                    provider=provider_name,
                    service_id="",
                    deployment_id="",
                    url="",
                    status=DeploymentStatus.FAILED,
                    error=str(e),
                )

        return results

    def get_deployment_status(
        self, provider_name: str, service_id: str, deployment_id: str
    ) -> DeploymentStatus:
        """Get deployment status from a specific provider"""
        if provider_name not in self.providers:
            raise ValueError(f"Provider {provider_name} not configured")

        provider = self.providers[provider_name]
        return provider.get_deployment_status(service_id, deployment_id)

    def list_deployments(
        self, provider_name: str, service_id: str
    ) -> List[Dict[str, Any]]:
        """List deployments from a specific provider"""
        if provider_name not in self.providers:
            raise ValueError(f"Provider {provider_name} not configured")

        provider = self.providers[provider_name]
        return provider.list_deployments(service_id)

    def add_custom_domain(
        self, provider_name: str, service_id: str, domain: str
    ) -> Dict[str, Any]:
        """Add custom domain to a specific provider"""
        if provider_name not in self.providers:
            raise ValueError(f"Provider {provider_name} not configured")

        provider = self.providers[provider_name]
        return provider.add_custom_domain(service_id, domain)

    def get_supported_providers(self) -> List[str]:
        """Get list of supported providers"""
        return list(self.supported_providers.keys())

    def get_configured_providers(self) -> List[str]:
        """Get list of configured providers"""
        return list(self.providers.keys())

    def remove_provider(self, provider_name: str):
        """Remove a provider configuration"""
        if provider_name in self.providers:
            del self.providers[provider_name]
            logger.info(f"Removed provider: {provider_name}")

    def test_provider_connection(self, provider_name: str) -> bool:
        """Test connection to a provider"""
        if provider_name not in self.providers:
            return False

        try:
            provider = self.providers[provider_name]
            # Try to list deployments or get account info
            if hasattr(provider, "test_connection"):
                return provider.test_connection()
            return True
        except Exception as e:
            logger.error(f"Provider connection test failed for {provider_name}: {e}")
            return False


# Factory function for easy provider creation
def create_provider(
    provider_name: str, api_key: str, config: Optional[Dict[str, Any]] = None
) -> HostingProvider:
    """Create a hosting provider instance"""
    if provider_name not in UniversalDeployer().supported_providers:
        raise ValueError(f"Unsupported provider: {provider_name}")

    provider_class = UniversalDeployer().supported_providers[provider_name]
    return provider_class(api_key, config)


# Example usage
if __name__ == "__main__":
    # Initialize universal deployer
    deployer = UniversalDeployer()

    # Add providers
    deployer.add_provider("render", "your_render_api_key")
    deployer.add_provider("vercel", "your_vercel_api_key", {"team_id": "your_team_id"})
    deployer.add_provider("netlify", "your_netlify_api_key")

    # Create deployment config
    config = DeploymentConfig(
        name="my-app",
        service_type=ServiceType.WEB,
        environment="node",
        build_command="npm install && npm run build",
        start_command="npm start",
        env_vars={"NODE_ENV": "production"},
    )

    # Deploy to all providers
    results = deployer.deploy_to_all(config, "https://github.com/user/repo")

    for provider, result in results.items():
        print(f"{provider}: {result.status.value} - {result.url}")
