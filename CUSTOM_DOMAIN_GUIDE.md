# 🌐 Custom Domain Management Guide

This guide covers how to deploy applications to Render with custom domains using the GitHub Uploader's Render deployer.

## 🎯 **Overview**

The custom domain functionality allows you to:

- **Deploy with custom domains**: Set up domains during initial deployment
- **Add domains to existing services**: Manage domains for already deployed services
- **Verify domain ownership**: Trigger DNS verification through the API
- **Remove domains**: Clean up unused custom domains

## 🚀 **Quick Start**

### 1. **Deploy with Custom Domains**

```python
from render_deployer import UniversalRenderDeployer

# Initialize deployer
deployer = UniversalRenderDeployer("your-render-api-key")

# Deploy with custom domains
result = deployer.deploy_from_github(
    github_repo="your-username/your-project",
    project_name="my-app",
    custom_domains={
        "frontend": ["myapp.com", "www.myapp.com"],
        "backend": ["api.myapp.com"]
    }
)
```

### 2. **Add Domain to Existing Service**

```python
from render_deployer import RenderDeployer

deployer = RenderDeployer("your-render-api-key")

# Add custom domain
domain_result = deployer.add_custom_domain("service-id", "new-domain.com")

# Verify the domain
verify_result = deployer.verify_custom_domain("service-id", domain_result["id"])
```

## 📋 **API Endpoints**

### **Deploy with Custom Domains**

```bash
POST /api/render/deploy
```

**Parameters:**

- `github_repo` (string): GitHub repository (e.g., "username/repo")
- `project_name` (string, optional): Project name
- `custom_env_vars` (object, optional): Environment variables
- `custom_domains` (object, optional): Custom domains configuration

**Example:**

```json
{
  "github_repo": "username/my-project",
  "project_name": "my-app",
  "custom_domains": {
    "frontend": ["myapp.com", "www.myapp.com"],
    "backend": ["api.myapp.com"]
  }
}
```

### **List Service Domains**

```bash
GET /api/render/services/{service_id}/domains
```

**Response:**

```json
{
  "status": "success",
  "domains": [
    {
      "id": "domain-id",
      "name": "myapp.com",
      "status": "pending",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### **Add Custom Domain**

```bash
POST /api/render/services/{service_id}/domains
```

**Parameters:**

- `domain` (string): Domain name to add

**Response:**

```json
{
  "status": "success",
  "message": "Domain myapp.com added successfully",
  "domain": {
    "id": "domain-id",
    "name": "myapp.com",
    "status": "pending"
  }
}
```

### **Remove Custom Domain**

```bash
DELETE /api/render/services/{service_id}/domains/{domain_id}
```

**Response:**

```json
{
  "status": "success",
  "message": "Domain removed successfully"
}
```

### **Get Domain Details**

```bash
GET /api/render/services/{service_id}/domains/{domain_id}
```

**Response:**

```json
{
  "status": "success",
  "domain": {
    "id": "domain-id",
    "name": "myapp.com",
    "status": "verified",
    "created_at": "2024-01-01T00:00:00Z",
    "verified_at": "2024-01-01T01:00:00Z"
  }
}
```

### **Verify Domain**

```bash
POST /api/render/services/{service_id}/domains/{domain_id}/verify
```

**Response:**

```json
{
  "status": "success",
  "message": "Domain verification triggered",
  "verification": {
    "status": "pending",
    "message": "DNS verification in progress"
  }
}
```

## 🔧 **DNS Configuration**

### **Required DNS Records**

For each custom domain, you need to add a CNAME record pointing to your Render service:

#### **Frontend Domain (e.g., myapp.com)**

```
Type: CNAME
Name: @ (or leave blank for root domain)
Value: your-frontend-service.onrender.com
TTL: 3600
```

#### **Backend Domain (e.g., api.myapp.com)**

```
Type: CNAME
Name: api
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

### **Domain Provider Examples**

#### **Cloudflare**

1. Go to DNS settings
2. Add CNAME record
3. Set name to `@` for root domain or subdomain name
4. Set target to your Render service URL
5. Set TTL to Auto or 3600

#### **GoDaddy**

1. Go to DNS Management
2. Add CNAME record
3. Set Host to `@` for root domain or subdomain
4. Set Points to your Render service URL
5. Set TTL to 1 hour

#### **Namecheap**

