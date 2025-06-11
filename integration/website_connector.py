"""
Website Integration Module for PharmQAgentAI
Handles integration with existing websites for user management and authentication
"""

import requests
import json
import hashlib
import hmac
from typing import Dict, Optional, Any
from datetime import datetime, timedelta
import os

class WebsiteIntegrator:
    """Handles integration with external websites"""
    
    def __init__(self, api_endpoint: str = None, api_key: str = None):
        """Initialize website integrator"""
        self.api_endpoint = api_endpoint or os.getenv('WEBSITE_API_ENDPOINT')
        self.api_key = api_key or os.getenv('WEBSITE_API_KEY')
        self.session = requests.Session()
        
        if self.api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            })
    
    def verify_user_credentials(self, email: str, token: str) -> Optional[Dict]:
        """Verify user credentials with external website"""
        if not self.api_endpoint:
            return None
            
        try:
            response = self.session.post(
                f"{self.api_endpoint}/auth/verify",
                json={
                    'email': email,
                    'token': token,
                    'timestamp': datetime.now().isoformat()
                }
            )
            
            if response.status_code == 200:
                return response.json()
            return None
            
        except requests.RequestException:
            return None
    
    def sync_user_data(self, user_data: Dict) -> bool:
        """Sync user data with external website"""
        if not self.api_endpoint:
            return False
            
        try:
            response = self.session.post(
                f"{self.api_endpoint}/users/sync",
                json=user_data
            )
            return response.status_code == 200
            
        except requests.RequestException:
            return False
    
    def get_subscription_status(self, user_id: str) -> Optional[Dict]:
        """Get subscription status from external website"""
        if not self.api_endpoint:
            return None
            
        try:
            response = self.session.get(
                f"{self.api_endpoint}/subscriptions/{user_id}"
            )
            
            if response.status_code == 200:
                return response.json()
            return None
            
        except requests.RequestException:
            return None
    
    def create_sso_token(self, user_data: Dict) -> str:
        """Create Single Sign-On token for seamless integration"""
        payload = {
            'user_id': user_data.get('id'),
            'email': user_data.get('email'),
            'timestamp': datetime.now().isoformat(),
            'expires': (datetime.now() + timedelta(hours=24)).isoformat()
        }
        
        if self.api_key:
            signature = hmac.new(
                self.api_key.encode(),
                json.dumps(payload, sort_keys=True).encode(),
                hashlib.sha256
            ).hexdigest()
            payload['signature'] = signature
        
        return json.dumps(payload)
    
    def validate_sso_token(self, token: str) -> Optional[Dict]:
        """Validate Single Sign-On token"""
        try:
            payload = json.loads(token)
            
            # Check expiration
            expires = datetime.fromisoformat(payload.get('expires', ''))
            if datetime.now() > expires:
                return None
            
            # Validate signature if API key is available
            if self.api_key and 'signature' in payload:
                expected_signature = hmac.new(
                    self.api_key.encode(),
                    json.dumps({k: v for k, v in payload.items() if k != 'signature'}, sort_keys=True).encode(),
                    hashlib.sha256
                ).hexdigest()
                
                if not hmac.compare_digest(payload['signature'], expected_signature):
                    return None
            
            return payload
            
        except (json.JSONDecodeError, ValueError, KeyError):
            return None

def generate_integration_code(website_platform: str = 'generic') -> str:
    """Generate integration code for different website platforms"""
    
    if website_platform.lower() == 'wordpress':
        return '''
        // WordPress Integration Code
        add_action('user_register', 'sync_user_with_pharmq');
        
        function sync_user_with_pharmq($user_id) {
            $user = get_userdata($user_id);
            $data = array(
                'email' => $user->user_email,
                'full_name' => $user->display_name,
                'user_id' => $user_id,
                'event_type' => 'user.created'
            );
            
            wp_remote_post('YOUR_PHARMQ_WEBHOOK_URL', array(
                'body' => json_encode($data),
                'headers' => array('Content-Type' => 'application/json')
            ));
        }
        '''
    
    elif website_platform.lower() == 'django':
        return '''
        # Django Integration Code
        from django.contrib.auth.signals import user_logged_in
        from django.dispatch import receiver
        import requests
        
        @receiver(user_logged_in)
        def sync_user_login(sender, user, request, **kwargs):
            data = {
                'email': user.email,
                'full_name': user.get_full_name(),
                'user_id': user.id,
                'event_type': 'user.login'
            }
            
            requests.post(
                'YOUR_PHARMQ_WEBHOOK_URL',
                json=data,
                headers={'Authorization': 'Bearer YOUR_API_KEY'}
            )
        '''
    
    else:
        return '''
        // Generic JavaScript Integration
        function syncUserWithPharmQ(userData) {
            fetch('YOUR_PHARMQ_WEBHOOK_URL', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer YOUR_API_KEY'
                },
                body: JSON.stringify({
                    event_type: 'user.created',
                    user_data: userData
                })
            });
        }
        
        // Call this when user registers or updates profile
        syncUserWithPharmQ({
            email: 'user@example.com',
            full_name: 'User Name',
            organization: 'Company Name'
        });
        '''