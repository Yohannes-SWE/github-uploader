# 🔐 OAuth Authentication Guide

This guide covers how to connect domain providers using OAuth authentication, eliminating the need for users to manually enter API keys.

## 🎯 **Overview**

The OAuth authentication system provides:

- **One-click login**: Connect domain providers with a single click
- **Secure authentication**: No API keys stored on user devices
- **Automatic token management**: Handles token refresh and expiration
- **User-friendly experience**: Seamless integration with existing workflows

## 🚀 **How OAuth Works**

### **Traditional API Key Method**

1. User finds API credentials in provider dashboard
2. User manually copies API key and secret
3. User pastes credentials into the application
4. Credentials are stored and used for API calls

### **OAuth Method**

1. User clicks "Login with OAuth" button
2. User is redirected to provider's login page
3. User authorizes the application
4. Provider returns access token automatically
5. Application uses token for API calls

## 🔧 **Supported Providers**

### **1. GoDaddy OAuth**

- **OAuth Endpoint**: `https://sso.godaddy.com/v1/api/oauth2/authorize`
- **Scopes**: `domains:read`, `domains:write`
- **Features**: Full DNS management, domain registration

### **2. Cloudflare OAuth**

- **OAuth Endpoint**: `https://dash.cloudflare.com/oauth/authorize`
- **Scopes**: `zone:read`, `zone:edit`, `dns:read`, `dns:edit`
- **Features**: DNS management, CDN, DDoS protection

### **3. Namecheap OAuth**

- **OAuth Endpoint**: `https://api.sandbox.namecheap.com/xml.response`
- **Scopes**: `domains:read`, `domains:write`
- **Features**: DNS management, WHOIS privacy

### **4. Squarespace OAuth**

- **OAuth Endpoint**: `https://api.squarespace.com/1.0/oauth2/authorize`
- **Scopes**: `sites:read`, `sites:write`, `domains:read`, `domains:write`
- **Features**: DNS management, website builder integration

## 🛠️ **Setup Instructions**

### **For Application Administrators**

#### **1. Register OAuth Applications**

##### **GoDaddy**

