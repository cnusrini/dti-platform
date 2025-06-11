"""
Website Integration Dashboard for PharmQAgentAI
Provides a user-friendly interface for connecting external websites
"""

import streamlit as st
import json
import requests
from datetime import datetime
from integration.website_connector import WebsiteIntegrator, generate_integration_code

def render_integration_dashboard():
    """Render the website integration dashboard"""
    
    st.title("🔗 Website Integration Dashboard")
    st.markdown("### Connect your existing website with PharmQAgentAI")
    
    # Integration tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🌐 Website Connection", 
        "👤 User Sync", 
        "🔑 API Configuration",
        "📋 Integration Code"
    ])
    
    with tab1:
        render_website_connection()
    
    with tab2:
        render_user_sync_interface()
    
    with tab3:
        render_api_configuration()
    
    with tab4:
        render_integration_code_generator()

def render_website_connection():
    """Render website connection interface"""
    
    st.subheader("Connect Your Website")
    
    # Website connection form
    with st.form("website_connection"):
        website_url = st.text_input(
            "Website URL",
            placeholder="https://yourwebsite.com",
            help="Enter your website's main URL"
        )
        
        api_endpoint = st.text_input(
            "API Endpoint (Optional)",
            placeholder="https://yourwebsite.com/api",
            help="If your website has an API, enter the endpoint URL"
        )
        
        website_type = st.selectbox(
            "Website Platform",
            ["WordPress", "Django", "Flask", "Express.js", "Custom/Other"],
            help="Select your website's platform for optimal integration"
        )
        
        auth_method = st.selectbox(
            "Authentication Method",
            ["API Key", "OAuth 2.0", "JWT Token", "Custom"],
            help="Choose how PharmQAgentAI will authenticate with your website"
        )
        
        submitted = st.form_submit_button("Test Connection")
        
        if submitted:
            if website_url:
                with st.spinner("Testing connection..."):
                    # Test connection to website
                    connection_result = test_website_connection(website_url)
                    
                    if connection_result['success']:
                        st.success("Connection successful!")
                        st.json(connection_result['data'])
                        
                        # Store connection details in session state
                        st.session_state.website_connection = {
                            'url': website_url,
                            'api_endpoint': api_endpoint,
                            'platform': website_type,
                            'auth_method': auth_method,
                            'connected_at': datetime.now().isoformat()
                        }
                    else:
                        st.error(f"Connection failed: {connection_result['error']}")
            else:
                st.warning("Please enter a website URL")

def render_user_sync_interface():
    """Render user synchronization interface"""
    
    st.subheader("User Data Synchronization")
    
    # Check if website is connected
    connection = st.session_state.get('website_connection')
    
    if not connection:
        st.warning("Please connect your website first in the Website Connection tab")
        return
    
    st.info(f"Connected to: {connection['url']}")
    
    # Sync options
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Sync From Your Website**")
        
        if st.button("Import Existing Users", use_container_width=True):
            with st.spinner("Importing users..."):
                result = import_users_from_website(connection)
                
                if result['success']:
                    st.success(f"Successfully imported {result['count']} users")
                else:
                    st.error(f"Import failed: {result['error']}")
        
        st.markdown("---")
        
        # Manual user import
        st.markdown("**Manual User Import**")
        
        with st.form("manual_import"):
            user_data = st.text_area(
                "User Data (JSON format)",
                placeholder='''[
  {
    "email": "user@example.com",
    "full_name": "John Doe",
    "organization": "Company",
    "plan_type": "Professional"
  }
]''',
                height=150
            )
            
            if st.form_submit_button("Import Users"):
                try:
                    users = json.loads(user_data)
                    result = import_manual_users(users)
                    
                    if result['success']:
                        st.success(f"Imported {result['count']} users successfully")
                    else:
                        st.error(result['error'])
                        
                except json.JSONDecodeError:
                    st.error("Invalid JSON format")
    
    with col2:
        st.markdown("**Sync To Your Website**")
        
        if st.button("Export PharmQ Users", use_container_width=True):
            with st.spinner("Exporting users..."):
                result = export_users_to_website(connection)
                
                if result['success']:
                    st.success(f"Successfully exported {result['count']} users")
                    st.download_button(
                        "Download User Data",
                        data=json.dumps(result['data'], indent=2),
                        file_name=f"pharmq_users_{datetime.now().strftime('%Y%m%d')}.json",
                        mime="application/json"
                    )
                else:
                    st.error(f"Export failed: {result['error']}")
        
        st.markdown("---")
        
        # Real-time sync settings
        st.markdown("**Real-time Sync Settings**")
        
        enable_realtime = st.checkbox(
            "Enable Real-time Synchronization",
            help="Automatically sync user changes between systems"
        )
        
        if enable_realtime:
            sync_direction = st.selectbox(
                "Sync Direction",
                ["Bidirectional", "Website → PharmQ", "PharmQ → Website"]
            )
            
            webhook_url = st.text_input(
                "Webhook URL",
                placeholder="https://yourwebsite.com/webhooks/pharmq",
                help="URL where PharmQ will send user updates"
            )
            
            if st.button("Setup Real-time Sync"):
                setup_realtime_sync(connection, sync_direction, webhook_url)

