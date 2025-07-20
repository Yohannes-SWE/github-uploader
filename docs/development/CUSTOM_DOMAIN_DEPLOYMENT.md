# 🚀 Custom Domain Deployment Guide - repotorpedo.com

This guide covers deploying the GitHub Uploader to your custom domain `repotorpedo.com` with proper DNS configuration and platform setup.

## 🎯 **Deployment Strategy**

### Recommended Architecture:

- **Frontend**: `repotorpedo.com` (main domain)
- **Backend**: `api.repotorpedo.com` (subdomain)
- **Platform**: Render, Railway, or Vercel + Railway

## 📋 **Pre-Deployment Checklist**

### 1. **Domain DNS Configuration**

You'll need to configure DNS records for your domain. Here are the recommended settings:

#### For Render Deployment:

```
# Frontend (repotorpedo.com)
Type: CNAME
Name: @
Value: your-frontend-service.onrender.com

# Backend (api.repotorpedo.com)
Type: CNAME
Name: api
Value: your-backend-service.onrender.com

# www subdomain (optional)
Type: CNAME
Name: www
Value: repotorpedo.com
```

#### For Railway Deployment:

```
# Frontend (repotorpedo.com)
Type: CNAME
Name: @
Value: your-frontend-service.railway.app

# Backend (api.repotorpedo.com)
Type: CNAME
Name: api
Value: your-backend-service.railway.app
```

#### For Vercel + Railway:

```
# Frontend (repotorpedo.com)
Type: CNAME
Name: @
Value: cname.vercel-dns.com

# Backend (api.repotorpedo.com)
Type: CNAME
Name: api
Value: your-railway-backend.railway.app
```

### 2. **GitHub OAuth App Configuration**

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Create or update your OAuth App:
   - **Application name**: `Repo Torpedo`
   - **Homepage URL**: `https://repotorpedo.com`
   - **Authorization callback URL**: `https://api.repotorpedo.com/api/auth/github/callback`

## 🚀 **Deployment Options**

### Option 1: Render (Recommended)

#### Backend Deployment:

1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect your GitHub repository
4. Configure:

   - **Name**: `repotorpedo-backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: `server`

5. **Set Environment Variables**:
   ```
   ENVIRONMENT=production
   GITHUB_CLIENT_ID=your_github_client_id
   GITHUB_CLIENT_SECRET=your_github_client_secret
   SECRET_KEY=your_secure_secret_key
   OPENAI_API_KEY=your_openai_api_key
   BASE_URL=https://api.repotorpedo.com
   GITHUB_CALLBACK_URL=https://api.repotorpedo.com/api/auth/github/callback
   ALLOWED_ORIGINS=https://repotorpedo.com,https://www.repotorpedo.com
   ```

#### Frontend Deployment:

1. Create new Static Site
2. Configure:

   - **Name**: `repotorpedo-frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `client/build`
   - **Root Directory**: `client`

3. **Set Environment Variables**:

   ```
   REACT_APP_API_URL=https://api.repotorpedo.com
   REACT_APP_ENVIRONMENT=production
   ```

4. **Custom Domain Setup**:
   - Go to Settings → Custom Domains
   - Add `repotorpedo.com`
   - Update DNS records as shown above

### Option 2: Railway + Vercel

#### Backend (Railway):