1. Go to Advanced DNS
2. Add CNAME record
3. Set Host to `@` for root domain or subdomain
4. Set Value to your Render service URL
5. Set TTL to Automatic

## 📝 **Step-by-Step Deployment**

### **1. Prepare Your Domain**

1. **Purchase a domain** (if you don't have one)
2. **Add DNS records** as shown above
3. **Wait for DNS propagation** (5-30 minutes)

### **2. Deploy Your Application**

```python
# Example deployment script
from render_deployer import UniversalRenderDeployer

deployer = UniversalRenderDeployer("your-api-key")

# Deploy with custom domains
result = deployer.deploy_from_github(
    github_repo="username/my-project",
    project_name="my-app",
    custom_domains={
        "frontend": ["myapp.com", "www.myapp.com"],
        "backend": ["api.myapp.com"]
    }
)

print("Deployment URLs:")
for service_type, url in result['deployment_urls'].items():
    print(f"{service_type}: {url}")
```

### **3. Verify Domains**

1. **Check DNS propagation**: Use tools like `dig` or online DNS checkers
2. **Verify in Render dashboard**: Go to your service settings
3. **Trigger verification**: Use the API endpoint if needed

```python
# Verify a domain
verify_result = deployer.verify_service_domain("service-id", "domain-id")
print(f"Verification status: {verify_result['status']}")
```

## 🔍 **Domain Status Types**

### **Pending**

- Domain added but DNS not yet configured
- Render waiting for DNS records to propagate

### **Verifying**

- DNS records detected
- Render verifying domain ownership

### **Verified**

- Domain successfully verified
- Ready to serve traffic

### **Failed**

- DNS verification failed
- Check DNS configuration

## 🛠️ **Troubleshooting**

### **Common Issues**

#### **1. DNS Not Propagated**

**Symptoms:** Domain shows "pending" status
**Solution:** Wait 5-30 minutes for DNS propagation

#### **2. Incorrect CNAME Record**

**Symptoms:** Domain verification fails
**Solution:** Double-check CNAME record points to correct Render service

#### **3. Multiple Domains for Same Service**

**Symptoms:** Only one domain works
**Solution:** Ensure each domain has its own CNAME record

#### **4. HTTPS Issues**

**Symptoms:** Mixed content warnings
**Solution:** Render automatically provides SSL certificates

### **Debugging Commands**

```bash
# Check DNS propagation
dig myapp.com CNAME

# Check if domain resolves
nslookup myapp.com

# Test HTTPS
curl -I https://myapp.com
```

## 📚 **Examples**

### **Full-Stack Application**

```python
# Deploy React frontend + Node.js backend
custom_domains = {
    "frontend": ["myapp.com", "www.myapp.com"],
    "backend": ["api.myapp.com"]
}

result = deployer.deploy_from_github(
    github_repo="username/fullstack-app",
    project_name="my-fullstack-app",
    custom_domains=custom_domains
)
```

### **Static Site**

```python
# Deploy static site with custom domain
custom_domains = {
    "frontend": ["portfolio.com", "www.portfolio.com"]
}

result = deployer.deploy_from_github(
    github_repo="username/portfolio",
    project_name="my-portfolio",
    custom_domains=custom_domains
)
```

### **API-Only Backend**

```python
# Deploy API with custom domain
custom_domains = {
    "backend": ["api.myapp.com"]
}

result = deployer.deploy_from_github(
    github_repo="username/api-server",
    project_name="my-api",
    custom_domains=custom_domains
)
```

## 🔐 **Security Considerations**

### **Domain Ownership**

- Only add domains you own
- Verify domain ownership before adding
- Use secure DNS providers

### **SSL Certificates**

- Render automatically provides SSL certificates
- Certificates are managed by Render
- No additional configuration needed

### **Access Control**

- API key provides full access to your Render account
- Keep API keys secure
- Rotate keys regularly

## 📞 **Support**

### **Getting Help**

1. Check DNS configuration
2. Verify domain ownership
3. Check Render service status
4. Review API responses for error details

### **Useful Resources**

- [Render Custom Domains Documentation](https://render.com/docs/custom-domains)
- [DNS Propagation Checker](https://www.whatsmydns.net/)
- [SSL Certificate Checker](https://www.ssllabs.com/ssltest/)

---

**Need help?** Check the troubleshooting section or run the example script: `python3 scripts/custom-domain-example.py`
