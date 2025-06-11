"""
API Endpoints for Website Integration
Provides REST API endpoints for external website integration
"""

from flask import Flask, request, jsonify
import json
from datetime import datetime
from auth.user_management import UserManager
from integration.website_connector import WebsiteIntegrator
import os

app = Flask(__name__)
user_manager = UserManager()
integrator = WebsiteIntegrator()

@app.route('/api/auth/verify', methods=['POST'])
def verify_auth():
    """Verify user authentication from external website"""
    try:
        data = request.get_json()
        email = data.get('email')
        token = data.get('token')
        
        if not email or not token:
            return jsonify({'error': 'Missing email or token'}), 400
        
        # Validate token with external system
        user_data = integrator.verify_user_credentials(email, token)
        
        if user_data:
            return jsonify({
                'status': 'success',
                'user_data': user_data,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/sync', methods=['POST'])
def sync_user():
    """Sync user data from external website"""
    try:
        data = request.get_json()
        
        # Extract user information
        email = data.get('email')
        full_name = data.get('full_name')
        organization = data.get('organization')
        plan_type = data.get('plan_type', 'Starter')
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        # Check if user exists
        existing_user = user_manager.authenticate_user(email, '')
        
        if existing_user:
            # Update existing user
            success = integrator.sync_user_data(data)
        else:
            # Create new user
            temp_password = f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            success = user_manager.register_user(
                email=email,
                password=temp_password,
                full_name=full_name,
                organization=organization
            )
            
            if success:
                # Get user ID and create subscription
                user = user_manager.authenticate_user(email, temp_password)
                if user:
                    user_manager.create_subscription(
                        user_id=user['id'],
                        plan_type=plan_type
                    )
        
        if success:
            return jsonify({
                'status': 'success',
                'message': 'User synchronized successfully'
            })
        else:
            return jsonify({'error': 'Failed to sync user'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/subscriptions/<user_id>', methods=['GET'])
def get_subscription(user_id):
    """Get subscription status for user"""
    try:
        subscription = user_manager.get_user_subscription(int(user_id))
        
        if subscription:
            return jsonify({
                'status': 'success',
                'subscription': subscription
            })
        else:
            return jsonify({'error': 'No subscription found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/sso', methods=['POST'])
def sso_login():
    """Handle Single Sign-On login"""
    try:
        data = request.get_json()
        token = data.get('token')
        
        if not token:
            return jsonify({'error': 'Token is required'}), 400
        
        # Validate SSO token
        user_data = integrator.validate_sso_token(token)
        
        if user_data:
            return jsonify({
                'status': 'success',
                'redirect_url': '/app',
                'user_data': user_data
            })
        else:
            return jsonify({'error': 'Invalid or expired token'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/webhooks/user_updates', methods=['POST'])
def webhook_handler():
    """Handle webhooks from external website"""
    try:
        # Verify webhook signature if configured
        signature = request.headers.get('X-Signature')
        payload = request.get_data(as_text=True)
        
        from integration.website_connector import WebhookHandler
        webhook_handler = WebhookHandler()
        
        if signature and not webhook_handler.verify_webhook_signature(payload, signature):
            return jsonify({'error': 'Invalid signature'}), 401
        
        data = request.get_json()
        success = webhook_handler.process_user_update(data)
        
        if success:
            return jsonify({'status': 'success'})
        else:
            return jsonify({'error': 'Failed to process webhook'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/integration/config', methods=['GET'])
def get_integration_config():
    """Get integration configuration for external websites"""
    from integration.website_connector import create_integration_endpoints
    
    config = create_integration_endpoints()
    config['base_url'] = request.host_url.rstrip('/')
    
    return jsonify(config)

@app.route('/api/integration/code/<platform>', methods=['GET'])
def get_integration_code(platform):
    """Get integration code for specific platform"""
    from integration.website_connector import generate_integration_code
    
    code = generate_integration_code(platform)
    
    return jsonify({
        'platform': platform,
        'integration_code': code,
        'instructions': f'Integration code for {platform} platform'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)