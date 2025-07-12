# Universal OAuth Setup Guide

This guide explains how to set up a universal GitHub OAuth system that works for all users without requiring individual setup.

## Overview

The universal OAuth system uses a single GitHub OAuth application that all users share. This eliminates the need for each user to create their own OAuth app, making the deployment process completely automated.

## Step 1: Create Universal GitHub OAuth App

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Click "New OAuth App"
3. Fill in the following details:
   - **Application name**: `RepoTorpedo Universal` (or your preferred name)
   - **Homepage URL**: `https://repotorpedo-frontend.onrender.com`
   - **Authorization callback URL**: `https://repotorpedo-backend.onrender.com/api/auth/github/callback`
4. Click "Register application"
5. Copy the **Client ID** and **Client Secret**

## Step 2: Configure OAuth Credentials

### Option A: Environment Variables (Recommended for Production)

Set these environment variables in your Render dashboard:

```bash
UNIVERSAL_GITHUB_CLIENT_ID=your_client_id_here
UNIVERSAL_GITHUB_CLIENT_SECRET=your_client_secret_here
```

### Option B: Configuration File (For Development)

Edit `server/oauth_config.py`:

```python
UNIVERSAL_GITHUB_CLIENT_ID = "your_client_id_here"
UNIVERSAL_GITHUB_CLIENT_SECRET = "your_client_secret_here"
```

## Step 3: Update Render Configuration

Update your `render.yaml` to include the OAuth environment variables:

```yaml
services:
  - type: web
    name: repotorpedo-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    rootDir: server
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: ENVIRONMENT
        value: production
      - key: UNIVERSAL_GITHUB_CLIENT_ID
        sync: false # Set this in Render dashboard
      - key: UNIVERSAL_GITHUB_CLIENT_SECRET
        sync: false # Set this in Render dashboard
      - key: SECRET_KEY
        sync: false
      - key: OPENAI_API_KEY
        sync: false
      - key: BASE_URL
        value: https://repotorpedo-backend.onrender.com
      - key: GITHUB_CALLBACK_URL
        value: https://repotorpedo-backend.onrender.com/api/auth/github/callback
      - key: ALLOWED_ORIGINS
        value: https://repotorpedo-frontend.onrender.com
```

## Step 4: Set Environment Variables in Render

1. Go to your [Render Dashboard](https://dashboard.render.com)
2. Find your `repotorpedo-backend` service
3. Click on it to open the service details
4. Go to the "Environment" tab
5. Add these environment variables:
   - **Key**: `UNIVERSAL_GITHUB_CLIENT_ID` | **Value**: `[Your GitHub Client ID]`
   - **Key**: `UNIVERSAL_GITHUB_CLIENT_SECRET` | **Value**: `[Your GitHub Client Secret]`
   - **Key**: `SECRET_KEY` | **Value**: `[Any random string for session encryption]`
6. Click "Save Changes"
7. The service will automatically redeploy

## Step 5: Test the OAuth Flow

1. Visit your frontend: `https://repotorpedo-frontend.onrender.com`
2. Click "Continue with GitHub"
3. You should be redirected to GitHub's authorization page
4. After authorizing, you should be redirected back to your frontend
5. The OAuth flow should work for all users without any setup

## Security Features

The universal OAuth system includes several security features:

- **State Parameter**: Each OAuth request includes a secure random state to prevent CSRF attacks
- **State Validation**: The callback validates the state parameter before processing
- **State Cleanup**: Old states are automatically cleaned up
- **Session Management**: User sessions are managed securely with session cookies

## Benefits of Universal OAuth

1. **No User Setup Required**: Users don't need to create their own OAuth apps
2. **Simplified Deployment**: One-time setup works for all users
3. **Better Security**: Centralized credential management
4. **Easier Maintenance**: Single OAuth app to maintain
5. **Faster Onboarding**: Users can start using the app immediately

## Troubleshooting

### OAuth App Not Found Error

- Ensure the Client ID and Client Secret are correct
- Check that the environment variables are set in Render
- Verify the OAuth app is properly configured on GitHub

### Callback URL Mismatch

- Make sure the callback URL in GitHub matches exactly: `https://repotorpedo-backend.onrender.com/api/auth/github/callback`
- Check that the `GITHUB_CALLBACK_URL` environment variable is set correctly

### CORS Errors

- Ensure `ALLOWED_ORIGINS` includes your frontend URL
- Check that the backend is running in production mode

### Session Issues

- Make sure `SECRET_KEY` is set for session encryption
- Verify that cookies are being set correctly

## Production Considerations

1. **Use Environment Variables**: Always use environment variables for OAuth credentials in production
2. **Secure Secret Key**: Use a strong, random secret key for session encryption
3. **HTTPS Only**: Ensure all OAuth flows use HTTPS
4. **Rate Limiting**: Consider implementing rate limiting for OAuth endpoints
5. **Monitoring**: Monitor OAuth success/failure rates

## Support

If you encounter issues:

1. Check the backend logs in Render dashboard
2. Verify all environment variables are set correctly
3. Test the OAuth flow in an incognito browser window
4. Ensure your GitHub OAuth app has the correct scopes (`repo` and `user`)