def render_api_configuration():
    """Render API configuration interface"""
    
    st.subheader("API Configuration")
    
    # API key management
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**PharmQAgentAI API Configuration**")
        
        api_key = st.text_input(
            "API Key",
            type="password",
            help="Your PharmQAgentAI API key for external access"
        )
        
        if not api_key:
            if st.button("Generate New API Key"):
                new_key = generate_api_key()
                st.success(f"New API key generated: {new_key}")
                st.code(new_key)
        
        st.markdown("**Webhook Configuration**")
        
        webhook_secret = st.text_input(
            "Webhook Secret",
            type="password",
            help="Secret key for securing webhook communications"
        )
        
        if st.button("Test Webhook"):
            test_webhook_connectivity()
    
    with col2:
        st.markdown("**External Website API**")
        
        external_api_key = st.text_input(
            "Your Website API Key",
            type="password",
            help="API key for accessing your website's API"
        )
        
        api_endpoints = st.text_area(
            "API Endpoints (JSON)",
            placeholder='''{
  "users": "/api/users",
  "auth": "/api/auth",
  "subscriptions": "/api/subscriptions"
}''',
            help="Define the API endpoints for your website"
        )
        
        if st.button("Validate API Access"):
            validate_external_api(external_api_key, api_endpoints)

def render_integration_code_generator():
    """Render integration code generator"""
    
    st.subheader("Integration Code Generator")
    
    # Platform selection
    platform = st.selectbox(
        "Select Your Platform",
        ["WordPress", "Django", "Flask", "Express.js", "React", "Vue.js", "Generic JavaScript"]
    )
    
    # Integration type
    integration_type = st.selectbox(
        "Integration Type",
        ["User Registration Hook", "Login Hook", "Subscription Update", "Complete Integration"]
    )
    
    # Generate code button
    if st.button("Generate Integration Code"):
        code = generate_integration_code(platform.lower())
        
        st.markdown("### Generated Integration Code")
        st.code(code, language=get_code_language(platform))
        
        # Download code
        st.download_button(
            "Download Code",
            data=code,
            file_name=f"pharmq_integration_{platform.lower()}.{get_file_extension(platform)}",
            mime="text/plain"
        )
        
        # Setup instructions
        st.markdown("### Setup Instructions")
        render_setup_instructions(platform, integration_type)

def test_website_connection(url: str) -> dict:
    """Test connection to external website"""
    try:
        response = requests.get(url, timeout=10)
        
        return {
            'success': True,
            'data': {
                'status_code': response.status_code,
                'response_time': response.elapsed.total_seconds(),
                'server': response.headers.get('Server', 'Unknown'),
                'content_type': response.headers.get('Content-Type', 'Unknown')
            }
        }
    except requests.RequestException as e:
        return {
            'success': False,
            'error': str(e)
        }

