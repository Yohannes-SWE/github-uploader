import unittest
import json
import requests
import time
import sys
import os
from datetime import datetime
from typing import Dict, List, Any
import logging

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserFlowTestBase(unittest.TestCase):
    """Base class for user flow tests"""
    
    def setUp(self):
        self.base_url = "http://localhost:5000"
        self.session = requests.Session()
        self.test_user = {
            "email": f"testuser_{int(time.time())}@example.com",
            "password": "TestPassword123!"
        }
        self.test_repo = "https://github.com/testuser/test-app"
        self.test_project = f"test-project-{int(time.time())}"
        
    def tearDown(self):
        """Clean up after tests"""
        # Logout if logged in
        try:
            self.session.post(f"{self.base_url}/auth/logout")
        except:
            pass
    
    def assert_success_response(self, response, message="Request should succeed"):
        """Assert that response indicates success"""
        self.assertEqual(response.status_code, 200, f"{message}: {response.status_code}")
        data = response.json()
        self.assertTrue(data.get('success', False), f"{message}: {data.get('error', 'Unknown error')}")
    
    def assert_error_response(self, response, expected_status=400, message="Request should fail"):
        """Assert that response indicates an error"""
        self.assertEqual(response.status_code, expected_status, f"{message}: {response.status_code}")
        data = response.json()
        self.assertFalse(data.get('success', True), f"{message}: Should not succeed")


