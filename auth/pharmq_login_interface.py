"""
PharmQAgentAI Login Interface
Professional login interface matching EmedChainHub design
"""

import streamlit as st
import os
from auth.external_db_connector import ExternalDBUserManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def render_login_page():
    """Render the main login interface"""
    
    # Custom CSS for professional styling
    st.markdown("""
    <style>
    .main-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    .brand-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .brand-logo {
        font-size: 3rem;
        font-weight: bold;
        color: #4F46E5;
        margin-bottom: 0.5rem;
    }
    
    .brand-subtitle {
        font-size: 1.2rem;
        color: #6B7280;
        margin-bottom: 3rem;
    }
    
    .login-card {
        background: white;
        border-radius: 16px;
        padding: 3rem 2.5rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        border: 1px solid #E5E7EB;
        margin-bottom: 2rem;
    }
    
    .login-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .login-title {
        font-size: 2rem;
        font-weight: bold;
        color: #111827;
        margin-bottom: 0.5rem;
    }
    
    .login-subtitle {
        color: #6B7280;
        font-size: 1rem;
    }
    
    .form-group {
        margin-bottom: 1.5rem;
    }
    
    .form-label {
        font-weight: 600;
        color: #374151;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .demo-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 2rem;
    }
    
    .demo-title {
        font-size: 1.25rem;
        font-weight: bold;
        color: #1E40AF;
        margin-bottom: 1rem;
    }
    
    .demo-subtitle {
        color: #1E40AF;
        margin-bottom: 1rem;
    }
    
    .demo-credentials {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3B82F6;
        font-family: monospace;
    }
    
    .error-message {
        background: #FEF2F2;
        border: 1px solid #FECACA;
        color: #DC2626;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .success-message {
        background: #F0FDF4;
        border: 1px solid #BBF7D0;
        color: #16A34A;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 1rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .signup-section {
        text-align: center;
        margin-top: 1.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid #E5E7EB;
    }
    
    .signup-text {
        color: #6B7280;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Brand header
    st.markdown('''
    <div class="brand-header">
        <div class="brand-logo">🧬 PharmQAgentAI</div>
        <div class="brand-subtitle">Sign in to your AI drug discovery platform</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Login card
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    
    # Login header
    st.markdown('''
    <div class="login-header">
        <div class="login-title">Welcome back</div>
        <div class="login-subtitle">Enter your credentials to access your account</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Check for authentication status
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'auth_error' not in st.session_state:
        st.session_state.auth_error = None
    
    # Show error message if any
    if st.session_state.auth_error:
        st.markdown(f'''
        <div class="error-message">
            {st.session_state.auth_error}
        </div>
        ''', unsafe_allow_html=True)
    
    # Login form
    with st.form("login_form"):
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        st.markdown('<label class="form-label">Email</label>', unsafe_allow_html=True)
        email = st.text_input("", placeholder="Enter your email", key="email_input", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        st.markdown('<label class="form-label">Password</label>', unsafe_allow_html=True)
        password = st.text_input("", placeholder="Enter your password", type="password", key="password_input", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
        submit_button = st.form_submit_button("Sign in")
        
        if submit_button:
            if email and password:
                # Authenticate user
                success, user_data, error_msg = authenticate_user(email, password)
                
                if success:
                    st.session_state.authenticated = True
                    st.session_state.user_data = user_data
                    st.session_state.auth_error = None
                    st.rerun()
                else:
                    st.session_state.auth_error = error_msg
                    st.rerun()
            else:
                st.session_state.auth_error = "Please enter both email and password"
                st.rerun()
    
    # Signup section
    st.markdown('''
    <div class="signup-section">
        <div class="signup-text">DON'T HAVE AN ACCOUNT?</div>
    </div>
    ''', unsafe_allow_html=True)
    
    if st.button("Create new account", key="signup_button"):
        st.session_state.show_signup = True
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close login card
    
    # Demo account section
    st.markdown('''
    <div class="demo-card">
        <div class="demo-title">Demo Account</div>
        <div class="demo-subtitle">Try the platform with these demo credentials:</div>
        <div class="demo-credentials">
            <strong>Email:</strong> admin@pharmqagent.ai<br>
            <strong>Password:</strong> admin123
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close main container

def render_signup_page():
    """Render the signup interface"""
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Brand header
    st.markdown('''
    <div class="brand-header">
        <div class="brand-logo">🧬 PharmQAgentAI</div>
        <div class="brand-subtitle">Create your AI drug discovery account</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Signup card
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="login-header">
        <div class="login-title">Create Account</div>
        <div class="login-subtitle">Join the future of pharmaceutical research</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Show error/success messages
    if st.session_state.get('signup_error'):
        st.markdown(f'''
        <div class="error-message">
            {st.session_state.signup_error}
        </div>
        ''', unsafe_allow_html=True)
    
    if st.session_state.get('signup_success'):
        st.markdown(f'''
        <div class="success-message">
            {st.session_state.signup_success}
        </div>
        ''', unsafe_allow_html=True)
    
    # Signup form
    with st.form("signup_form"):
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        st.markdown('<label class="form-label">Full Name</label>', unsafe_allow_html=True)
        full_name = st.text_input("", placeholder="Enter your full name", key="signup_name", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        st.markdown('<label class="form-label">Email</label>', unsafe_allow_html=True)
        email = st.text_input("", placeholder="Enter your email", key="signup_email", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        st.markdown('<label class="form-label">Organization (Optional)</label>', unsafe_allow_html=True)
        organization = st.text_input("", placeholder="Enter your organization", key="signup_org", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        st.markdown('<label class="form-label">Password</label>', unsafe_allow_html=True)
        password = st.text_input("", placeholder="Enter your password", type="password", key="signup_password", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        st.markdown('<label class="form-label">Confirm Password</label>', unsafe_allow_html=True)
        confirm_password = st.text_input("", placeholder="Confirm your password", type="password", key="signup_confirm", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
        signup_button = st.form_submit_button("Create Account")
        
        if signup_button:
            if full_name and email and password and confirm_password:
                if password == confirm_password:
                    # Register user
                    success, error_msg = register_user(email, password, full_name, organization)
                    
                    if success:
                        st.session_state.signup_success = "Account created successfully! You can now sign in."
                        st.session_state.signup_error = None
                        st.session_state.show_signup = False
                        st.rerun()
                    else:
                        st.session_state.signup_error = error_msg
                        st.session_state.signup_success = None
                        st.rerun()
                else:
                    st.session_state.signup_error = "Passwords do not match"
                    st.rerun()
            else:
                st.session_state.signup_error = "Please fill in all required fields"
                st.rerun()
    
    # Back to login
    if st.button("← Back to Sign In", key="back_to_login"):
        st.session_state.show_signup = False
        st.rerun()
    
    st.markdown('</div></div>', unsafe_allow_html=True)

def authenticate_user(email: str, password: str):
    """Authenticate user against Neon database"""
    try:
        # Initialize database manager
        db_manager = ExternalDBUserManager()
        
        # Attempt authentication
        user_data = db_manager.authenticate_user(email, password)
        
        if user_data:
            return True, user_data, None
        else:
            return False, None, "Invalid email or password. Please check your credentials and try again."
            
    except Exception as e:
        return False, None, f"Authentication service unavailable. Please try again later."

def register_user(email: str, password: str, full_name: str, organization: str = None):
    """Register new user in Neon database"""
    try:
        # Initialize database manager
        db_manager = ExternalDBUserManager()
        
        # Attempt registration
        success = db_manager.register_user(email, password, full_name, organization)
        
        if success:
            return True, None
        else:
            return False, "Email already exists or registration failed. Please try a different email."
            
    except Exception as e:
        return False, f"Registration service unavailable. Please try again later."

def main():
    """Main authentication flow"""
    
    # Initialize session state
    if 'show_signup' not in st.session_state:
        st.session_state.show_signup = False
    
    if 'signup_error' not in st.session_state:
        st.session_state.signup_error = None
    
    if 'signup_success' not in st.session_state:
        st.session_state.signup_success = None
    
    # Show appropriate page
    if st.session_state.get('show_signup', False):
        render_signup_page()
    else:
        render_login_page()

if __name__ == "__main__":
    main()