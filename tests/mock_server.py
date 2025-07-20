#!/usr/bin/env python3
"""
Mock Server for User Flow Testing
=================================

This mock server simulates the RepoTorpedo application API endpoints
for testing purposes. It provides realistic responses without requiring
external dependencies or actual provider APIs.
"""

import json
import time
import uuid
import threading
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, session
from flask_cors import CORS
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'test-secret-key'
CORS(app)

# Mock data storage
users = {}
providers = {}
deployments = {}
sessions = {}

# Mock provider configurations
MOCK_PROVIDERS = {
    'render': {
        'name': 'Render',
        'description': 'Cloud application hosting platform',
        'features': ['Web Services', 'Static Sites', 'Background Workers', 'Cron Jobs'],
        'pricing': 'Free tier available',
        'docs_url': 'https://render.com/docs'
    },
    'vercel': {
        'name': 'Vercel',
        'description': 'Deploy frontend applications with zero configuration',
        'features': ['Static Sites', 'Serverless Functions', 'Edge Functions', 'Preview Deployments'],
        'pricing': 'Free tier available',
        'docs_url': 'https://vercel.com/docs'
    },
    'netlify': {
        'name': 'Netlify',
        'description': 'All-in-one platform for web projects',
        'features': ['Static Sites', 'Forms', 'Functions', 'Edge Functions'],
        'pricing': 'Free tier available',
        'docs_url': 'https://docs.netlify.com'
    },
    'railway': {
        'name': 'Railway',
        'description': 'Deploy anything with just one command',
        'features': ['Web Services', 'Databases', 'Cron Jobs', 'Background Workers'],
        'pricing': 'Free tier available',
        'docs_url': 'https://docs.railway.app'
    }
}

# Mock deployment statuses
DEPLOYMENT_STATUSES = ['pending', 'building', 'deploying', 'success', 'failed', 'cancelled']


def generate_mock_url(provider: str, project_name: str) -> str:
    """Generate mock deployment URLs"""
    urls = {
        'render': f'https://{project_name}.onrender.com',
        'vercel': f'https://{project_name}.vercel.app',
        'netlify': f'https://{project_name}.netlify.app',
        'railway': f'https://{project_name}.railway.app'
    }
    return urls.get(provider, f'https://{project_name}.example.com')


def require_auth(f):
    """Decorator to require authentication"""
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': 'Not authenticated'}), 401
        return f(*args, **kwargs)
    return decorated_function


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })


# Authentication endpoints
@app.route('/auth/register', methods=['POST'])
def register():
    """Mock user registration"""
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'Invalid JSON'}), 400
    
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    
    if not email or not password:
        return jsonify({'success': False, 'error': 'Email and password are required'}), 400
    
    if password != confirm_password:
        return jsonify({'success': False, 'error': 'Passwords do not match'}), 400
    
    if email in users:
        return jsonify({'success': False, 'error': 'User already exists'}), 400
    
    # Create user
    user_id = str(uuid.uuid4())
    users[email] = {
        'id': user_id,
        'email': email,
        'password': password,  # In real app, this would be hashed
        'created_at': datetime.now().isoformat(),
        'configured_providers': {},
        'deployment_history': []
    }
    
    # Create session
    session['user_id'] = user_id
    session['email'] = email
    
    return jsonify({
        'success': True,
        'message': 'User registered successfully',
        'user': {
            'id': user_id,
            'email': email
        }
    })


@app.route('/auth/login', methods=['POST'])
def login():
    """Mock user login"""
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'Invalid JSON'}), 400
    
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'success': False, 'error': 'Email and password are required'}), 400
    
    if email not in users:
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    
    user = users[email]
    if user['password'] != password:
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    
    # Create session
    session['user_id'] = user['id']
    session['email'] = email
    
    return jsonify({
        'success': True,
        'message': 'Login successful',
        'user': {
            'id': user['id'],
            'email': email
        }
    })


@app.route('/auth/logout', methods=['POST'])
def logout():
    """Mock user logout"""
    session.clear()
    return jsonify({
        'success': True,
        'message': 'Logout successful'
    })


@app.route('/auth/me', methods=['GET'])
@require_auth
def get_current_user():
    """Get current user information"""
    user_id = session['user_id']
    email = session['email']
    
    if email not in users:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    
    user = users[email]
    return jsonify({
        'success': True,
        'user': {
            'id': user['id'],
            'email': user['email'],
            'created_at': user['created_at']
        }
    })