class AuthenticationFlowTests(UserFlowTestBase):
    """Test user authentication flows"""
    
    def test_01_user_registration_flow(self):
        """Test complete user registration flow"""
        logger.info("Testing user registration flow")
        
        # Step 1: Register new user
        register_data = {
            "email": self.test_user["email"],
            "password": self.test_user["password"],
            "confirm_password": self.test_user["password"]
        }
        
        response = self.session.post(f"{self.base_url}/auth/register", json=register_data)
        self.assert_success_response(response, "User registration should succeed")
        
        # Step 2: Verify user is logged in after registration
        response = self.session.get(f"{self.base_url}/auth/me")
        self.assert_success_response(response, "User should be logged in after registration")
        
        user_data = response.json()
        self.assertEqual(user_data['user']['email'], self.test_user["email"])
    
    def test_02_user_login_flow(self):
        """Test user login flow"""
        logger.info("Testing user login flow")
        
        # Step 1: Register user first
        register_data = {
            "email": self.test_user["email"],
            "password": self.test_user["password"],
            "confirm_password": self.test_user["password"]
        }
        self.session.post(f"{self.base_url}/auth/register", json=register_data)
        
        # Step 2: Logout
        self.session.post(f"{self.base_url}/auth/logout")
        
        # Step 3: Login with correct credentials
        login_data = {
            "email": self.test_user["email"],
            "password": self.test_user["password"]
        }
        
        response = self.session.post(f"{self.base_url}/auth/login", json=login_data)
        self.assert_success_response(response, "User login should succeed")
        
        # Step 4: Verify user is logged in
        response = self.session.get(f"{self.base_url}/auth/me")
        self.assert_success_response(response, "User should be logged in")
    
    def test_03_invalid_login_flow(self):
        """Test invalid login scenarios"""
        logger.info("Testing invalid login scenarios")
        
        # Test 1: Login with non-existent user
        login_data = {
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
        
        response = self.session.post(f"{self.base_url}/auth/login", json=login_data)
        self.assert_error_response(response, 401, "Login with non-existent user should fail")
        
        # Test 2: Login with wrong password
        # First register a user
        register_data = {
            "email": self.test_user["email"],
            "password": self.test_user["password"],
            "confirm_password": self.test_user["password"]
        }
        self.session.post(f"{self.base_url}/auth/register", json=register_data)
        self.session.post(f"{self.base_url}/auth/logout")
        
        # Then try to login with wrong password
        login_data = {
            "email": self.test_user["email"],
            "password": "wrongpassword"
        }
        
        response = self.session.post(f"{self.base_url}/auth/login", json=login_data)
        self.assert_error_response(response, 401, "Login with wrong password should fail")
    
    def test_04_logout_flow(self):
        """Test user logout flow"""
        logger.info("Testing user logout flow")
        
        # Step 1: Register and login
        register_data = {
            "email": self.test_user["email"],
            "password": self.test_user["password"],
            "confirm_password": self.test_user["password"]
        }
        self.session.post(f"{self.base_url}/auth/register", json=register_data)
        
        # Step 2: Verify user is logged in
        response = self.session.get(f"{self.base_url}/auth/me")
        self.assert_success_response(response, "User should be logged in")
        
        # Step 3: Logout
        response = self.session.post(f"{self.base_url}/auth/logout")
        self.assert_success_response(response, "Logout should succeed")
        
        # Step 4: Verify user is logged out
        response = self.session.get(f"{self.base_url}/auth/me")
        self.assert_error_response(response, 401, "User should be logged out")


class ProviderConfigurationFlowTests(UserFlowTestBase):
    """Test hosting provider configuration flows"""
    
    def setUp(self):
        super().setUp()
        # Register and login user
        register_data = {
            "email": self.test_user["email"],
            "password": self.test_user["password"],
            "confirm_password": self.test_user["password"]
        }
        self.session.post(f"{self.base_url}/auth/register", json=register_data)
    
    def test_01_get_supported_providers(self):
        """Test getting list of supported providers"""
        logger.info("Testing get supported providers")
        
        response = self.session.get(f"{self.base_url}/providers/supported")
        self.assert_success_response(response, "Should get supported providers")
        
        data = response.json()
        self.assertIn('providers', data)
        self.assertIn('provider_info', data)
        
        # Verify expected providers are present
        expected_providers = ['render', 'vercel', 'netlify', 'railway']
        for provider in expected_providers:
            self.assertIn(provider, data['providers'])
            self.assertIn(provider, data['provider_info'])
    
    def test_02_configure_render_provider(self):
        """Test configuring Render provider"""
        logger.info("Testing Render provider configuration")
        
        # Test with valid API key (mock)
        config_data = {
            "api_key": "test_render_api_key_123",
            "config": {}
        }
        
        response = self.session.post(f"{self.base_url}/providers/render/configure", json=config_data)
        # This might fail with invalid API key, but should handle gracefully
        if response.status_code == 200:
            self.assert_success_response(response, "Render configuration should succeed")
        else:
            self.assert_error_response(response, 400, "Render configuration should fail with invalid key")
    
    def test_03_configure_vercel_provider(self):
        """Test configuring Vercel provider"""
        logger.info("Testing Vercel provider configuration")
        
        config_data = {
            "api_key": "test_vercel_api_key_123",
            "config": {
                "team_id": "test_team_id"
            }
        }
        
        response = self.session.post(f"{self.base_url}/providers/vercel/configure", json=config_data)
        if response.status_code == 200:
            self.assert_success_response(response, "Vercel configuration should succeed")
        else:
            self.assert_error_response(response, 400, "Vercel configuration should fail with invalid key")
    
    def test_04_configure_netlify_provider(self):
        """Test configuring Netlify provider"""
        logger.info("Testing Netlify provider configuration")
        
        config_data = {
            "api_key": "test_netlify_api_key_123",
            "config": {}
        }
        
        response = self.session.post(f"{self.base_url}/providers/netlify/configure", json=config_data)
        if response.status_code == 200:
            self.assert_success_response(response, "Netlify configuration should succeed")
        else:
            self.assert_error_response(response, 400, "Netlify configuration should fail with invalid key")
    
    def test_05_configure_railway_provider(self):
        """Test configuring Railway provider"""
        logger.info("Testing Railway provider configuration")
        
        config_data = {
            "api_key": "test_railway_api_key_123",
            "config": {}
        }
        
        response = self.session.post(f"{self.base_url}/providers/railway/configure", json=config_data)
        if response.status_code == 200:
            self.assert_success_response(response, "Railway configuration should succeed")
        else:
            self.assert_error_response(response, 400, "Railway configuration should fail with invalid key")
    
    def test_06_configure_invalid_provider(self):
        """Test configuring non-existent provider"""
        logger.info("Testing invalid provider configuration")
        
        config_data = {
            "api_key": "test_api_key",
            "config": {}
        }
        
        response = self.session.post(f"{self.base_url}/providers/invalid_provider/configure", json=config_data)
        self.assert_error_response(response, 400, "Invalid provider should fail")
    
    def test_07_configure_provider_without_api_key(self):
        """Test configuring provider without API key"""
        logger.info("Testing provider configuration without API key")
        
        config_data = {
            "config": {}
        }
        
        response = self.session.post(f"{self.base_url}/providers/render/configure", json=config_data)
        self.assert_error_response(response, 400, "Configuration without API key should fail")
    
    def test_08_get_configured_providers(self):
        """Test getting configured providers"""
        logger.info("Testing get configured providers")
        
        response = self.session.get(f"{self.base_url}/providers/configured")
        self.assert_success_response(response, "Should get configured providers")
        
        data = response.json()
        self.assertIn('providers', data)
        self.assertIn('configurations', data)
    
    def test_09_test_provider_connection(self):
        """Test provider connection testing"""
        logger.info("Testing provider connection test")
        
        # First configure a provider
        config_data = {
            "api_key": "test_api_key",
            "config": {}
        }
        self.session.post(f"{self.base_url}/providers/render/configure", json=config_data)
        
        # Test connection
        response = self.session.post(f"{self.base_url}/providers/render/test")
        self.assert_success_response(response, "Provider connection test should succeed")
        
        data = response.json()
        self.assertIn('connected', data)
        self.assertIn('provider', data)
    
    def test_10_remove_provider(self):
        """Test removing provider configuration"""
        logger.info("Testing provider removal")
        
        # First configure a provider
        config_data = {
            "api_key": "test_api_key",
            "config": {}
        }
        self.session.post(f"{self.base_url}/providers/render/configure", json=config_data)
        
        # Remove provider
        response = self.session.delete(f"{self.base_url}/providers/render/remove")
        self.assert_success_response(response, "Provider removal should succeed")
        
        # Verify provider is removed
        response = self.session.get(f"{self.base_url}/providers/configured")
        data = response.json()
        self.assertNotIn('render', data['providers'])


class DeploymentFlowTests(UserFlowTestBase):
    """Test deployment flows"""
    
    def setUp(self):
        super().setUp()
        # Register and login user
        register_data = {
            "email": self.test_user["email"],
            "password": self.test_user["password"],
            "confirm_password": self.test_user["password"]
        }
        self.session.post(f"{self.base_url}/auth/register", json=register_data)
        
        # Configure a test provider
        config_data = {
            "api_key": "test_api_key",
            "config": {}
        }
        self.session.post(f"{self.base_url}/providers/render/configure", json=config_data)
    
    def test_01_deploy_to_single_provider(self):
        """Test deploying to a single provider"""
        logger.info("Testing single provider deployment")
        
        deploy_data = {
            "repo_url": self.test_repo,
            "project_name": self.test_project,
            "providers": ["render"],
            "environment": "node",
            "build_command": "npm install && npm run build",
            "start_command": "npm start",
            "env_vars": {
                "NODE_ENV": "production"
            }
        }
        
        response = self.session.post(f"{self.base_url}/deploy", json=deploy_data)
        self.assert_success_response(response, "Deployment should be initiated")
        
        data = response.json()
        self.assertIn('results', data)
        self.assertIn('deployment_id', data)
        self.assertIn('render', data['results'])
    
    def test_02_deploy_to_multiple_providers(self):
        """Test deploying to multiple providers"""
        logger.info("Testing multiple provider deployment")
        
        # Configure additional providers
        providers_config = [
            ("vercel", {"api_key": "test_vercel_key", "config": {}}),
            ("netlify", {"api_key": "test_netlify_key", "config": {}})
        ]
        
        for provider, config in providers_config:
            self.session.post(f"{self.base_url}/providers/{provider}/configure", json=config)
        
        deploy_data = {
            "repo_url": self.test_repo,
            "project_name": f"{self.test_project}-multi",
            "providers": ["render", "vercel", "netlify"],
            "environment": "node",
            "build_command": "npm install && npm run build",
            "start_command": "npm start"
        }
        
        response = self.session.post(f"{self.base_url}/deploy", json=deploy_data)
        self.assert_success_response(response, "Multi-provider deployment should be initiated")
        
        data = response.json()
        self.assertIn('results', data)
        self.assertIn('render', data['results'])
        self.assertIn('vercel', data['results'])
        self.assertIn('netlify', data['results'])
    
    def test_03_deploy_to_all_providers(self):
        """Test deploying to all configured providers"""
        logger.info("Testing deploy to all providers")
        
        deploy_data = {
            "repo_url": self.test_repo,
            "project_name": f"{self.test_project}-all",
            "environment": "node",
            "build_command": "npm install && npm run build",
            "start_command": "npm start"
        }
        
        response = self.session.post(f"{self.base_url}/deploy", json=deploy_data)
        self.assert_success_response(response, "Deploy to all should be initiated")
        
        data = response.json()
        self.assertIn('results', data)
        # Should deploy to at least render (configured in setUp)
        self.assertIn('render', data['results'])
    
    def test_04_deploy_with_custom_domains(self):
        """Test deploying with custom domains"""
        logger.info("Testing deployment with custom domains")
        
        deploy_data = {
            "repo_url": self.test_repo,
            "project_name": f"{self.test_project}-domains",
            "providers": ["render"],
            "environment": "node",
            "custom_domains": ["test.example.com", "app.example.com"]
        }
        
        response = self.session.post(f"{self.base_url}/deploy", json=deploy_data)
        self.assert_success_response(response, "Deployment with custom domains should be initiated")
    
    def test_05_deploy_with_different_environments(self):
        """Test deploying with different environments"""
        logger.info("Testing deployment with different environments")
        
        environments = ["node", "python", "static"]
        
        for env in environments:
            deploy_data = {
                "repo_url": self.test_repo,
                "project_name": f"{self.test_project}-{env}",
                "providers": ["render"],
                "environment": env
            }
            
            response = self.session.post(f"{self.base_url}/deploy", json=deploy_data)
            self.assert_success_response(response, f"Deployment with {env} environment should be initiated")
    
    def test_06_deploy_without_required_fields(self):
        """Test deployment without required fields"""
        logger.info("Testing deployment without required fields")
        
        # Test without repo_url
        deploy_data = {
            "project_name": self.test_project,
            "providers": ["render"]
        }
        
        response = self.session.post(f"{self.base_url}/deploy", json=deploy_data)
        self.assert_error_response(response, 400, "Deployment without repo_url should fail")
        
        # Test without project_name
        deploy_data = {
            "repo_url": self.test_repo,
            "providers": ["render"]
        }
        
        response = self.session.post(f"{self.base_url}/deploy", json=deploy_data)
        self.assert_error_response(response, 400, "Deployment without project_name should fail")
    
    def test_07_deploy_to_unconfigured_provider(self):
        """Test deploying to unconfigured provider"""
        logger.info("Testing deployment to unconfigured provider")
        
        deploy_data = {
            "repo_url": self.test_repo,
            "project_name": self.test_project,
            "providers": ["unconfigured_provider"]
        }
        
        response = self.session.post(f"{self.base_url}/deploy", json=deploy_data)
        self.assert_error_response(response, 400, "Deployment to unconfigured provider should fail")
    
    def test_08_deploy_without_providers_configured(self):
        """Test deployment when no providers are configured"""
        logger.info("Testing deployment without any providers configured")
        
        # Remove all providers
        configured_response = self.session.get(f"{self.base_url}/providers/configured")
        if configured_response.status_code == 200:
            data = configured_response.json()
            for provider in data['providers']:
                self.session.delete(f"{self.base_url}/providers/{provider}/remove")
        
        deploy_data = {
            "repo_url": self.test_repo,
            "project_name": self.test_project
        }
        
        response = self.session.post(f"{self.base_url}/deploy", json=deploy_data)
        self.assert_error_response(response, 400, "Deployment without providers should fail")


class DeploymentStatusFlowTests(UserFlowTestBase):
    """Test deployment status and monitoring flows"""
    
    def setUp(self):
        super().setUp()
        # Register and login user
        register_data = {
            "email": self.test_user["email"],
            "password": self.test_user["password"],
            "confirm_password": self.test_user["password"]
        }
        self.session.post(f"{self.base_url}/auth/register", json=register_data)
        
        # Configure a provider and create a deployment
        config_data = {
            "api_key": "test_api_key",
            "config": {}
        }
        self.session.post(f"{self.base_url}/providers/render/configure", json=config_data)
        
        deploy_data = {
            "repo_url": self.test_repo,
            "project_name": self.test_project,
            "providers": ["render"]
        }
        response = self.session.post(f"{self.base_url}/deploy", json=deploy_data)
        self.deployment_id = response.json()['deployment_id']
    
    def test_01_get_deployment_history(self):
        """Test getting deployment history"""
        logger.info("Testing get deployment history")
        
        response = self.session.get(f"{self.base_url}/deployments")
        self.assert_success_response(response, "Should get deployment history")
        
        data = response.json()
        self.assertIn('deployments', data)
        self.assertIsInstance(data['deployments'], list)
        
        # Should have at least one deployment from setUp
        self.assertGreater(len(data['deployments']), 0)
    
    def test_02_get_specific_deployment_status(self):
        """Test getting status of specific deployment"""
        logger.info("Testing get specific deployment status")
        
        response = self.session.get(f"{self.base_url}/deployments/{self.deployment_id}/status")
        self.assert_success_response(response, "Should get deployment status")
        
        data = response.json()
        self.assertIn('deployment', data)
        self.assertEqual(data['deployment']['id'], self.deployment_id)
        self.assertIn('results', data['deployment'])
    
    def test_03_get_nonexistent_deployment_status(self):
        """Test getting status of non-existent deployment"""
        logger.info("Testing get non-existent deployment status")
        
        response = self.session.get(f"{self.base_url}/deployments/nonexistent-id/status")
        self.assert_error_response(response, 404, "Non-existent deployment should return 404")


class CustomDomainFlowTests(UserFlowTestBase):
    """Test custom domain management flows"""
    
    def setUp(self):
        super().setUp()
        # Register and login user
        register_data = {
            "email": self.test_user["email"],
            "password": self.test_user["password"],
            "confirm_password": self.test_user["password"]
        }
        self.session.post(f"{self.base_url}/auth/register", json=register_data)
        
        # Configure a provider
        config_data = {
            "api_key": "test_api_key",
            "config": {}
        }
        self.session.post(f"{self.base_url}/providers/render/configure", json=config_data)
    
    def test_01_add_custom_domain(self):
        """Test adding custom domain"""
        logger.info("Testing add custom domain")
        
        domain_data = {
            "service_id": "test_service_id",
            "domain": "test.example.com"
        }
        
        response = self.session.post(f"{self.base_url}/providers/render/domains", json=domain_data)
        # This might fail with invalid service_id, but should handle gracefully
        if response.status_code == 200:
            self.assert_success_response(response, "Adding custom domain should succeed")
        else:
            self.assert_error_response(response, 400, "Adding custom domain should fail with invalid service_id")
    
    def test_02_add_custom_domain_without_service_id(self):
        """Test adding custom domain without service_id"""
        logger.info("Testing add custom domain without service_id")
        
        domain_data = {
            "domain": "test.example.com"
        }
        
        response = self.session.post(f"{self.base_url}/providers/render/domains", json=domain_data)
        self.assert_error_response(response, 400, "Adding domain without service_id should fail")
    
    def test_03_add_custom_domain_without_domain(self):
        """Test adding custom domain without domain"""
        logger.info("Testing add custom domain without domain")
        
        domain_data = {
            "service_id": "test_service_id"
        }
        
        response = self.session.post(f"{self.base_url}/providers/render/domains", json=domain_data)
        self.assert_error_response(response, 400, "Adding domain without domain should fail")
    
    def test_04_add_custom_domain_to_unconfigured_provider(self):
        """Test adding custom domain to unconfigured provider"""
        logger.info("Testing add custom domain to unconfigured provider")
        
        domain_data = {
            "service_id": "test_service_id",
            "domain": "test.example.com"
        }
        
        response = self.session.post(f"{self.base_url}/providers/unconfigured/domains", json=domain_data)
        self.assert_error_response(response, 400, "Adding domain to unconfigured provider should fail")


class ErrorHandlingFlowTests(UserFlowTestBase):
    """Test error handling flows"""
    
    def test_01_unauthenticated_access(self):
        """Test accessing protected endpoints without authentication"""
        logger.info("Testing unauthenticated access")
        
        protected_endpoints = [
            ("GET", "/providers/configured"),
            ("POST", "/providers/render/configure"),
            ("POST", "/deploy"),
            ("GET", "/deployments"),
            ("POST", "/providers/render/domains")
        ]
        
        for method, endpoint in protected_endpoints:
            if method == "GET":
                response = self.session.get(f"{self.base_url}{endpoint}")
            elif method == "POST":
                response = self.session.post(f"{self.base_url}{endpoint}", json={})
            elif method == "DELETE":
                response = self.session.delete(f"{self.base_url}{endpoint}")
            
            self.assert_error_response(response, 401, f"Unauthenticated access to {endpoint} should fail")
    
    def test_02_invalid_json_requests(self):
        """Test handling of invalid JSON requests"""
        logger.info("Testing invalid JSON requests")
        
        # Register user first
        register_data = {
            "email": self.test_user["email"],
            "password": self.test_user["password"],
            "confirm_password": self.test_user["password"]
        }
        self.session.post(f"{self.base_url}/auth/register", json=register_data)
        
        # Test with invalid JSON
        headers = {'Content-Type': 'application/json'}
        response = self.session.post(
            f"{self.base_url}/deploy",
            data="invalid json",
            headers=headers
        )
        self.assert_error_response(response, 400, "Invalid JSON should be rejected")
    
    def test_03_missing_required_fields(self):
        """Test handling of missing required fields"""
        logger.info("Testing missing required fields")
        
        # Register user first
        register_data = {
            "email": self.test_user["email"],
            "password": self.test_user["password"],
            "confirm_password": self.test_user["password"]
        }
        self.session.post(f"{self.base_url}/auth/register", json=register_data)
        
        # Test registration without email
        register_data = {
            "password": "testpassword",
            "confirm_password": "testpassword"
        }
        response = self.session.post(f"{self.base_url}/auth/register", json=register_data)
        self.assert_error_response(response, 400, "Registration without email should fail")
        
        # Test registration without password
        register_data = {
            "email": "test@example.com",
            "confirm_password": "testpassword"
        }
        response = self.session.post(f"{self.base_url}/auth/register", json=register_data)
        self.assert_error_response(response, 400, "Registration without password should fail")
    
    def test_04_password_mismatch(self):
        """Test password confirmation mismatch"""
        logger.info("Testing password confirmation mismatch")
        
        register_data = {
            "email": self.test_user["email"],
            "password": "password123",
            "confirm_password": "password456"
        }
        
        response = self.session.post(f"{self.base_url}/auth/register", json=register_data)
        self.assert_error_response(response, 400, "Password mismatch should fail")
    
    def test_05_invalid_email_format(self):
        """Test invalid email format"""
        logger.info("Testing invalid email format")
        
        register_data = {
            "email": "invalid-email",
            "password": "password123",
            "confirm_password": "password123"
        }
        
        response = self.session.post(f"{self.base_url}/auth/register", json=register_data)
        self.assert_error_response(response, 400, "Invalid email format should fail")


class PerformanceFlowTests(UserFlowTestBase):
    """Test performance and load handling"""
    
    def test_01_concurrent_deployments(self):
        """Test handling multiple concurrent deployments"""
        logger.info("Testing concurrent deployments")
        
        # Register and login user
        register_data = {
            "email": self.test_user["email"],
            "password": self.test_user["password"],
            "confirm_password": self.test_user["password"]
        }
        self.session.post(f"{self.base_url}/auth/register", json=register_data)
        
        # Configure provider
        config_data = {
            "api_key": "test_api_key",
            "config": {}
        }
        self.session.post(f"{self.base_url}/providers/render/configure", json=config_data)
        
        # Create multiple concurrent deployments
        import threading
        import time
        
        results = []
        errors = []
        
        def deploy_project(project_num):
            try:
                deploy_data = {
                    "repo_url": self.test_repo,
                    "project_name": f"{self.test_project}-{project_num}",
                    "providers": ["render"]
                }
                
                response = self.session.post(f"{self.base_url}/deploy", json=deploy_data)
                results.append((project_num, response.status_code))
            except Exception as e:
                errors.append((project_num, str(e)))
        
        # Start 5 concurrent deployments
        threads = []
        for i in range(5):
            thread = threading.Thread(target=deploy_project, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify results
        self.assertEqual(len(results), 5, "All deployments should complete")
        for project_num, status_code in results:
            self.assertIn(status_code, [200, 400], f"Deployment {project_num} should return valid status")
        
        self.assertEqual(len(errors), 0, "No deployment errors should occur")
    
    def test_02_large_payload_handling(self):
        """Test handling of large payloads"""
        logger.info("Testing large payload handling")
        
        # Register user
        register_data = {
            "email": self.test_user["email"],
            "password": self.test_user["password"],
            "confirm_password": self.test_user["password"]
        }
        self.session.post(f"{self.base_url}/auth/register", json=register_data)
        
        # Create large environment variables payload
        large_env_vars = {}
        for i in range(100):
            large_env_vars[f"VAR_{i}"] = f"value_{i}" * 100  # Large values
        
        deploy_data = {
            "repo_url": self.test_repo,
            "project_name": self.test_project,
            "providers": ["render"],
            "env_vars": large_env_vars
        }
        
        response = self.session.post(f"{self.base_url}/deploy", json=deploy_data)
        # Should handle large payload gracefully
        self.assertIn(response.status_code, [200, 400], "Large payload should be handled")


class SecurityFlowTests(UserFlowTestBase):
    """Test security-related flows"""
    
    def test_01_session_management(self):
        """Test session management and security"""
        logger.info("Testing session management")
        
        # Register user
        register_data = {
            "email": self.test_user["email"],
            "password": self.test_user["password"],
            "confirm_password": self.test_user["password"]
        }
        self.session.post(f"{self.base_url}/auth/register", json=register_data)
        
        # Verify session is maintained
        response = self.session.get(f"{self.base_url}/auth/me")
        self.assert_success_response(response, "Session should be maintained")
        
        # Test session timeout (if implemented)
        # This would require waiting for session timeout, which might not be practical in tests
    
    def test_02_csrf_protection(self):
        """Test CSRF protection (if implemented)"""
        logger.info("Testing CSRF protection")
        
        # This test would depend on CSRF implementation
        # For now, just verify that requests work normally
        register_data = {
            "email": self.test_user["email"],
            "password": self.test_user["password"],
            "confirm_password": self.test_user["password"]
        }
        
        response = self.session.post(f"{self.base_url}/auth/register", json=register_data)
        self.assert_success_response(response, "Registration should work with session")
    
    def test_03_input_validation(self):
        """Test input validation and sanitization"""
        logger.info("Testing input validation")
        
        # Test SQL injection attempts
        malicious_inputs = [
            "'; DROP TABLE users; --",
            "<script>alert('xss')</script>",
            "../../../etc/passwd",
            "'; INSERT INTO users VALUES ('hacker', 'password'); --"
        ]
        
        for malicious_input in malicious_inputs:
            register_data = {
                "email": malicious_input,
                "password": "password123",
                "confirm_password": "password123"
            }
            
            response = self.session.post(f"{self.base_url}/auth/register", json=register_data)
            # Should handle malicious input gracefully
            self.assertIn(response.status_code, [200, 400], "Malicious input should be handled")


class IntegrationFlowTests(UserFlowTestBase):
    """Test complete integration flows"""
    
    def test_01_complete_user_journey(self):
        """Test complete user journey from registration to deployment"""
        logger.info("Testing complete user journey")
        
        # Step 1: Register user
        register_data = {
            "email": self.test_user["email"],
            "password": self.test_user["password"],
            "confirm_password": self.test_user["password"]
        }
        response = self.session.post(f"{self.base_url}/auth/register", json=register_data)
        self.assert_success_response(response, "User registration should succeed")
        
        # Step 2: Get supported providers
        response = self.session.get(f"{self.base_url}/providers/supported")
        self.assert_success_response(response, "Should get supported providers")
        
        # Step 3: Configure a provider
        config_data = {
            "api_key": "test_api_key",
            "config": {}
        }
        response = self.session.post(f"{self.base_url}/providers/render/configure", json=config_data)
        if response.status_code == 200:
            self.assert_success_response(response, "Provider configuration should succeed")
        
        # Step 4: Deploy application
        deploy_data = {
            "repo_url": self.test_repo,
            "project_name": self.test_project,
            "providers": ["render"]
        }
        response = self.session.post(f"{self.base_url}/deploy", json=deploy_data)
        self.assert_success_response(response, "Deployment should be initiated")
        
        deployment_id = response.json()['deployment_id']
        
        # Step 5: Check deployment status
        response = self.session.get(f"{self.base_url}/deployments/{deployment_id}/status")
        self.assert_success_response(response, "Should get deployment status")
        
        # Step 6: Get deployment history
        response = self.session.get(f"{self.base_url}/deployments")
        self.assert_success_response(response, "Should get deployment history")
        
        # Step 7: Logout
        response = self.session.post(f"{self.base_url}/auth/logout")
        self.assert_success_response(response, "Logout should succeed")
        
        # Step 8: Verify logged out
        response = self.session.get(f"{self.base_url}/auth/me")
        self.assert_error_response(response, 401, "Should be logged out")
    
    def test_02_multi_provider_journey(self):
        """Test complete journey with multiple providers"""
        logger.info("Testing multi-provider journey")
        
        # Register user
        register_data = {
            "email": self.test_user["email"],
            "password": self.test_user["password"],
            "confirm_password": self.test_user["password"]
        }
        self.session.post(f"{self.base_url}/auth/register", json=register_data)
        
        # Configure multiple providers
        providers = ["render", "vercel", "netlify"]
        for provider in providers:
            config_data = {
                "api_key": f"test_{provider}_key",
                "config": {}
            }
            self.session.post(f"{self.base_url}/providers/{provider}/configure", json=config_data)
        
        # Deploy to all providers
        deploy_data = {
            "repo_url": self.test_repo,
            "project_name": f"{self.test_project}-multi",
            "providers": providers
        }
        response = self.session.post(f"{self.base_url}/deploy", json=deploy_data)
        self.assert_success_response(response, "Multi-provider deployment should succeed")
        
        # Verify all providers in results
        data = response.json()
        for provider in providers:
            self.assertIn(provider, data['results'])


def run_user_flow_tests():
    """Run all user flow tests"""
    logger.info("Starting user flow tests...")
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        AuthenticationFlowTests,
        ProviderConfigurationFlowTests,
        DeploymentFlowTests,
        DeploymentStatusFlowTests,
        CustomDomainFlowTests,
        ErrorHandlingFlowTests,
        PerformanceFlowTests,
        SecurityFlowTests,
        IntegrationFlowTests
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    logger.info(f"Tests run: {result.testsRun}")
    logger.info(f"Failures: {len(result.failures)}")
    logger.info(f"Errors: {len(result.errors)}")
    
    if result.failures:
        logger.error("Test failures:")
        for test, traceback in result.failures:
            logger.error(f"  {test}: {traceback}")
    
    if result.errors:
        logger.error("Test errors:")
        for test, traceback in result.errors:
            logger.error(f"  {test}: {traceback}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_user_flow_tests()
    exit(0 if success else 1) 