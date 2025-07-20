# Universal GitHub OAuth Configuration
# This file contains the OAuth credentials for the universal GitHub OAuth app
# Update these values with your actual GitHub OAuth app credentials

# GitHub OAuth App credentials
UNIVERSAL_GITHUB_CLIENT_ID = "your_github_client_id_here"
UNIVERSAL_GITHUB_CLIENT_SECRET = "your_github_client_secret_here"

# OAuth App settings
GITHUB_OAUTH_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_OAUTH_ACCESS_TOKEN_URL = "https://github.com/login/oauth/access_token"

# Callback URL (update this to match your deployment)
CALLBACK_URL = "https://api.repotorpedo.com/api/auth/github/callback"

# Scopes requested
SCOPES = ["repo", "user"]

# Security settings
STATE_TIMEOUT = 300  # 5 minutes
MAX_STATES = 1000  # Maximum number of pending states to store
