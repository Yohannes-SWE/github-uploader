import requests
import json
import time
import os
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod
from urllib.parse import urlencode, parse_qs
import secrets


class OAuthProvider(ABC):
    """Abstract base class for OAuth-enabled domain providers"""

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.auth_url = self.get_auth_url()
        self.token_url = self.get_token_url()

    @abstractmethod
    def get_auth_url(self) -> str:
        """Get the OAuth authorization URL"""
        pass

    @abstractmethod
    def get_token_url(self) -> str:
        """Get the OAuth token exchange URL"""
        pass

    @abstractmethod
    def get_scopes(self) -> List[str]:
        """Get required OAuth scopes"""
        pass

    @abstractmethod
    def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        pass

    @abstractmethod
    def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get user information using access token"""
        pass

    @abstractmethod
    def create_domain_provider(self, access_token: str) -> Any:
        """Create a domain provider instance with the access token"""
        pass


class GoDaddyOAuth(OAuthProvider):
    """GoDaddy OAuth integration"""

    def get_auth_url(self) -> str:
        return "https://sso.godaddy.com/v1/api/oauth2/authorize"

    def get_token_url(self) -> str:
        return "https://sso.godaddy.com/v1/api/oauth2/token"

    def get_scopes(self) -> List[str]:
        return ["domains:read", "domains:write"]

    def build_auth_url(self, state: str) -> str:
        """Build the OAuth authorization URL"""
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": " ".join(self.get_scopes()),
            "state": state,
        }
        return f"{self.auth_url}?{urlencode(params)}"

    def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
        }

        response = requests.post(self.token_url, data=data)

        if response.status_code == 200:
            token_data = response.json()
            return {
                "access_token": token_data.get("access_token"),
                "refresh_token": token_data.get("refresh_token"),
                "expires_in": token_data.get("expires_in"),
                "token_type": token_data.get("token_type", "Bearer"),
            }
        else:
            raise Exception(f"Token exchange failed: {response.text}")

    def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get user information from GoDaddy"""
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(
            "https://api.godaddy.com/v1/user/profile", headers=headers
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get user info: {response.text}")

    def create_domain_provider(self, access_token: str) -> Any:
        """Create GoDaddy domain provider with OAuth token"""
        from domain_providers import GoDaddyProvider

        # GoDaddy OAuth tokens can be used directly as API keys
        return GoDaddyProvider(access_token, None)


class CloudflareOAuth(OAuthProvider):
    """Cloudflare OAuth integration"""

    def get_auth_url(self) -> str:
        return "https://dash.cloudflare.com/oauth/authorize"

    def get_token_url(self) -> str:
        return "https://dash.cloudflare.com/oauth/token"

    def get_scopes(self) -> List[str]:
        return ["zone:read", "zone:edit", "dns:read", "dns:edit"]

    def build_auth_url(self, state: str) -> str:
        """Build the OAuth authorization URL"""
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": " ".join(self.get_scopes()),
            "state": state,
        }
        return f"{self.auth_url}?{urlencode(params)}"

    def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
        }

        response = requests.post(self.token_url, data=data)

        if response.status_code == 200:
            token_data = response.json()
            return {
                "access_token": token_data.get("access_token"),
                "refresh_token": token_data.get("refresh_token"),
                "expires_in": token_data.get("expires_in"),
                "token_type": token_data.get("token_type", "Bearer"),
            }
        else:
            raise Exception(f"Token exchange failed: {response.text}")

    def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get user information from Cloudflare"""
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(
            "https://api.cloudflare.com/client/v4/user", headers=headers
        )

        if response.status_code == 200:
            data = response.json()
            return data.get("result", {})
        else:
            raise Exception(f"Failed to get user info: {response.text}")

    def create_domain_provider(self, access_token: str) -> Any:
        """Create Cloudflare domain provider with OAuth token"""
        from domain_providers import CloudflareProvider

        return CloudflareProvider(access_token)


class NamecheapOAuth(OAuthProvider):
    """Namecheap OAuth integration"""

    def get_auth_url(self) -> str:
        return (
            "https://api.sandbox.namecheap.com/xml.response"  # Use sandbox for testing
        )

    def get_token_url(self) -> str:
        return "https://api.sandbox.namecheap.com/xml.response"

    def get_scopes(self) -> List[str]:
        return ["domains:read", "domains:write"]

    def build_auth_url(self, state: str) -> str:
        """Build the OAuth authorization URL"""
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": " ".join(self.get_scopes()),
            "state": state,
        }
        return f"{self.auth_url}?{urlencode(params)}"

    def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        # Namecheap uses a different OAuth flow
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
        }

        response = requests.post(self.token_url, data=data)

        if response.status_code == 200:
            # Parse XML response (simplified)
            return {
                "access_token": "namecheap_token",  # Placeholder
                "refresh_token": None,
                "expires_in": 3600,
                "token_type": "Bearer",
            }
        else:
            raise Exception(f"Token exchange failed: {response.text}")

    def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get user information from Namecheap"""
        # Namecheap API call to get user info
        return {"username": "namecheap_user", "email": "user@example.com"}

    def create_domain_provider(self, access_token: str) -> Any:
        """Create Namecheap domain provider with OAuth token"""
        from domain_providers import NamecheapProvider

        # For Namecheap, we might need to extract username from token
        return NamecheapProvider(access_token, self.client_secret)


