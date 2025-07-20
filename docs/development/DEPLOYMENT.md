# 🚀 Production Deployment Guide

This guide covers deploying the GitHub Uploader to production with comprehensive setup instructions and troubleshooting.

## 🎯 **Recommended: Render (Best Free Option)**

### Why Render?

- ✅ **Truly Free**: 750 hours/month
- ✅ **Easy Setup**: Connect GitHub repo
- ✅ **Auto-deploy**: Updates on push
- ✅ **Good Performance**: Fast response times
- ✅ **HTTPS**: Automatic SSL certificates
- ⚠️ **Sleep Mode**: Auto-sleeps after 15 min inactivity

### Step-by-Step Render Deployment

#### 1. **Prepare Your Repository**

```bash
# Ensure your repo is up to date
git add .
git commit -m "Prepare for production deployment"
git push origin main
```

#### 2. **Set Up GitHub OAuth App**

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Click "New OAuth App"
3. Configure:
   - **Application name**: `GitHub Uploader`
   - **Homepage URL**: `https://github-uploader-frontend.onrender.com`
   - **Authorization callback URL**: `https://github-uploader-backend.onrender.com/api/auth/github/callback`
4. Copy **Client ID** and **Client Secret**

#### 3. **Deploy Backend to Render**

1. Go to [render.com](https://render.com) and create account
2. Click "New Web Service"
3. Connect your GitHub repository
4. Configure:

   - **Name**: `github-uploader-backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: `server`

5. **Set Environment Variables**:

   ```
   ENVIRONMENT=production
   GITHUB_CLIENT_ID=your_github_client_id
   GITHUB_CLIENT_SECRET=your_github_client_secret
   SECRET_KEY=your_secure_secret_key_here
   OPENAI_API_KEY=your_openai_api_key
   BASE_URL=https://github-uploader-backend.onrender.com
   GITHUB_CALLBACK_URL=https://github-uploader-backend.onrender.com/api/auth/github/callback
   ALLOWED_ORIGINS=https://github-uploader-frontend.onrender.com
   ```

6. Click "Create Web Service"

#### 4. **Deploy Frontend to Render**

1. Click "New Static Site"
2. Connect your GitHub repository
3. Configure:

   - **Name**: `github-uploader-frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `client/build`
   - **Root Directory**: `client`

4. **Set Environment Variables**:

   ```
   REACT_APP_API_URL=https://github-uploader-backend.onrender.com
   REACT_APP_ENVIRONMENT=production
   ```

5. Click "Create Static Site"

#### 5. **Update GitHub OAuth App**

1. Go back to GitHub Developer Settings
2. Update your OAuth app URLs:
   - **Homepage**: `https://github-uploader-frontend.onrender.com`
   - **Callback URL**: `https://github-uploader-backend.onrender.com/api/auth/github/callback`

## 🆓 **Alternative Free Options**

### Railway

- **Free**: $5 credit/month
- **Setup**: Similar to Render
- **Pros**: Better performance, no sleep mode

#### Railway Deployment:

1. Go to [railway.app](https://railway.app)
2. Connect GitHub repository
3. Deploy backend:
   - **Root Directory**: `server`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Set environment variables (same as Render)
5. Deploy frontend to Vercel/Netlify

### Vercel (Frontend) + Railway (Backend)

#### Vercel Frontend Setup:

1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Configure:

   - **Framework Preset**: Create React App
   - **Root Directory**: `client`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

4. **Set Environment Variables**:
   ```
   REACT_APP_API_URL=https://your-railway-backend.railway.app
   REACT_APP_ENVIRONMENT=production
   ```

### Netlify (Frontend) + Railway (Backend)

#### Netlify Frontend Setup:

1. Go to [netlify.com](https://netlify.com)
2. Connect GitHub repository
3. Configure:

   - **Base directory**: `client`
   - **Build command**: `npm run build`
   - **Publish directory**: `build`

4. **Set Environment Variables**:
   ```
   REACT_APP_API_URL=https://your-railway-backend.railway.app
   REACT_APP_ENVIRONMENT=production
   ```

## 🔧 **Production Environment Variables**

### Required Variables:

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

# URLs
BASE_URL=https://your-backend-domain.com
FRONTEND_URL=https://your-frontend-domain.com
GITHUB_CALLBACK_URL=https://your-backend-domain.com/api/auth/github/callback
ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### Frontend Variables:

```bash
REACT_APP_API_URL=https://your-backend-domain.com
REACT_APP_ENVIRONMENT=production
```

## 🐳 **Docker Deployment**

### Production Docker Compose:

```yaml
version: "3.8"
services:
  backend:
    build: ./server
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - GITHUB_CLIENT_ID=${GITHUB_CLIENT_ID}
      - GITHUB_CLIENT_SECRET=${GITHUB_CLIENT_SECRET}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - SECRET_KEY=${SECRET_KEY}
      - BASE_URL=${BASE_URL}
      - GITHUB_CALLBACK_URL=${GITHUB_CALLBACK_URL}
      - ALLOWED_ORIGINS=${ALLOWED_ORIGINS}
    restart: unless-stopped

  frontend:
    build: ./client
    ports:
      - "3000:80"
    environment:
      - REACT_APP_API_URL=${REACT_APP_API_URL}
      - REACT_APP_ENVIRONMENT=production
    depends_on:
      - backend
    restart: unless-stopped
```

### Deploy with Docker:

```bash
# Build and run
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop services
docker-compose -f docker-compose.prod.yml down
```

## 🔍 **Pre-Deployment Testing**

### Local Production Testing:

```bash
# Test backend
cd server
ENVIRONMENT=production python -m uvicorn main:app --host 0.0.0.0 --port 8000

# Test frontend
cd client
REACT_APP_API_URL=http://localhost:8000 npm start
```

### Environment Variable Testing:

```bash
# Test environment loading
cd server
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Environment loaded successfully')"
```

## 📝 **Post-Deployment Checklist**

- [ ] Backend is accessible at your production URL
- [ ] Frontend is accessible at your production URL
- [ ] GitHub OAuth callback URLs updated
- [ ] Environment variables set correctly
- [ ] Test login flow works
- [ ] Test file upload works
- [ ] Test AI analysis works
- [ ] Test CI/CD generation works
- [ ] HTTPS certificates are working
- [ ] CORS is configured correctly

## 🆘 **Troubleshooting**

### Common Issues:

#### Backend Not Starting:

```bash
# Check logs
docker logs <container_id>

# Verify environment variables
echo $GITHUB_CLIENT_ID
echo $OPENAI_API_KEY

# Check Python version
python --version
```

#### Frontend Not Loading:

```bash
# Check build logs
npm run build

# Verify API URL
echo $REACT_APP_API_URL

# Clear browser cache
# Hard refresh: Ctrl+Shift+R
```

#### OAuth Not Working:

1. **Verify callback URLs** in GitHub OAuth app
2. **Check if backend URL is accessible**
3. **Ensure environment variables are set**
4. **Check CORS configuration**

#### CORS Errors:

```bash
# Check allowed origins
echo $ALLOWED_ORIGINS

# Verify frontend URL is in allowed origins
# Update CORS configuration if needed
```

### Debug Mode:

```bash
# Enable debug logging
DEBUG=true python -m uvicorn main:app --host 0.0.0.0 --port 8000

# Check detailed logs
tail -f /var/log/application.log
```

## 🔒 **Security Considerations**

### Production Security:

1. **Use strong SECRET_KEY**:

   ```bash
   # Generate secure secret key
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Enable HTTPS only**:

   ```python
   # In production, set https_only=True
   app.add_middleware(
       SessionMiddleware,
       secret_key=SECRET_KEY,
       https_only=True
   )
   ```

3. **Rate limiting**:

   ```python
   # Add rate limiting middleware
   from slowapi import Limiter, _rate_limit_exceeded_handler
   from slowapi.util import get_remote_address
   ```

4. **Input validation**:
   ```python
   # Validate all inputs
   from pydantic import BaseModel, validator
   ```

## 📊 **Monitoring & Analytics**

### Health Check Endpoint:

```python
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }
```

### Logging Configuration:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## 🚀 **Performance Optimization**

### Backend Optimizations:

1. **Enable compression**:

   ```python
   from fastapi.middleware.gzip import GZipMiddleware
   app.add_middleware(GZipMiddleware, minimum_size=1000)
   ```

2. **Add caching**:

   ```python
   from fastapi_cache import FastAPICache
   from fastapi_cache.backends.redis import RedisBackend
   ```

3. **Database connection pooling** (if using database)

### Frontend Optimizations:

1. **Code splitting**:

   ```javascript
   const LazyComponent = React.lazy(() => import("./LazyComponent"))
   ```

2. **Image optimization**:

   ```javascript
   // Use WebP format and lazy loading
   <img loading="lazy" src="image.webp" alt="description" />
   ```

3. **Bundle analysis**:
   ```bash
   npm run analyze
   ```

---

**Your GitHub Uploader is now ready for production deployment! 🎉**