1. Go to [GoDaddy Developer Portal](https://developer.godaddy.com/)
2. Create a new application
3. Set redirect URI to: `https://your-domain.com/api/domain-providers/oauth/callback/godaddy`
4. Note down Client ID and Client Secret

##### **Cloudflare**

1. Go to [Cloudflare Apps](https://www.cloudflare.com/apps/)
2. Create a new app
3. Set redirect URI to: `https://your-domain.com/api/domain-providers/oauth/callback/cloudflare`
4. Note down Client ID and Client Secret

##### **Namecheap**

1. Go to [Namecheap API](https://www.namecheap.com/support/api/)
2. Register your application
3. Set redirect URI to: `https://your-domain.com/api/domain-providers/oauth/callback/namecheap`
4. Note down Client ID and Client Secret

##### **Squarespace**

1. Go to [Squarespace Developer](https://developers.squarespace.com/)
2. Create a new app
3. Set redirect URI to: `https://your-domain.com/api/domain-providers/oauth/callback/squarespace`
4. Note down Client ID and Client Secret

#### **2. Configure Environment Variables**

```bash
# GoDaddy OAuth
export GODADDY_OAUTH_CLIENT_ID="your-godaddy-client-id"
export GODADDY_OAUTH_CLIENT_SECRET="your-godaddy-client-secret"

# Cloudflare OAuth
export CLOUDFLARE_OAUTH_CLIENT_ID="your-cloudflare-client-id"
export CLOUDFLARE_OAUTH_CLIENT_SECRET="your-cloudflare-client-secret"

# Namecheap OAuth
export NAMECHEAP_OAUTH_CLIENT_ID="your-namecheap-client-id"
export NAMECHEAP_OAUTH_CLIENT_SECRET="your-namecheap-client-secret"

# Squarespace OAuth
export SQUARESPACE_OAUTH_CLIENT_ID="your-squarespace-client-id"
export SQUARESPACE_OAUTH_CLIENT_SECRET="your-squarespace-client-secret"
```

### **For End Users**

#### **1. Connect Domain Provider**

1. **Navigate to Domain Providers**: Go to the domain providers section in the app
2. **Choose Provider**: Select your domain provider (GoDaddy, Cloudflare, etc.)
3. **Click OAuth Login**: Click "Login with OAuth" button
4. **Authorize Application**: Complete the OAuth flow on the provider's website
5. **Verify Connection**: Check that your domains are listed

#### **2. Deploy with Automated DNS**

Once connected, you can deploy applications with automatic DNS configuration:

```python
# Example deployment with OAuth-connected provider
result = deployer.deploy_with_automated_dns(
    github_repo="username/my-project",
    project_name="my-app",
    domain_config={
        "domain_provider": "godaddy",  # OAuth-connected provider
        "domains": {
            "frontend": "myapp.com",
            "backend": "api.myapp.com"
        }
    }
)
```

## 📋 **API Endpoints**

### **Get Supported Providers**

```bash
GET /api/domain-providers/supported
```

**Response:**

```json
{
  "status": "success",
  "providers": [
    {
      "name": "godaddy",
      "display_name": "GoDaddy",
      "auth_method": "oauth",
      "configured": true,
      "scopes": ["domains:read", "domains:write"],
      "features": [
        "DNS Management",
        "Domain Registration",
        "SSL Certificates",
        "OAuth Support"
      ]
    }
  ]
}
```

### **Initiate OAuth Login**

```bash
GET /api/domain-providers/oauth/login/{provider}
```

**Response:**

```json
{
  "auth_url": "https://sso.godaddy.com/v1/api/oauth2/authorize?client_id=...",
  "state": "secure-random-state",
  "provider": "godaddy"
}
```

### **OAuth Callback**

```bash
GET /api/domain-providers/oauth/callback/{provider}?code=...&state=...
```

**Response:**

```json
{
  "status": "success",
  "message": "GoDaddy account connected successfully via OAuth",
  "provider": "godaddy",
  "auth_method": "oauth",
  "user_info": {
    "username": "user@example.com",
    "name": "John Doe"
  },
  "domains_count": 5,
  "domains": [{ "name": "myapp.com", "status": "active" }]
}
```

### **Get OAuth Status**

```bash
GET /api/domain-providers/oauth/status
```

**Response:**

```json
{
  "status": "success",
  "oauth_configured": true,
  "providers": [
    {
      "name": "godaddy",
      "display_name": "GoDaddy",
      "configured": true,
      "scopes": ["domains:read", "domains:write"]
    }
  ]
}
```

## 🔄 **OAuth Flow Diagram**

```
User clicks "Login with OAuth"
           ↓
App requests OAuth URL
           ↓
User redirected to provider
           ↓
User authorizes application
           ↓
Provider redirects with code
           ↓
App exchanges code for token
           ↓
App stores token securely
           ↓
Provider connected successfully
```

## 🛡️ **Security Features**

### **1. Secure State Management**

- **Cryptographic state**: Uses secure random tokens
- **State expiration**: States expire after 10 minutes
- **State verification**: Prevents CSRF attacks

### **2. Token Security**

- **Access tokens**: Stored securely in session
- **Refresh tokens**: Handled automatically
- **Token expiration**: Monitored and refreshed

### **3. User Privacy**

- **Minimal scopes**: Only requested permissions needed
- **User consent**: Clear authorization prompts
- **Data protection**: Tokens encrypted in storage

## 📱 **User Interface**

### **Provider Selection Screen**

The OAuth interface shows:

- **Provider cards**: Visual representation of each provider
- **Auth method indicators**: OAuth vs API key options
- **Feature lists**: What each provider offers
- **Connection status**: Whether provider is connected

### **OAuth Flow**

1. **Login button**: Clear call-to-action for OAuth
2. **Popup window**: Secure OAuth flow in popup
3. **Progress indicators**: Show connection status
4. **Success confirmation**: Clear feedback on completion

## 🔧 **Configuration Examples**

### **Development Environment**

```bash
# .env file
GODADDY_OAUTH_CLIENT_ID=dev-godaddy-client-id
GODADDY_OAUTH_CLIENT_SECRET=dev-godaddy-client-secret
CLOUDFLARE_OAUTH_CLIENT_ID=dev-cloudflare-client-id
CLOUDFLARE_OAUTH_CLIENT_SECRET=dev-cloudflare-client-secret
```

### **Production Environment**

```bash
# Production environment variables
GODADDY_OAUTH_CLIENT_ID=prod-godaddy-client-id
GODADDY_OAUTH_CLIENT_SECRET=prod-godaddy-client-secret
CLOUDFLARE_OAUTH_CLIENT_ID=prod-cloudflare-client-id
CLOUDFLARE_OAUTH_CLIENT_SECRET=prod-cloudflare-client-secret
```

## 🚀 **Integration Examples**

### **React Component Usage**

```jsx
import DomainProviderOAuth from "./components/DomainProviderOAuth"

function App() {
  const handleProviderConnected = (provider) => {
    console.log(`${provider} connected successfully`)
    // Update UI or proceed with deployment
  }

  return <DomainProviderOAuth onProviderConnected={handleProviderConnected} />
}
```

### **Programmatic OAuth**

```python
from domain_providers_oauth import DomainProviderOAuthManager

# Initialize OAuth manager
oauth_manager = DomainProviderOAuthManager("https://your-domain.com")

# Get OAuth URL for user
oauth_data = oauth_manager.get_oauth_url("godaddy")
print(f"OAuth URL: {oauth_data['auth_url']}")

# Handle callback (in your web framework)
oauth_result = oauth_manager.handle_oauth_callback("godaddy", code, state)
domain_provider = oauth_result["domain_provider"]
```

## 🛠️ **Troubleshooting**

### **Common Issues**

#### **1. OAuth Not Configured**

**Symptoms:** "OAuth not configured for provider"
**Solutions:**

- Check environment variables are set
- Verify OAuth application registration
- Ensure redirect URIs match

#### **2. OAuth Callback Failed**

**Symptoms:** "OAuth callback failed"
**Solutions:**

- Check state parameter validity
- Verify code parameter
- Ensure callback URL is correct

#### **3. Token Exchange Failed**

**Symptoms:** "Token exchange failed"
**Solutions:**

- Verify client ID and secret
- Check redirect URI matches
- Ensure authorization code is valid

#### **4. User Info Retrieval Failed**

**Symptoms:** "Failed to get user info"
**Solutions:**

- Check access token validity
- Verify API permissions
- Ensure scopes are correct

### **Debugging Commands**

```bash
# Check OAuth configuration
curl -X GET "https://your-domain.com/api/domain-providers/oauth/status"

# Test OAuth URL generation
curl -X GET "https://your-domain.com/api/domain-providers/oauth/login/godaddy"

# Check provider status
curl -X GET "https://your-domain.com/api/domain-providers/supported"
```

## 📚 **Provider-Specific Notes**

### **GoDaddy**

- Uses GoDaddy SSO OAuth 2.0
- Requires domain management permissions
- Supports automatic token refresh

### **Cloudflare**

- Uses Cloudflare OAuth 2.0
- Requires zone-level permissions
- Includes CDN and security features

### **Namecheap**

- Uses Namecheap API OAuth
- Requires domain management access
- Supports WHOIS privacy features

### **Squarespace**

- Uses Squarespace OAuth 2.0
- Includes website builder integration
- Supports e-commerce features

## 🔐 **Security Best Practices**

### **For Administrators**

1. **Use HTTPS**: Always use HTTPS in production
2. **Secure storage**: Store client secrets securely
3. **Monitor usage**: Track OAuth usage and errors
4. **Regular rotation**: Rotate client secrets periodically

### **For Users**

1. **Verify URLs**: Ensure you're on the correct provider site
2. **Check permissions**: Review requested permissions
3. **Revoke access**: Remove access when no longer needed
4. **Monitor activity**: Check for suspicious activity

## 📞 **Support**

### **Getting Help**

1. Check OAuth configuration
2. Verify provider registration
3. Test OAuth flow manually
4. Review error logs

### **Useful Resources**

- [OAuth 2.0 Specification](https://tools.ietf.org/html/rfc6749)
- [GoDaddy Developer Portal](https://developer.godaddy.com/)
- [Cloudflare API Documentation](https://developers.cloudflare.com/api/)
- [Namecheap API Documentation](https://www.namecheap.com/support/api/)
- [Squarespace Developer](https://developers.squarespace.com/)

---

**Need help?** Check the troubleshooting section or contact support for OAuth-specific issues.
