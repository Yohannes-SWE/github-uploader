#!/usr/bin/env python3
"""
Automated Deployment with Domain Provider Integration

This script demonstrates how to deploy an application to Render and automatically
configure DNS records with popular domain providers like GoDaddy, Namecheap, Cloudflare, etc.
"""

import os
import sys
import time
from typing import Dict, List, Optional, Any

# Add the server directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'server'))

from render_deployer import UniversalRenderDeployer
from domain_providers import create_provider, DomainManager, DNSRecord, DNSRecordType


class AutomatedDeployer:
    """Automated deployment with domain provider integration"""
    
    def __init__(self, render_api_key: str):
        self.render_deployer = UniversalRenderDeployer(render_api_key)
        self.domain_manager = DomainManager()
        self.connected_providers = {}
    
    def connect_domain_provider(self, provider_name: str, api_key: str, api_secret: str = None):
        """Connect to a domain provider"""
        try:
            provider = create_provider(provider_name, api_key, api_secret)
            
            # Test the connection
            domains = provider.list_domains()
            
            # Register with domain manager
            self.domain_manager.register_provider(provider_name, provider)
            self.connected_providers[provider_name] = provider
            
            print(f"✅ Connected to {provider_name.capitalize()}")
            print(f"   Found {len(domains)} domains")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to connect to {provider_name}: {e}")
            return False
    
    def deploy_with_automated_dns(self, github_repo: str, project_name: str, 
                                 domain_config: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy application and automatically configure DNS"""
        
        print(f"🚀 Starting automated deployment for {project_name}")
        print(f"   Repository: {github_repo}")
        
        # Step 1: Deploy to Render
        print("\n📦 Deploying to Render...")
        try:
            deployment_result = self.render_deployer.deploy_from_github(
                github_repo=github_repo,
                project_name=project_name,
                custom_env_vars=domain_config.get("env_vars", {}),
                custom_domains=domain_config.get("custom_domains", {})
            )
            
            print("✅ Render deployment successful!")
            
        except Exception as e:
            print(f"❌ Render deployment failed: {e}")
            return {"status": "error", "message": f"Render deployment failed: {e}"}
        
        # Step 2: Configure DNS with domain providers
        dns_results = {}
        
        if domain_config.get("domain_provider") and domain_config.get("domains"):
            print("\n🌐 Configuring DNS records...")
            
            provider_name = domain_config["domain_provider"]
            domains = domain_config["domains"]
            
            if provider_name not in self.connected_providers:
                print(f"❌ Provider {provider_name} not connected")
                return {"status": "error", "message": f"Provider {provider_name} not connected"}
            
            # Configure DNS for each service
            for service_type, service_data in deployment_result["deployment_urls"].items():
                if service_type in domains:
                    domain = domains[service_type]
                    print(f"   Configuring {service_type} domain: {domain}")
                    
                    try:
                        dns_result = self.domain_manager.setup_render_domains(
                            provider_name, domain, service_data
                        )
                        dns_results[service_type] = dns_result
                        print(f"   ✅ DNS configured for {domain}")
                        
                    except Exception as e:
                        print(f"   ❌ DNS configuration failed for {domain}: {e}")
                        dns_results[service_type] = {"error": str(e)}
        
        # Step 3: Verify DNS propagation
        propagation_results = {}
        
        if dns_results:
            print("\n🔍 Verifying DNS propagation...")
            
            for service_type, dns_result in dns_results.items():
                if "error" not in dns_result:
                    domain = domains[service_type]
                    service_url = deployment_result["deployment_urls"][service_type]
                    
                    print(f"   Checking propagation for {domain}...")
                    
                    # Wait for propagation
                    for attempt in range(10):
                        if self.domain_manager.verify_dns_propagation(domain, service_url, "CNAME"):
                            propagation_results[service_type] = {
                                "status": "success",
                                "attempts": attempt + 1
                            }
                            print(f"   ✅ DNS propagated for {domain} (attempt {attempt + 1})")
                            break
                        
                        if attempt < 9:
                            print(f"   ⏳ Waiting for DNS propagation... (attempt {attempt + 1}/10)")
                            time.sleep(30)
                    else:
                        propagation_results[service_type] = {
                            "status": "pending",
                            "message": "DNS propagation not complete after 10 attempts"
                        }
                        print(f"   ⚠️ DNS propagation pending for {domain}")
        
        return {
            "status": "success",
            "deployment": deployment_result,
            "dns_configuration": dns_results,
            "dns_propagation": propagation_results,
            "summary": {
                "project_name": project_name,
                "render_services": len(deployment_result["services"]),
                "domains_configured": len(dns_results),
                "domains_propagated": len([r for r in propagation_results.values() if r.get("status") == "success"])
            }
        }
    
    def list_available_domains(self, provider_name: str) -> List[Dict[str, Any]]:
        """List available domains for a provider"""
        if provider_name not in self.connected_providers:
            print(f"❌ Provider {provider_name} not connected")
            return []
        
        try:
            domains = self.connected_providers[provider_name].list_domains()
            return domains
        except Exception as e:
            print(f"❌ Failed to list domains: {e}")
            return []
    
    def get_domain_records(self, provider_name: str, domain: str) -> List[DNSRecord]:
        """Get DNS records for a domain"""
        if provider_name not in self.connected_providers:
            print(f"❌ Provider {provider_name} not connected")
            return []
        
        try:
            records = self.connected_providers[provider_name].list_dns_records(domain)
            return records
        except Exception as e:
            print(f"❌ Failed to get DNS records: {e}")
            return []


def main():
    """Main function with interactive deployment"""
    
    print("🚀 Automated Deployment with Domain Provider Integration")
    print("=" * 60)
    
    # Get Render API key
    render_api_key = os.getenv("RENDER_API_KEY")
    if not render_api_key:
        print("❌ Please set RENDER_API_KEY environment variable")
        print("Get your API key from: https://dashboard.render.com/account/api-keys")
        return
    
    # Initialize deployer
    deployer = AutomatedDeployer(render_api_key)
    
    # Connect domain providers
    print("\n🔗 Connecting Domain Providers")
    print("-" * 30)
    
    # Example: Connect to GoDaddy
    godaddy_key = os.getenv("GODADDY_API_KEY")
    godaddy_secret = os.getenv("GODADDY_API_SECRET")
    
    if godaddy_key and godaddy_secret:
        deployer.connect_domain_provider("godaddy", godaddy_key, godaddy_secret)
    
    # Example: Connect to Cloudflare
    cloudflare_key = os.getenv("CLOUDFLARE_API_KEY")
    
    if cloudflare_key:
        deployer.connect_domain_provider("cloudflare", cloudflare_key)
    
    # Example: Connect to Namecheap
    namecheap_key = os.getenv("NAMECHEAP_API_KEY")
    namecheap_secret = os.getenv("NAMECHEAP_API_SECRET")
    
    if namecheap_key and namecheap_secret:
        deployer.connect_domain_provider("namecheap", namecheap_key, namecheap_secret)
    
    # Example deployment configuration
    deployment_config = {
        "github_repo": "your-username/your-project",
        "project_name": "my-awesome-app",
        "domain_config": {
            "domain_provider": "godaddy",  # or "cloudflare", "namecheap"
            "domains": {
                "frontend": "myapp.com",
                "backend": "api.myapp.com"
            },
            "env_vars": {
                "NODE_ENV": "production",
                "DATABASE_URL": "postgresql://user:pass@host:5432/db"
            }
        }
    }
    
    print(f"\n📋 Deployment Configuration:")
    print(f"   Repository: {deployment_config['github_repo']}")
    print(f"   Project: {deployment_config['project_name']}")
    print(f"   Domain Provider: {deployment_config['domain_config']['domain_provider']}")
    print(f"   Frontend Domain: {deployment_config['domain_config']['domains']['frontend']}")
    print(f"   Backend Domain: {deployment_config['domain_config']['domains']['backend']}")
    
    # Ask for confirmation
    confirm = input("\n🤔 Proceed with deployment? (y/N): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Deployment cancelled")
        return
    
    # Execute deployment
    print("\n🚀 Starting deployment...")
    result = deployer.deploy_with_automated_dns(
        deployment_config["github_repo"],
        deployment_config["project_name"],
        deployment_config["domain_config"]
    )
    
    # Display results
    print(f"\n📊 Deployment Results:")
    print(f"   Status: {result['status']}")
    
    if result['status'] == 'success':
        summary = result['summary']
        print(f"   Render Services: {summary['render_services']}")
        print(f"   Domains Configured: {summary['domains_configured']}")
        print(f"   Domains Propagated: {summary['domains_propagated']}")
        
        print(f"\n🌐 Service URLs:")
        for service_type, url in result['deployment']['deployment_urls'].items():
            print(f"   {service_type.capitalize()}: {url}")
        
        print(f"\n🔗 Custom Domains:")
        for service_type, domain in deployment_config['domain_config']['domains'].items():
            print(f"   {service_type.capitalize()}: https://{domain}")
    
    else:
        print(f"   Error: {result.get('message', 'Unknown error')}")


def example_usage():
    """Example usage of the automated deployer"""
    
    print("📚 Example Usage")
    print("=" * 30)
    
    # Example 1: Simple deployment with GoDaddy
    print("\n1. Deploy with GoDaddy DNS:")
    print("""
    # Set environment variables
    export RENDER_API_KEY="your-render-api-key"
    export GODADDY_API_KEY="your-godaddy-api-key"
    export GODADDY_API_SECRET="your-godaddy-api-secret"
    
    # Run deployment
    python3 automated-deployment-with-domains.py
    """)
    
    # Example 2: Cloudflare deployment
    print("\n2. Deploy with Cloudflare DNS:")
    print("""
    # Set environment variables
    export RENDER_API_KEY="your-render-api-key"
    export CLOUDFLARE_API_KEY="your-cloudflare-api-key"
    
    # Run deployment
    python3 automated-deployment-with-domains.py
    """)
    
    # Example 3: Programmatic usage
    print("\n3. Programmatic Usage:")
    print("""
    from automated_deployment_with_domains import AutomatedDeployer
    
    # Initialize deployer
    deployer = AutomatedDeployer("your-render-api-key")
    
    # Connect domain provider
    deployer.connect_domain_provider("godaddy", "api-key", "api-secret")
    
    # Deploy with automated DNS
    result = deployer.deploy_with_automated_dns(
        github_repo="username/project",
        project_name="my-app",
        domain_config={
            "domain_provider": "godaddy",
            "domains": {
                "frontend": "myapp.com",
                "backend": "api.myapp.com"
            }
        }
    )
    """)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--example":
        example_usage()
    else:
        main() 