# 🌐 Domain Provider Automation Guide

This guide covers how to automatically configure DNS records with popular domain providers when deploying applications to Render.

## 🎯 **Overview**

The domain provider automation feature allows you to:

- **Connect to domain providers**: GoDaddy, Namecheap, Cloudflare, Squarespace
- **Automatically configure DNS**: Set up CNAME records for Render services
- **Verify DNS propagation**: Monitor when DNS changes take effect
- **Full-stack support**: Configure both frontend and backend domains
- **One-click deployment**: Deploy and configure DNS in a single operation

## 🚀 **Supported Providers**

### **1. GoDaddy**

- **API Documentation**: [GoDaddy Developer Portal](https://developer.godaddy.com/doc/endpoint/domains)
- **Features**: DNS Management, Domain Registration, SSL Certificates
- **Authentication**: API Key + API Secret

### **2. Namecheap**

- **API Documentation**: [Namecheap API](https://www.namecheap.com/support/api/)
- **Features**: DNS Management, Domain Registration, WHOIS Privacy
- **Authentication**: API Key + API Secret

### **3. Cloudflare**

- **API Documentation**: [Cloudflare API](https://developers.cloudflare.com/api/)
- **Features**: DNS Management, CDN, SSL Certificates, DDoS Protection
- **Authentication**: API Token

### **4. Squarespace**

- **API Documentation**: [Squarespace Developer](https://developers.squarespace.com/)
- **Features**: DNS Management, Website Builder, E-commerce
- **Authentication**: API Key

## 🔧 **Setup Instructions**

### **1. Get API Credentials**

#### **GoDaddy**

1. Go to [GoDaddy Developer Portal](https://developer.godaddy.com/)
2. Create an account and log in
3. Navigate to "Keys" section
4. Generate API Key and API Secret
5. Note down both credentials

#### **Namecheap**

1. Go to [Namecheap API](https://www.namecheap.com/support/api/)
2. Log in to your Namecheap account
3. Navigate to "API Access" section
4. Generate API Key and API Secret
5. Note down both credentials

#### **Cloudflare**

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. Navigate to "My Profile" → "API Tokens"
3. Create new token with "Zone:Zone:Edit" permissions
4. Copy the generated token

#### **Squarespace**

1. Go to [Squarespace Developer](https://developers.squarespace.com/)
2. Create a developer account
3. Generate API key for your account
4. Note down the API key

### **2. Connect Provider via API**

```bash
# Connect GoDaddy
curl -X POST "https://your-backend.com/api/domain-providers/connect" \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "godaddy",
    "api_key": "your-godaddy-api-key",
    "api_secret": "your-godaddy-api-secret"
  }'

# Connect Cloudflare
curl -X POST "https://your-backend.com/api/domain-providers/connect" \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "cloudflare",
    "api_key": "your-cloudflare-api-token"
  }'
```

### **3. Deploy with Automated DNS**

```bash
# Deploy with custom domains and DNS automation
curl -X POST "https://your-backend.com/api/render/deploy" \
  -H "Content-Type: application/json" \
  -d '{
    "github_repo": "username/my-project",
    "project_name": "my-app",
    "custom_domains": {
      "frontend": ["myapp.com", "www.myapp.com"],
      "backend": ["api.myapp.com"]
    },
    "domain_provider": "godaddy"
  }'
```

## 📋 **API Endpoints**

### **Connect Domain Provider**

```bash
POST /api/domain-providers/connect
```

**Parameters:**

- `provider` (string): Provider name (godaddy, namecheap, cloudflare, squarespace)
- `api_key` (string): Provider API key
- `api_secret` (string, optional): Provider API secret

**Response:**

```json
{
  "status": "success",
  "message": "GoDaddy account connected successfully",
  "provider": "godaddy",
  "domains_count": 5,
  "domains": [
    { "name": "myapp.com", "status": "active" },
    { "name": "example.com", "status": "active" }
  ]
}
```

### **List Provider Domains**

```bash
GET /api/domain-providers/{provider}/domains
```

**Response:**

```json
{
  "status": "success",
  "provider": "godaddy",
  "domains": [
    {
      "name": "myapp.com",
      "status": "active",
      "expires": "2025-01-01T00:00:00Z"
    }
  ]
}
```

### **Get Domain DNS Records**

```bash
GET /api/domain-providers/{provider}/domains/{domain}/records
```

**Response:**

```json
{
  "status": "success",
  "provider": "godaddy",
  "domain": "myapp.com",
  "records": [
    {
      "type": "CNAME",
      "name": "@",
      "value": "myapp.onrender.com",
      "ttl": 3600
    }
  ]
}
```

### **Setup Render Domain**

```bash
POST /api/domain-providers/{provider}/domains/{domain}/setup-render
```

**Parameters:**

- `render_service_url` (string): Render service URL

**Response:**

```json
{
  "status": "success",
  "message": "DNS records configured for myapp.com",
  "result": {
    "status": "success",
    "message": "Domain myapp.com added successfully",
    "domain": {
      "id": "domain-id",
      "name": "myapp.com",
      "status": "pending"
    }
  }
}
```

### **Setup Full-Stack Domains**

```bash
POST /api/domain-providers/{provider}/setup-fullstack
```

**Parameters:**

- `frontend_domain` (string): Frontend domain
- `backend_domain` (string): Backend domain
- `frontend_url` (string): Frontend service URL
- `backend_url` (string): Backend service URL

### **Verify DNS Propagation**

```bash
POST /api/domain-providers/{provider}/domains/{domain}/verify-propagation
```

**Parameters:**

- `expected_value` (string): Expected DNS record value
- `record_type` (string, optional): Record type (default: CNAME)

## 🚀 **Automated Deployment Script**

### **Using the Automated Deployer**

```python
from scripts.automated_deployment_with_domains import AutomatedDeployer

# Initialize deployer
deployer = AutomatedDeployer("your-render-api-key")

# Connect domain providers
deployer.connect_domain_provider("godaddy", "api-key", "api-secret")
deployer.connect_domain_provider("cloudflare", "api-token")

# Deploy with automated DNS
result = deployer.deploy_with_automated_dns(
    github_repo="username/my-project",
    project_name="my-app",
    domain_config={
        "domain_provider": "godaddy",
        "domains": {
            "frontend": "myapp.com",
            "backend": "api.myapp.com"
        },
        "env_vars": {
            "NODE_ENV": "production",
            "DATABASE_URL": "postgresql://..."
        }
    }
)

print(f"Deployment Status: {result['status']}")
print(f"Domains Configured: {result['summary']['domains_configured']}")
print(f"Domains Propagated: {result['summary']['domains_propagated']}")
```

### **Environment Variables**

```bash
# Render API
export RENDER_API_KEY="your-render-api-key"

# GoDaddy
export GODADDY_API_KEY="your-godaddy-api-key"
export GODADDY_API_SECRET="your-godaddy-api-secret"

# Cloudflare
export CLOUDFLARE_API_KEY="your-cloudflare-api-token"

# Namecheap
export NAMECHEAP_API_KEY="your-namecheap-api-key"
export NAMECHEAP_API_SECRET="your-namecheap-api-secret"
```

## 📝 **Step-by-Step Workflow**

### **1. Prepare Your Domains**

1. **Purchase domains** from your preferred provider
2. **Get API credentials** from the provider
3. **Ensure domains are active** and ready for DNS configuration

### **2. Connect Domain Provider**

```bash
# Connect via API
curl -X POST "https://your-backend.com/api/domain-providers/connect" \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "godaddy",
    "api_key": "your-api-key",
    "api_secret": "your-api-secret"
  }'
```

### **3. Deploy Application**

```bash
# Deploy with automated DNS
curl -X POST "https://your-backend.com/api/render/deploy" \
  -H "Content-Type: application/json" \
  -d '{
    "github_repo": "username/my-project",
    "project_name": "my-app",
    "custom_domains": {
      "frontend": ["myapp.com"],
      "backend": ["api.myapp.com"]
    }
  }'
```

### **4. Configure DNS Automatically**

```bash
# Setup DNS for frontend
curl -X POST "https://your-backend.com/api/domain-providers/godaddy/domains/myapp.com/setup-render" \
  -H "Content-Type: application/json" \
  -d '{
    "render_service_url": "myapp-frontend.onrender.com"
  }'

# Setup DNS for backend
curl -X POST "https://your-backend.com/api/domain-providers/godaddy/domains/api.myapp.com/setup-render" \
  -H "Content-Type: application/json" \
  -d '{
    "render_service_url": "myapp-backend.onrender.com"
  }'
```

### **5. Verify DNS Propagation**

```bash
# Check DNS propagation
curl -X POST "https://your-backend.com/api/domain-providers/godaddy/domains/myapp.com/verify-propagation" \
  -H "Content-Type: application/json" \
  -d '{
    "expected_value": "myapp-frontend.onrender.com",
    "record_type": "CNAME"
  }'
```

## 🔍 **DNS Configuration Details**

### **Automatic DNS Records**

The system automatically creates the following DNS records:

#### **Frontend Domain (e.g., myapp.com)**

```
Type: CNAME
Name: @ (root domain)
Value: your-frontend-service.onrender.com
TTL: 3600
```

#### **Backend Domain (e.g., api.myapp.com)**

```
Type: CNAME
Name: api (subdomain)
Value: your-backend-service.onrender.com
TTL: 3600
```

#### **WWW Subdomain (e.g., www.myapp.com)**

```
Type: CNAME
Name: www
Value: myapp.com
TTL: 3600
```

### **Provider-Specific Configuration**

#### **GoDaddy**

- Uses GoDaddy DNS API v1
- Supports all DNS record types
- Automatic SSL certificate provisioning

#### **Cloudflare**

- Uses Cloudflare API v4
- Includes CDN and DDoS protection
- Automatic SSL certificate provisioning

#### **Namecheap**

- Uses Namecheap XML API
- Supports WHOIS privacy
- Automatic SSL certificate provisioning

#### **Squarespace**

- Uses Squarespace API v1.0
- Includes website builder integration
- Automatic SSL certificate provisioning

## 🛠️ **Troubleshooting**

### **Common Issues**

#### **1. API Authentication Failed**

**Symptoms:** "Failed to connect provider account"
**Solutions:**

- Verify API credentials are correct
- Check API key permissions
- Ensure account is active

#### **2. Domain Not Found**

**Symptoms:** "Domain not found in provider account"
**Solutions:**

- Verify domain ownership
- Check domain status (active, suspended, etc.)
- Ensure domain is in the correct account

#### **3. DNS Configuration Failed**

**Symptoms:** "Failed to add DNS record"
**Solutions:**

- Check existing DNS records for conflicts
- Verify domain is unlocked for DNS changes
- Ensure API has DNS management permissions

#### **4. DNS Propagation Delayed**

**Symptoms:** "DNS propagation not complete"
**Solutions:**

- Wait 5-30 minutes for propagation
- Check DNS propagation with external tools
- Verify DNS records are correctly configured

### **Debugging Commands**

```bash
# Check DNS propagation
dig myapp.com CNAME

# Check if domain resolves
nslookup myapp.com

# Test HTTPS
curl -I https://myapp.com

# Check DNS records
curl -X GET "https://your-backend.com/api/domain-providers/godaddy/domains/myapp.com/records"
```

## 📚 **Examples**

### **Full-Stack Application with GoDaddy**

```python
# Complete deployment example
from scripts.automated_deployment_with_domains import AutomatedDeployer

deployer = AutomatedDeployer("your-render-api-key")
deployer.connect_domain_provider("godaddy", "api-key", "api-secret")

result = deployer.deploy_with_automated_dns(
    github_repo="username/fullstack-app",
    project_name="my-fullstack-app",
    domain_config={
        "domain_provider": "godaddy",
        "domains": {
            "frontend": "myapp.com",
            "backend": "api.myapp.com"
        },
        "env_vars": {
            "NODE_ENV": "production",
            "DATABASE_URL": "postgresql://user:pass@host:5432/db"
        }
    }
)
```

### **Static Site with Cloudflare**

```python
# Static site deployment
result = deployer.deploy_with_automated_dns(
    github_repo="username/portfolio",
    project_name="my-portfolio",
    domain_config={
        "domain_provider": "cloudflare",
        "domains": {
            "frontend": "portfolio.com"
        }
    }
)
```

### **API-Only Backend with Namecheap**

```python
# API deployment
result = deployer.deploy_with_automated_dns(
    github_repo="username/api-server",
    project_name="my-api",
    domain_config={
        "domain_provider": "namecheap",
        "domains": {
            "backend": "api.myapp.com"
        }
    }
)
```

## 🔐 **Security Considerations**

### **API Key Security**

- Store API keys securely (environment variables, secret management)
- Use least-privilege API permissions
- Rotate API keys regularly
- Monitor API usage for suspicious activity

### **Domain Security**

- Only configure domains you own
- Verify domain ownership before configuration
- Use secure DNS providers
- Enable DNSSEC when available

### **SSL Certificates**

- All providers automatically provision SSL certificates
- Certificates are managed by the providers
- No additional configuration needed

## 📞 **Support**

### **Getting Help**

1. Check provider API documentation
2. Verify API credentials and permissions
3. Test DNS configuration manually
4. Check DNS propagation with external tools

### **Useful Resources**

- [GoDaddy Developer Portal](https://developer.godaddy.com/)
- [Namecheap API Documentation](https://www.namecheap.com/support/api/)
- [Cloudflare API Documentation](https://developers.cloudflare.com/api/)
- [Squarespace Developer](https://developers.squarespace.com/)
- [DNS Propagation Checker](https://www.whatsmydns.net/)

---

**Need help?** Run the example script: `python3 scripts/automated-deployment-with-domains.py --example`
