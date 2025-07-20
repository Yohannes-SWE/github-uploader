from flask import Blueprint, request, jsonify, session
from universal_deployer import UniversalDeployer, DeploymentConfig, ServiceType, create_provider
import json
import logging

logger = logging.getLogger(__name__)

providers_bp = Blueprint('providers', __name__)

# Initialize universal deployer
deployer = UniversalDeployer()

@providers_bp.route('/providers/supported', methods=['GET'])
def get_supported_providers():
    """Get list of supported hosting providers"""
    try:
        providers = deployer.get_supported_providers()
        provider_info = {
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
        
        return jsonify({
            'success': True,
            'providers': providers,
            'provider_info': provider_info
        })
    except Exception as e:
        logger.error(f"Error getting supported providers: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@providers_bp.route('/providers/configured', methods=['GET'])
def get_configured_providers():
    """Get list of configured providers for the current user"""
    try:
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': 'Not authenticated'}), 401
        
        user_id = session['user_id']
        
        # In a real app, you'd store provider configs in a database
        # For now, we'll use session storage
        configured_providers = session.get('configured_providers', {})
        
        return jsonify({
            'success': True,
            'providers': list(configured_providers.keys()),
            'configurations': configured_providers
        })
    except Exception as e:
        logger.error(f"Error getting configured providers: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@providers_bp.route('/providers/<provider_name>/configure', methods=['POST'])
def configure_provider(provider_name):
    """Configure a hosting provider with API key"""
    try:
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': 'Not authenticated'}), 401
        
        data = request.get_json()
        api_key = data.get('api_key')
        config = data.get('config', {})
        
        if not api_key:
            return jsonify({'success': False, 'error': 'API key is required'}), 400
        
        # Validate provider
        if provider_name not in deployer.get_supported_providers():
            return jsonify({'success': False, 'error': f'Unsupported provider: {provider_name}'}), 400
        
        # Test the API key by creating a provider instance
        try:
            provider = create_provider(provider_name, api_key, config)
            
            # Test connection (if method exists)
            if hasattr(provider, 'test_connection'):
                if not provider.test_connection():
                    return jsonify({'success': False, 'error': 'Invalid API key or connection failed'}), 400
            
            # Store configuration in session (in production, use database)
            if 'configured_providers' not in session:
                session['configured_providers'] = {}
            
            session['configured_providers'][provider_name] = {
                'api_key': api_key,
                'config': config,
                'configured_at': str(datetime.utcnow())
            }
            
            # Add to deployer
            deployer.add_provider(provider_name, api_key, config)
            
            return jsonify({
                'success': True,
                'message': f'{provider_name} configured successfully',
                'provider': provider_name
            })
            
        except Exception as e:
            logger.error(f"Provider configuration failed: {e}")
            return jsonify({'success': False, 'error': f'Configuration failed: {str(e)}'}), 400
            
    except Exception as e:
        logger.error(f"Error configuring provider: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@providers_bp.route('/providers/<provider_name>/test', methods=['POST'])
def test_provider_connection(provider_name):
    """Test connection to a configured provider"""
    try:
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': 'Not authenticated'}), 401
        
        configured_providers = session.get('configured_providers', {})
        
        if provider_name not in configured_providers:
            return jsonify({'success': False, 'error': f'Provider {provider_name} not configured'}), 400
        
        # Test connection
        is_connected = deployer.test_provider_connection(provider_name)
        
        return jsonify({
            'success': True,
            'provider': provider_name,
            'connected': is_connected,
            'message': f'Connection {"successful" if is_connected else "failed"}'
        })
        
    except Exception as e:
        logger.error(f"Error testing provider connection: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@providers_bp.route('/providers/<provider_name>/remove', methods=['DELETE'])
def remove_provider(provider_name):
    """Remove a provider configuration"""
    try:
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': 'Not authenticated'}), 401
        
        configured_providers = session.get('configured_providers', {})
        
        if provider_name not in configured_providers:
            return jsonify({'success': False, 'error': f'Provider {provider_name} not configured'}), 400
        
        # Remove from session
        del configured_providers[provider_name]
        session['configured_providers'] = configured_providers
        
        # Remove from deployer
        deployer.remove_provider(provider_name)
        
        return jsonify({
            'success': True,
            'message': f'{provider_name} removed successfully',
            'provider': provider_name
        })
        
    except Exception as e:
        logger.error(f"Error removing provider: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@providers_bp.route('/deploy', methods=['POST'])
def deploy_application():
    """Deploy application to configured providers"""
    try:
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': 'Not authenticated'}), 401
        
        data = request.get_json()
        
        # Required fields
        repo_url = data.get('repo_url')
        project_name = data.get('project_name')
        providers = data.get('providers', [])  # List of providers to deploy to
        
        if not repo_url or not project_name:
            return jsonify({'success': False, 'error': 'repo_url and project_name are required'}), 400
        
        # Get configured providers
        configured_providers = session.get('configured_providers', {})
        
        if not configured_providers:
            return jsonify({'success': False, 'error': 'No providers configured'}), 400
        
        # If no specific providers specified, deploy to all
        if not providers:
            providers = list(configured_providers.keys())
        
        # Validate providers are configured
        for provider in providers:
            if provider not in configured_providers:
                return jsonify({'success': False, 'error': f'Provider {provider} not configured'}), 400
        
        # Create deployment configuration
        deployment_config = DeploymentConfig(
            name=project_name,
            service_type=ServiceType.WEB,
            environment=data.get('environment', 'node'),
            build_command=data.get('build_command'),
            start_command=data.get('start_command'),
            root_directory=data.get('root_directory'),
            static_publish_path=data.get('static_publish_path'),
            env_vars=data.get('env_vars', {}),
            auto_deploy=data.get('auto_deploy', True),
            branch=data.get('branch', 'main'),
            custom_domains=data.get('custom_domains', []),
            framework=data.get('framework')
        )
        
        # Deploy to specified providers
        results = {}
        for provider in providers:
            try:
                result = deployer.deploy_to_provider(provider, deployment_config, repo_url)
                results[provider] = {
                    'success': result.status.value == 'success',
                    'status': result.status.value,
                    'url': result.url,
                    'service_id': result.service_id,
                    'deployment_id': result.deployment_id,
                    'error': result.error
                }
            except Exception as e:
                logger.error(f"Deployment to {provider} failed: {e}")
                results[provider] = {
                    'success': False,
                    'status': 'failed',
                    'url': '',
                    'service_id': '',
                    'deployment_id': '',
                    'error': str(e)
                }
        
        # Store deployment history (in production, use database)
        deployment_history = session.get('deployment_history', [])
        deployment_history.append({
            'id': str(uuid.uuid4()),
            'project_name': project_name,
            'repo_url': repo_url,
            'providers': providers,
            'results': results,
            'timestamp': str(datetime.utcnow()),
            'user_id': session['user_id']
        })
        session['deployment_history'] = deployment_history[-10:]  # Keep last 10
        
        return jsonify({
            'success': True,
            'message': 'Deployment initiated',
            'results': results,
            'deployment_id': deployment_history[-1]['id']
        })
        
    except Exception as e:
        logger.error(f"Error deploying application: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@providers_bp.route('/deployments', methods=['GET'])
def get_deployment_history():
    """Get deployment history for the current user"""
    try:
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': 'Not authenticated'}), 401
        
        deployment_history = session.get('deployment_history', [])
        
        return jsonify({
            'success': True,
            'deployments': deployment_history
        })
        
    except Exception as e:
        logger.error(f"Error getting deployment history: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@providers_bp.route('/deployments/<deployment_id>/status', methods=['GET'])
def get_deployment_status(deployment_id):
    """Get status of a specific deployment"""
    try:
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': 'Not authenticated'}), 401
        
        deployment_history = session.get('deployment_history', [])
        deployment = next((d for d in deployment_history if d['id'] == deployment_id), None)
        
        if not deployment:
            return jsonify({'success': False, 'error': 'Deployment not found'}), 404
        
        # Get updated status from providers
        updated_results = {}
        for provider, result in deployment['results'].items():
            if result['service_id'] and result['deployment_id']:
                try:
                    status = deployer.get_deployment_status(provider, result['service_id'], result['deployment_id'])
                    updated_results[provider] = {
                        **result,
                        'status': status.value
                    }
                except Exception as e:
                    logger.error(f"Error getting status for {provider}: {e}")
                    updated_results[provider] = result
        
        return jsonify({
            'success': True,
            'deployment': {
                **deployment,
                'results': updated_results
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting deployment status: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@providers_bp.route('/providers/<provider_name>/domains', methods=['POST'])
def add_custom_domain(provider_name):
    """Add custom domain to a service"""
    try:
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': 'Not authenticated'}), 401
        
        data = request.get_json()
        service_id = data.get('service_id')
        domain = data.get('domain')
        
        if not service_id or not domain:
            return jsonify({'success': False, 'error': 'service_id and domain are required'}), 400
        
        # Check if provider is configured
        configured_providers = session.get('configured_providers', {})
        if provider_name not in configured_providers:
            return jsonify({'success': False, 'error': f'Provider {provider_name} not configured'}), 400
        
        # Add domain
        result = deployer.add_custom_domain(provider_name, service_id, domain)
        
        if 'error' in result:
            return jsonify({'success': False, 'error': result['error']}), 400
        
        return jsonify({
            'success': True,
            'message': f'Domain {domain} added successfully',
            'domain': result
        })
        
    except Exception as e:
        logger.error(f"Error adding custom domain: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# Import required modules
from datetime import datetime
import uuid 