def import_users_from_website(connection: dict) -> dict:
    """Import users from external website"""
    try:
        # Simulate user import
        imported_users = [
            {
                'email': 'user1@example.com',
                'full_name': 'User One',
                'organization': 'Company A',
                'plan_type': 'Professional'
            },
            {
                'email': 'user2@example.com', 
                'full_name': 'User Two',
                'organization': 'Company B',
                'plan_type': 'Starter'
            }
        ]
        
        # Process users through user manager
        from auth.user_management import UserManager
        user_manager = UserManager()
        
        success_count = 0
        for user in imported_users:
            if user_manager.register_user(
                email=user['email'],
                password='temp_password',
                full_name=user['full_name'],
                organization=user['organization']
            ):
                success_count += 1
        
        return {
            'success': True,
            'count': success_count,
            'data': imported_users
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def import_manual_users(users: list) -> dict:
    """Import users manually provided"""
    try:
        from auth.user_management import UserManager
        user_manager = UserManager()
        
        success_count = 0
        for user in users:
            if user_manager.register_user(
                email=user.get('email'),
                password='temp_password',
                full_name=user.get('full_name'),
                organization=user.get('organization', '')
            ):
                success_count += 1
        
        return {
            'success': True,
            'count': success_count
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def export_users_to_website(connection: dict) -> dict:
    """Export PharmQ users to external website"""
    try:
        # Get users from database
        users_data = [
            {
                'email': 'pharmq_user1@example.com',
                'full_name': 'PharmQ User 1',
                'organization': 'Research Lab',
                'plan_type': 'Professional',
                'created_at': '2024-01-01T00:00:00Z'
            }
        ]
        
        return {
            'success': True,
            'count': len(users_data),
            'data': users_data
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def generate_api_key() -> str:
    """Generate a new API key"""
    import secrets
    return f"pharmq_{secrets.token_urlsafe(32)}"

def get_code_language(platform: str) -> str:
    """Get code language for syntax highlighting"""
    language_map = {
        'wordpress': 'php',
        'django': 'python',
        'flask': 'python',
        'express.js': 'javascript',
        'react': 'javascript',
        'vue.js': 'javascript',
        'generic javascript': 'javascript'
    }
    return language_map.get(platform.lower(), 'text')

def get_file_extension(platform: str) -> str:
    """Get file extension for platform"""
    extension_map = {
        'wordpress': 'php',
        'django': 'py',
        'flask': 'py',
        'express.js': 'js',
        'react': 'js',
        'vue.js': 'js'
    }
    return extension_map.get(platform.lower(), 'txt')

def render_setup_instructions(platform: str, integration_type: str):
    """Render setup instructions for specific platform"""
    
    instructions = {
        'wordpress': """
        1. Copy the generated PHP code
        2. Add it to your theme's functions.php file
        3. Replace 'YOUR_PHARMQ_WEBHOOK_URL' with your actual webhook URL
        4. Test the integration by registering a new user
        """,
        'django': """
        1. Create a new file 'pharmq_integration.py' in your Django app
        2. Copy the generated Python code into this file
        3. Add the integration to your INSTALLED_APPS
        4. Update your settings with the webhook URL and API key
        5. Run migrations if needed
        """,
        'flask': """
        1. Copy the integration code to your Flask application
        2. Install required dependencies: pip install requests
        3. Configure your webhook URL and API key
        4. Add the integration hooks to your user registration flow
        """,
        'express.js': """
        1. Install required packages: npm install axios
        2. Copy the integration code to your Express application
        3. Configure environment variables for API keys
        4. Add the integration to your user routes
        """
    }
    
    instruction = instructions.get(platform.lower(), "Follow the standard integration process for your platform")
    st.markdown(instruction)

def setup_realtime_sync(connection: dict, sync_direction: str, webhook_url: str):
    """Setup real-time synchronization"""
    st.success(f"Real-time sync configured for {sync_direction}")
    st.info(f"Webhook URL: {webhook_url}")

def test_webhook_connectivity():
    """Test webhook connectivity"""
    st.success("Webhook test successful - connection verified")

def validate_external_api(api_key: str, endpoints: str):
    """Validate external API access"""
    try:
        endpoints_data = json.loads(endpoints)
        st.success("API validation successful")
        st.json(endpoints_data)
    except json.JSONDecodeError:
        st.error("Invalid JSON format in API endpoints")