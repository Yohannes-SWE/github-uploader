# 🚀 Deployment Guide - Free Options

## 🎯 **Recommended: Render (Best Free Option)**

### Why Render?

- ✅ **Truly Free**: 750 hours/month
- ✅ **Easy Setup**: Connect GitHub repo
- ✅ **Auto-deploy**: Updates on push
- ✅ **Good Performance**: Fast response times
- ⚠️ **Sleep Mode**: Auto-sleeps after 15 min inactivity

### Deploy to Render:

1. **Sign up**: Go to [render.com](https://render.com) and create account
2. **Connect GitHub**: Link your GitHub repository
3. **Deploy Backend**:

   - Click "New Web Service"
   - Select your repo
   - **Name**: `github-uploader-backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: `server`

4. **Set Environment Variables**:

   - `GITHUB_CLIENT_ID`: Your GitHub OAuth Client ID
   - `GITHUB_CLIENT_SECRET`: Your GitHub OAuth Client Secret
   - `SECRET_KEY`: Your secret key
   - `OPENAI_API_KEY`: Your OpenAI API key

5. **Deploy Frontend**:

   - Click "New Static Site"
   - Select your repo
   - **Name**: `github-uploader-frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `client/build`
   - **Root Directory**: `client`

6. **Update GitHub OAuth**:
   - Go to GitHub Developer Settings
   - Update your OAuth app:
     - **Homepage**: `https://your-frontend-name.onrender.com`
     - **Callback URL**: `https://your-backend-name.onrender.com/auth/github/callback`

## 🆓 **Alternative Free Options:**

### Railway

- **Free**: $5 credit/month
- **Setup**: Similar to Render
- **Pros**: Better performance, no sleep mode

### Vercel (Frontend Only)

- **Free**: Unlimited static sites
- **Setup**: Connect repo, auto-deploy
- **Note**: Backend needs separate hosting

### Netlify (Frontend Only)

- **Free**: 100GB bandwidth
- **Setup**: Drag & drop or Git integration
- **Note**: Backend needs separate hosting

## 🔧 **Local Testing Before Deploy:**

```bash
# Test backend
cd server
python3.11 -m uvicorn main:app --host 0.0.0.0 --port 8000

# Test frontend
cd client
npm start
```

## 📝 **Post-Deployment Checklist:**

- [ ] Backend is accessible at your Render URL
- [ ] Frontend is accessible at your Render URL
- [ ] GitHub OAuth callback URLs updated
- [ ] Environment variables set correctly
- [ ] Test login flow works
- [ ] Test file upload works

## 🆘 **Troubleshooting:**

**Backend not starting?**

- Check environment variables
- Verify Python 3.11+ is used
- Check build logs in Render dashboard

**Frontend not loading?**

- Verify build completed successfully
- Check if API URL is correct
- Clear browser cache

**OAuth not working?**

- Verify callback URLs in GitHub OAuth app
- Check if backend URL is accessible
- Ensure environment variables are set
