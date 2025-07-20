#!/usr/bin/env python3
"""
Custom Domain Deployment Example

This script demonstrates how to deploy an application to Render with custom domains.
"""

import os
import sys
from typing import Dict, List

# Add the server directory to the path so we can import render_deployer
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'server'))

from render_deployer import UniversalRenderDeployer


def deploy_with_custom_domains():
    """Example of deploying an application with custom domains"""
    
    # Your Render API key (get from https://dashboard.render.com/account/api-keys)
    render_api_key = os.getenv("RENDER_API_KEY")
    if not render_api_key:
        print("❌ Please set RENDER_API_KEY environment variable")
        print("Get your API key from: https://dashboard.render.com/account/api-keys")
        return
    
    # Initialize the deployer
    deployer = UniversalRenderDeployer(render_api_key)
    
    # Example GitHub repository
    github_repo = "your-username/your-project"
    project_name = "my-awesome-app"
    
    # Custom environment variables
    custom_env_vars = {
        "NODE_ENV": "production",
        "DATABASE_URL": "postgresql://user:pass@host:5432/db",
        "JWT_SECRET": "your-secret-key"
    }
    
    # Custom domains configuration
    custom_domains = {
        "frontend": [
            "myapp.com",
            "www.myapp.com"
        ],
        "backend": [
            "api.myapp.com"
        ]
    }
    
    print("🚀 Deploying application with custom domains...")
    print(f"Repository: {github_repo}")
    print(f"Project: {project_name}")
    print(f"Frontend domains: {custom_domains['frontend']}")
    print(f"Backend domains: {custom_domains['backend']}")
    
    try:
        # Deploy the application
        result = deployer.deploy_from_github(
            github_repo=github_repo,
            project_name=project_name,
            custom_env_vars=custom_env_vars,
            custom_domains=custom_domains
        )
        
        print("\n✅ Deployment successful!")
        print(f"Project: {result['project_name']}")
        print(f"Type: {result['app_type']}")
        
        # Print service URLs
        for service in result['services']:
            service_type = service['type']
            service_url = service['service']['service']['url']
            print(f"{service_type.capitalize()}: {service_url}")
        
        # Print deployment URLs
        print("\n🌐 Deployment URLs:")
        for service_type, url in result['deployment_urls'].items():
            print(f"{service_type.capitalize()}: {url}")
            
    except Exception as e:
        print(f"❌ Deployment failed: {e}")


def manage_existing_service_domains():
    """Example of managing domains for an existing service"""
    
    render_api_key = os.getenv("RENDER_API_KEY")
    if not render_api_key:
        print("❌ Please set RENDER_API_KEY environment variable")
        return
    
    deployer = UniversalRenderDeployer(render_api_key)
    
    # Example service ID (you would get this from a previous deployment)
    service_id = "your-service-id"
    
    print(f"🔍 Managing domains for service: {service_id}")
    
    try:
        # List existing domains
        domains = deployer.list_service_domains(service_id)
        print(f"\n📋 Current domains: {len(domains)}")
        for domain in domains:
            print(f"  - {domain['name']} (ID: {domain['id']})")
        
        # Add a new domain
        new_domain = "new-subdomain.myapp.com"
        print(f"\n➕ Adding domain: {new_domain}")
        
        domain_result = deployer.add_domain_to_service(service_id, new_domain)
        print(f"✅ Domain added: {domain_result['name']}")
        
        # Verify the domain
        print(f"\n🔍 Verifying domain: {new_domain}")
        verify_result = deployer.verify_service_domain(service_id, domain_result['id'])
        print(f"✅ Verification status: {verify_result.get('status', 'unknown')}")
        
    except Exception as e:
        print(f"❌ Domain management failed: {e}")


def deploy_with_dns_instructions():
    """Example that provides DNS setup instructions"""
    
    print("🌐 Custom Domain Deployment with DNS Instructions")
    print("=" * 50)
    
    # Example domains
    frontend_domain = "myapp.com"
    backend_domain = "api.myapp.com"
    
    print(f"\n📋 DNS Configuration Required:")
    print(f"Frontend: {frontend_domain}")
    print(f"Backend: {backend_domain}")
    
    print(f"\n🔧 DNS Records to Add:")
    print(f"Type: CNAME")
    print(f"Name: @")
    print(f"Value: your-frontend-service.onrender.com")
    print(f"TTL: 3600")
    print()
    print(f"Type: CNAME")
    print(f"Name: api")
    print(f"Value: your-backend-service.onrender.com")
    print(f"TTL: 3600")
    
    print(f"\n📝 Steps:")
    print(f"1. Add the DNS records above to your domain provider")
    print(f"2. Wait for DNS propagation (usually 5-30 minutes)")
    print(f"3. Deploy your application with custom domains")
    print(f"4. Verify domains in Render dashboard")
    
    # Example deployment with domains
    custom_domains = {
        "frontend": [frontend_domain, f"www.{frontend_domain}"],
        "backend": [backend_domain]
    }
    
    print(f"\n🚀 Example deployment configuration:")
    print(f"custom_domains = {custom_domains}")


if __name__ == "__main__":
    print("Custom Domain Deployment Examples")
    print("=" * 40)
    
    # Check if RENDER_API_KEY is set
    if not os.getenv("RENDER_API_KEY"):
        print("⚠️  RENDER_API_KEY not set. Running examples without deployment.")
        print()
        deploy_with_dns_instructions()
    else:
        print("1. Deploy with custom domains")
        print("2. Manage existing service domains")
        print("3. Show DNS instructions")
        
        choice = input("\nSelect an option (1-3): ").strip()
        
        if choice == "1":
            deploy_with_custom_domains()
        elif choice == "2":
            manage_existing_service_domains()
        elif choice == "3":
            deploy_with_dns_instructions()
        else:
            print("Invalid choice. Running DNS instructions example.")
            deploy_with_dns_instructions() 