# Provider endpoints
@app.route('/providers/supported', methods=['GET'])
def get_supported_providers():
    """Get list of supported providers"""
    return jsonify({
        'success': True,
        'providers': list(MOCK_PROVIDERS.keys()),
        'provider_info': MOCK_PROVIDERS
    })


@app.route('/providers/configured', methods=['GET'])
@require_auth
def get_configured_providers():
    """Get configured providers for current user"""
    email = session['email']
    user = users[email]
    
    return jsonify({
        'success': True,
        'providers': list(user['configured_providers'].keys()),
        'configurations': user['configured_providers']
    })


@app.route('/providers/<provider_name>/configure', methods=['POST'])
@require_auth
def configure_provider(provider_name):
    """Configure a hosting provider"""
    if provider_name not in MOCK_PROVIDERS:
        return jsonify({'success': False, 'error': f'Unsupported provider: {provider_name}'}), 400
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Invalid JSON'}), 400
    
    api_key = data.get('api_key')
    config = data.get('config', {})
    
    if not api_key:
        return jsonify({'success': False, 'error': 'API key is required'}), 400
    
    # Mock API key validation
    if api_key.startswith('invalid_'):
        return jsonify({'success': False, 'error': 'Invalid API key'}), 400
    
    email = session['email']
    user = users[email]
    
    # Store provider configuration
    user['configured_providers'][provider_name] = {
        'api_key': api_key,
        'config': config,
        'configured_at': datetime.now().isoformat()
    }
    
    return jsonify({
        'success': True,
        'message': f'{provider_name} configured successfully',
        'provider': provider_name
    })


@app.route('/providers/<provider_name>/test', methods=['POST'])
@require_auth
def test_provider_connection(provider_name):
    """Test provider connection"""
    email = session['email']
    user = users[email]
    
    if provider_name not in user['configured_providers']:
        return jsonify({'success': False, 'error': f'Provider {provider_name} not configured'}), 400
    
    # Mock connection test
    connected = True  # In real app, this would test the actual API
    
    return jsonify({
        'success': True,
        'provider': provider_name,
        'connected': connected,
        'message': f'Connection {"successful" if connected else "failed"}'
    })


@app.route('/providers/<provider_name>/remove', methods=['DELETE'])
@require_auth
def remove_provider(provider_name):
    """Remove provider configuration"""
    email = session['email']
    user = users[email]
    
    if provider_name not in user['configured_providers']:
        return jsonify({'success': False, 'error': f'Provider {provider_name} not configured'}), 400
    
    del user['configured_providers'][provider_name]
    
    return jsonify({
        'success': True,
        'message': f'{provider_name} removed successfully',
        'provider': provider_name
    })


# Deployment endpoints
@app.route('/deploy', methods=['POST'])
@require_auth
def deploy_application():
    """Deploy application to configured providers"""
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Invalid JSON'}), 400
    
    repo_url = data.get('repo_url')
    project_name = data.get('project_name')
    providers_list = data.get('providers', [])
    
    if not repo_url or not project_name:
        return jsonify({'success': False, 'error': 'repo_url and project_name are required'}), 400
    
    email = session['email']
    user = users[email]
    
    if not user['configured_providers']:
        return jsonify({'success': False, 'error': 'No providers configured'}), 400
    
    # If no specific providers specified, deploy to all
    if not providers_list:
        providers_list = list(user['configured_providers'].keys())
    
    # Validate providers are configured
    for provider in providers_list:
        if provider not in user['configured_providers']:
            return jsonify({'success': False, 'error': f'Provider {provider} not configured'}), 400
    
    # Create deployment
    deployment_id = str(uuid.uuid4())
    deployment = {
        'id': deployment_id,
        'project_name': project_name,
        'repo_url': repo_url,
        'providers': providers_list,
        'results': {},
        'timestamp': datetime.now().isoformat(),
        'user_id': user['id']
    }
    
    # Simulate deployment to each provider
    for provider in providers_list:
        service_id = f"{provider}_{project_name}_{uuid.uuid4().hex[:8]}"
        deployment_id_provider = f"{provider}_{uuid.uuid4().hex[:8]}"
        
        deployment['results'][provider] = {
            'success': True,
            'status': 'success',
            'url': generate_mock_url(provider, project_name),
            'service_id': service_id,
            'deployment_id': deployment_id_provider,
            'error': None
        }
    
    # Store deployment
    deployments[deployment_id] = deployment
    user['deployment_history'].append(deployment)
    
    # Keep only last 10 deployments
    user['deployment_history'] = user['deployment_history'][-10:]
    
    return jsonify({
        'success': True,
        'message': 'Deployment initiated',
        'results': deployment['results'],
        'deployment_id': deployment_id
    })


