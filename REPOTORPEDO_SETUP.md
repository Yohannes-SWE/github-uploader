# 🚀 Quick Setup Guide - repotorpedo.com

This guide will get your GitHub Uploader live on `repotorpedo.com` in under 30 minutes!

## 📋 **Prerequisites**

- GitHub account
- OpenAI API key
- Squarespace domain access (repotorpedo.com)

## ⚡ **Quick Start (5 Steps)**

### Step 1: Set Up GitHub OAuth App

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Click "New OAuth App"
3. Fill in:
   - **Application name**: `Repo Torpedo`
   - **Homepage URL**: `https://repotorpedo.com`
   - **Authorization callback URL**: `https://api.repotorpedo.com/api/auth/github/callback`
4. Copy the **Client ID** and **Client Secret**

### Step 2: Deploy to Render (Free)

1. Go to [render.com](https://render.com) and sign up
2. Click "New Web Service"
3. Connect your GitHub repository
4. Configure backend:

   - **Name**: `repotorpedo-backend`
   - **Root Directory**: `server`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. Set environment variables:

   ```
   ENVIRONMENT=production
   GITHUB_CLIENT_ID=your_client_id_here
   GITHUB_CLIENT_SECRET=your_client_secret_here
   SECRET_KEY=your_secret_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   BASE_URL=https://api.repotorpedo.com
   GITHUB_CALLBACK_URL=https://api.repotorpedo.com/api/auth/github/callback
   ALLOWED_ORIGINS=https://repotorpedo.com,https://www.repotorpedo.com
   ```

6. Create frontend service:

   - Click "New Static Site"
   - **Name**: `repotorpedo-frontend`
   - **Root Directory**: `client`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `client/build`

7. Set frontend environment variables:
   ```
   REACT_APP_API_URL=https://api.repotorpedo.com
   REACT_APP_ENVIRONMENT=production
   ```

### Step 3: Configure Custom Domains in Render

1. **Backend Domain**:

   - Go to your backend service settings
   - Click "Custom Domains"
   - Add `api.repotorpedo.com`

2. **Frontend Domain**:
   - Go to your frontend service settings
   - Click "Custom Domains"
   - Add `repotorpedo.com`

### Step 4: Configure DNS in Squarespace

1. Log into Squarespace
2. Go to Settings → Domains
3. Click on repotorpedo.com
4. Go to DNS Settings
5. Add these records:

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

### Step 5: Test Your Deployment

1. Wait 5-10 minutes for DNS propagation
2. Visit `https://repotorpedo.com`
3. Test GitHub login
4. Test file upload

## 🔧 **Alternative: Railway + Vercel**

### Backend (Railway):

1. Go to [railway.app](https://railway.app)
2. Deploy your repository
3. Set environment variables (same as above)
4. Add custom domain: `api.repotorpedo.com`

### Frontend (Vercel):

1. Go to [vercel.com](https://vercel.com)
2. Import your repository
3. Configure:
   - **Root Directory**: `client`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
4. Set environment variables:
   ```
   REACT_APP_API_URL=https://api.repotorpedo.com
   REACT_APP_ENVIRONMENT=production
   ```
5. Add custom domain: `repotorpedo.com`

## 🎯 **Environment Variables Summary**

### Backend Variables:

```bash
ENVIRONMENT=production
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
SECRET_KEY=your_secure_secret_key
OPENAI_API_KEY=your_openai_api_key
BASE_URL=https://api.repotorpedo.com
GITHUB_CALLBACK_URL=https://api.repotorpedo.com/api/auth/github/callback
ALLOWED_ORIGINS=https://repotorpedo.com,https://www.repotorpedo.com
```

### Frontend Variables:

```bash
REACT_APP_API_URL=https://api.repotorpedo.com
REACT_APP_ENVIRONMENT=production
```

## 🚨 **Common Issues & Solutions**

### DNS Not Working:

- Wait up to 48 hours for full propagation
- Check DNS records are correct
- Use [whatsmydns.net](https://whatsmydns.net) to check propagation

### SSL Certificate Issues:

- Wait 10-15 minutes after adding custom domain
- Ensure DNS is pointing to the right place
- Check if custom domain is properly configured in platform

### OAuth Not Working:

- Verify callback URL in GitHub OAuth app
- Check environment variables are set correctly
- Ensure backend is accessible at api.repotorpedo.com

## 🎉 **You're Done!**

Your GitHub Uploader will be live at:

- **Frontend**: https://repotorpedo.com
- **Backend**: https://api.repotorpedo.com

## 📞 **Need Help?**

1. Check the full deployment guide: `DEPLOYMENT.md`
2. Run the custom domain script: `./scripts/deploy-custom-domain.sh --help`
3. Test your deployment: `./scripts/deploy-custom-domain.sh --test`

---

**Happy deploying! 🚀**