class SquarespaceOAuth(OAuthProvider):
    """Squarespace OAuth integration"""

    def get_auth_url(self) -> str:
        return "https://api.squarespace.com/1.0/oauth2/authorize"

    def get_token_url(self) -> str:
        return "https://api.squarespace.com/1.0/oauth2/token"

    def get_scopes(self) -> List[str]:
        return ["sites:read", "sites:write", "domains:read", "domains:write"]

    def build_auth_url(self, state: str) -> str:
        """Build the OAuth authorization URL"""
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": " ".join(self.get_scopes()),
            "state": state,
        }
        return f"{self.auth_url}?{urlencode(params)}"

    def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
        }

        response = requests.post(self.token_url, data=data)

        if response.status_code == 200:
            token_data = response.json()
            return {
                "access_token": token_data.get("access_token"),
                "refresh_token": token_data.get("refresh_token"),
                "expires_in": token_data.get("expires_in"),
                "token_type": token_data.get("token_type", "Bearer"),
            }
        else:
            raise Exception(f"Token exchange failed: {response.text}")

    def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get user information from Squarespace"""
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(
            "https://api.squarespace.com/1.0/user/profile", headers=headers
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get user info: {response.text}")

    def create_domain_provider(self, access_token: str) -> Any:
        """Create Squarespace domain provider with OAuth token"""
        from domain_providers import SquarespaceProvider

        return SquarespaceProvider(access_token)


class DomainProviderOAuthManager:
    """Manager for OAuth authentication with domain providers"""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.oauth_providers = {}
        self.pending_oauth_states = {}

        # Initialize OAuth providers with environment variables
        self._initialize_providers()

    def _initialize_providers(self):
        """Initialize OAuth providers with credentials from environment"""

        # GoDaddy OAuth
        godaddy_client_id = os.getenv("GODADDY_OAUTH_CLIENT_ID")
        godaddy_client_secret = os.getenv("GODADDY_OAUTH_CLIENT_SECRET")
        if godaddy_client_id and godaddy_client_secret:
            self.oauth_providers["godaddy"] = GoDaddyOAuth(
                godaddy_client_id,
                godaddy_client_secret,
                f"{self.base_url}/api/domain-providers/oauth/callback/godaddy",
            )

        # Cloudflare OAuth
        cloudflare_client_id = os.getenv("CLOUDFLARE_OAUTH_CLIENT_ID")
        cloudflare_client_secret = os.getenv("CLOUDFLARE_OAUTH_CLIENT_SECRET")
        if cloudflare_client_id and cloudflare_client_secret:
            self.oauth_providers["cloudflare"] = CloudflareOAuth(
                cloudflare_client_id,
                cloudflare_client_secret,
                f"{self.base_url}/api/domain-providers/oauth/callback/cloudflare",
            )

        # Namecheap OAuth
        namecheap_client_id = os.getenv("NAMECHEAP_OAUTH_CLIENT_ID")
        namecheap_client_secret = os.getenv("NAMECHEAP_OAUTH_CLIENT_SECRET")
        if namecheap_client_id and namecheap_client_secret:
            self.oauth_providers["namecheap"] = NamecheapOAuth(
                namecheap_client_id,
                namecheap_client_secret,
                f"{self.base_url}/api/domain-providers/oauth/callback/namecheap",
            )

        # Squarespace OAuth
        squarespace_client_id = os.getenv("SQUARESPACE_OAUTH_CLIENT_ID")
        squarespace_client_secret = os.getenv("SQUARESPACE_OAUTH_CLIENT_SECRET")
        if squarespace_client_id and squarespace_client_secret:
            self.oauth_providers["squarespace"] = SquarespaceOAuth(
                squarespace_client_id,
                squarespace_client_secret,
                f"{self.base_url}/api/domain-providers/oauth/callback/squarespace",
            )

    def get_oauth_url(self, provider: str) -> Dict[str, str]:
        """Get OAuth URL for a provider"""
        if provider not in self.oauth_providers:
            raise Exception(f"OAuth not configured for {provider}")

        # Generate secure state
        state = secrets.token_urlsafe(32)

        # Store state for verification
        self.pending_oauth_states[state] = {
            "provider": provider,
            "timestamp": time.time(),
            "expires": time.time() + 600,  # 10 minutes
        }

        oauth_provider = self.oauth_providers[provider]
        auth_url = oauth_provider.build_auth_url(state)

        return {"auth_url": auth_url, "state": state}

    def handle_oauth_callback(
        self, provider: str, code: str, state: str
    ) -> Dict[str, Any]:
        """Handle OAuth callback and exchange code for token"""

        # Verify state
        if state not in self.pending_oauth_states:
            raise Exception("Invalid OAuth state")

        state_data = self.pending_oauth_states[state]
        if state_data["provider"] != provider:
            raise Exception("OAuth state mismatch")

        if time.time() > state_data["expires"]:
            del self.pending_oauth_states[state]
            raise Exception("OAuth state expired")

        # Clean up state
        del self.pending_oauth_states[state]

        # Exchange code for token
        oauth_provider = self.oauth_providers[provider]
        token_data = oauth_provider.exchange_code_for_token(code)

        # Get user info
        user_info = oauth_provider.get_user_info(token_data["access_token"])

        # Create domain provider instance
        domain_provider = oauth_provider.create_domain_provider(
            token_data["access_token"]
        )

        return {
            "provider": provider,
            "access_token": token_data["access_token"],
            "refresh_token": token_data.get("refresh_token"),
            "expires_in": token_data.get("expires_in"),
            "user_info": user_info,
            "domain_provider": domain_provider,
        }

    def get_supported_providers(self) -> List[Dict[str, Any]]:
        """Get list of supported OAuth providers"""
        providers = []

        for name, oauth_provider in self.oauth_providers.items():
            providers.append(
                {
                    "name": name,
                    "display_name": name.capitalize(),
                    "scopes": oauth_provider.get_scopes(),
                    "configured": True,
                }
            )

        return providers

    def is_provider_configured(self, provider: str) -> bool:
        """Check if OAuth is configured for a provider"""
        return provider in self.oauth_providers


# OAuth state management (in-memory for demo, use Redis in production)
PENDING_OAUTH_STATES = {}


def generate_oauth_state() -> str:
    """Generate a secure OAuth state"""
    return secrets.token_urlsafe(32)


def store_oauth_state(state: str, provider: str, user_agent: str = "", ip: str = ""):
    """Store OAuth state for verification"""
    PENDING_OAUTH_STATES[state] = {
        "provider": provider,
        "timestamp": time.time(),
        "user_agent": user_agent,
        "ip": ip,
        "expires": time.time() + 600,  # 10 minutes
    }


def verify_oauth_state(state: str) -> Optional[Dict[str, Any]]:
    """Verify and retrieve OAuth state"""
    if state not in PENDING_OAUTH_STATES:
        return None

    state_data = PENDING_OAUTH_STATES[state]

    # Check expiration
    if time.time() > state_data["expires"]:
        del PENDING_OAUTH_STATES[state]
        return None

    # Clean up state
    del PENDING_OAUTH_STATES[state]

    return state_data
