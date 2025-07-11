import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """Test that the health check endpoint works"""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert "status" in response.json()

def test_github_login_redirect():
    """Test that GitHub login redirects properly"""
    response = client.get("/auth/github/login", allow_redirects=False)
    assert response.status_code == 307  # Redirect
    assert "github.com" in response.headers["location"]

def test_analyze_endpoint_requires_file():
    """Test that analyze endpoint requires a file"""
    response = client.post("/analyze")
    assert response.status_code == 422  # Validation error

def test_upload_endpoint_requires_auth():
    """Test that upload endpoint requires authentication"""
    response = client.post("/upload")
    assert response.status_code == 401  # Unauthorized

def test_cors_headers():
    """Test that CORS headers are set"""
    response = client.options("/api/health")
    assert "access-control-allow-origin" in response.headers 