@app.route('/deployments', methods=['GET'])
@require_auth
def get_deployment_history():
    """Get deployment history for current user"""
    email = session['email']
    user = users[email]
    
    return jsonify({
        'success': True,
        'deployments': user['deployment_history']
    })


@app.route('/deployments/<deployment_id>/status', methods=['GET'])
@require_auth
def get_deployment_status(deployment_id):
    """Get status of specific deployment"""
    if deployment_id not in deployments:
        return jsonify({'success': False, 'error': 'Deployment not found'}), 404
    
    deployment = deployments[deployment_id]
    
    # Update status (simulate real-time updates)
    for provider, result in deployment['results'].items():
        if result['status'] == 'success':
            # Keep successful deployments as is
            pass
        elif result['status'] == 'pending':
            # Simulate status progression
            if time.time() % 10 < 5:  # Random status change
                result['status'] = 'building'
        elif result['status'] == 'building':
            if time.time() % 10 < 5:
                result['status'] = 'deploying'
        elif result['status'] == 'deploying':
            if time.time() % 10 < 5:
                result['status'] = 'success'
    
    return jsonify({
        'success': True,
        'deployment': deployment
    })


@app.route('/providers/<provider_name>/domains', methods=['POST'])
@require_auth
def add_custom_domain(provider_name):
    """Add custom domain to a service"""
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Invalid JSON'}), 400
    
    service_id = data.get('service_id')
    domain = data.get('domain')
    
    if not service_id or not domain:
        return jsonify({'success': False, 'error': 'service_id and domain are required'}), 400
    
    email = session['email']
    user = users[email]
    
    if provider_name not in user['configured_providers']:
        return jsonify({'success': False, 'error': f'Provider {provider_name} not configured'}), 400
    
    # Mock domain addition
    domain_result = {
        'id': str(uuid.uuid4()),
        'domain': domain,
        'provider': provider_name,
        'service_id': service_id,
        'status': 'pending',
        'created_at': datetime.now().isoformat()
    }
    
    return jsonify({
        'success': True,
        'message': f'Domain {domain} added successfully',
        'domain': domain_result
    })


# Error simulation endpoints
@app.route('/simulate/error/<error_type>', methods=['POST'])
def simulate_error(error_type):
    """Simulate various error conditions for testing"""
    error_responses = {
        'timeout': ({'success': False, 'error': 'Request timeout'}, 500),
        'rate_limit': ({'success': False, 'error': 'Rate limit exceeded'}, 429),
        'invalid_json': ({'success': False, 'error': 'Invalid JSON'}, 400),
        'unauthorized': ({'success': False, 'error': 'Unauthorized'}, 401),
        'not_found': ({'success': False, 'error': 'Resource not found'}, 404),
        'server_error': ({'success': False, 'error': 'Internal server error'}, 500)
    }
    
    if error_type in error_responses:
        response, status_code = error_responses[error_type]
        return jsonify(response), status_code
    
    return jsonify({'success': False, 'error': 'Unknown error type'}), 400


# Health and monitoring endpoints
@app.route('/metrics', methods=['GET'])
def get_metrics():
    """Get application metrics"""
    return jsonify({
        'success': True,
        'metrics': {
            'total_users': len(users),
            'total_deployments': len(deployments),
            'active_sessions': len(sessions),
            'uptime': time.time(),
            'memory_usage': '128MB',
            'cpu_usage': '15%'
        }
    })


@app.route('/status', methods=['GET'])
def get_status():
    """Get application status"""
    return jsonify({
        'success': True,
        'status': 'operational',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'database': 'healthy',
            'cache': 'healthy',
            'external_apis': 'healthy'
        }
    })


def start_mock_server(host='localhost', port=5000, debug=False):
    """Start the mock server"""
    logger.info(f"Starting mock server on {host}:{port}")
    app.run(host=host, port=port, debug=debug, use_reloader=False)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Start Mock Server for Testing')
    parser.add_argument('--host', default='localhost', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    start_mock_server(host=args.host, port=args.port, debug=args.debug) 