1. Go to [railway.app](https://railway.app)
2. Deploy your repository
3. Configure:

   - **Root Directory**: `server`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Set Environment Variables** (same as Render)

5. **Custom Domain Setup**:
   - Go to Settings → Domains
   - Add `api.repotorpedo.com`
   - Update DNS records

#### Frontend (Vercel):

1. Go to [vercel.com](https://vercel.com)
2. Import your repository
3. Configure:

   - **Framework Preset**: Create React App
   - **Root Directory**: `client`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

4. **Set Environment Variables**:

   ```
   REACT_APP_API_URL=https://api.repotorpedo.com
   REACT_APP_ENVIRONMENT=production
   ```

5. **Custom Domain Setup**:
   - Go to Settings → Domains
   - Add `repotorpedo.com`
   - Update DNS records

### Option 3: Vercel (Full Stack)

#### Deploy Both Frontend and Backend:

1. Go to [vercel.com](https://vercel.com)
2. Import your repository
3. Configure:

   - **Framework Preset**: Other
   - **Root Directory**: `client`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

4. **Set Environment Variables**:

   ```
   REACT_APP_API_URL=https://api.repotorpedo.com
   REACT_APP_ENVIRONMENT=production
   ```

5. **Deploy Backend Separately**:
   - Create another Vercel project for backend
   - Root Directory: `server`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## 🔧 **DNS Configuration Steps**

### Squarespace DNS Management:

1. **Log into Squarespace**
2. **Go to Settings → Domains**
3. **Click on repotorpedo.com**
4. **Go to DNS Settings**
5. **Add DNS Records**:

#### For Render:

```
Type: CNAME
Name: api
Value: your-backend-service.onrender.com
TTL: 3600

Type: CNAME
Name: @
Value: your-frontend-service.onrender.com
TTL: 3600
```

#### For Railway:

```
Type: CNAME
Name: api
Value: your-backend-service.railway.app
TTL: 3600

Type: CNAME
Name: @
Value: your-frontend-service.railway.app
TTL: 3600
```

#### For Vercel:

```
Type: CNAME
Name: @
Value: cname.vercel-dns.com
TTL: 3600

Type: CNAME
Name: api
Value: your-backend-service.railway.app
TTL: 3600
```

## 📝 **Environment Configuration**

### Create `.env` file for production:

```bash
# Environment
ENVIRONMENT=production

# GitHub OAuth
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

# OpenAI API
OPENAI_API_KEY=your_openai_api_key

# Security
SECRET_KEY=your_secure_secret_key_here

# Custom Domain URLs
BASE_URL=https://api.repotorpedo.com
FRONTEND_URL=https://repotorpedo.com
GITHUB_CALLBACK_URL=https://api.repotorpedo.com/api/auth/github/callback
ALLOWED_ORIGINS=https://repotorpedo.com,https://www.repotorpedo.com
```

### Frontend Environment Variables:

```bash
REACT_APP_API_URL=https://api.repotorpedo.com
REACT_APP_ENVIRONMENT=production
```

## 🔍 **Testing Your Deployment**

### 1. **DNS Propagation Check**:

```bash
# Check if DNS is propagated
nslookup api.repotorpedo.com
nslookup repotorpedo.com
```

### 2. **Health Check**:

```bash
# Test backend health
curl https://api.repotorpedo.com/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00.000000",
  "version": "2.0.0",
  "environment": "production"
}
```

### 3. **Frontend Test**:

- Visit `https://repotorpedo.com`
- Check if the app loads correctly
- Test GitHub OAuth login
- Test file upload functionality

## 🆘 **Troubleshooting**

### Common Issues:

#### DNS Not Working:

1. **Wait for propagation** (can take up to 48 hours)
2. **Check DNS records** are correct
3. **Verify TTL settings**
4. **Use DNS checker tools** like whatsmydns.net

#### SSL Certificate Issues:

1. **Wait for SSL provisioning** (automatic on most platforms)
2. **Check if custom domain is properly configured**
3. **Verify DNS records are pointing to the right place**

#### OAuth Not Working:

1. **Verify callback URL** in GitHub OAuth app
2. **Check environment variables** are set correctly
3. **Ensure backend is accessible** at api.repotorpedo.com

#### CORS Errors:

1. **Check ALLOWED_ORIGINS** includes your domain
2. **Verify frontend and backend URLs** are correct
3. **Clear browser cache** and try again

### Debug Commands:

```bash
# Check DNS resolution
dig api.repotorpedo.com
dig repotorpedo.com

# Test HTTPS
curl -I https://api.repotorpedo.com/health
curl -I https://repotorpedo.com

# Check SSL certificate
openssl s_client -connect api.repotorpedo.com:443 -servername api.repotorpedo.com
```

## 🎯 **Post-Deployment Checklist**

- [ ] DNS records are configured correctly
- [ ] SSL certificates are working
- [ ] Backend is accessible at `https://api.repotorpedo.com`
- [ ] Frontend is accessible at `https://repotorpedo.com`
- [ ] GitHub OAuth app is configured with correct URLs
- [ ] Environment variables are set correctly
- [ ] OAuth login flow works
- [ ] File upload functionality works
- [ ] AI analysis works
- [ ] CI/CD generation works

## 🚀 **Performance Optimization**

### For Custom Domain:

1. **Enable CDN** (if available on your platform)
2. **Configure caching headers**
3. **Enable compression**
4. **Use HTTP/2** (automatic on most platforms)

### Monitoring:

1. **Set up uptime monitoring** for both domains
2. **Configure error tracking** (Sentry, LogRocket)
3. **Set up analytics** (Google Analytics, Plausible)

---

**Your GitHub Uploader will be live at `https://repotorpedo.com` with API at `https://api.repotorpedo.com`! 🎉**
