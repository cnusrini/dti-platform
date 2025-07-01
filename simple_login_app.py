"""
Simple PharmQAgentAI Login Application
Minimal version for quick loading
"""

import streamlit as st
import os
import psycopg2
import hashlib
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="PharmQAgentAI Login",
    page_icon="🧬",
    layout="centered"
)

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(email: str, password: str):
    """Simple authentication against Neon database"""
    try:
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            return False, None, "Database not configured"
        
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        cursor.execute("""
            SELECT id, email, full_name, organization
            FROM pharmq_users 
            WHERE email = %s AND password_hash = %s AND is_active = TRUE
        """, (email, password_hash))
        
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            return True, {
                'id': user[0],
                'email': user[1], 
                'full_name': user[2],
                'organization': user[3]
            }, None
        else:
            return False, None, "Invalid email or password"
            
    except Exception as e:
        return False, None, f"Authentication error: {str(e)}"

def register_user(email: str, password: str, full_name: str, organization: str = None):
    """Simple user registration"""
    try:
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            return False, "Database not configured"
        
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT id FROM pharmq_users WHERE email = %s", (email,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return False, "Email already exists"
        
        # Create user
        password_hash = hash_password(password)
        cursor.execute("""
            INSERT INTO pharmq_users (email, password_hash, full_name, organization)
            VALUES (%s, %s, %s, %s)
        """, (email, password_hash, full_name, organization))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True, None
        
    except Exception as e:
        return False, f"Registration error: {str(e)}"

def render_login_interface():
    """Render the login interface"""
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .brand-title {
        font-size: 2.5rem;
        color: #4F46E5;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .brand-subtitle {
        color: #6B7280;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .login-container {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    .demo-box {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem;
        margin-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <div class="brand-title">🧬 PharmQAgentAI</div>
        <div class="brand-subtitle">Sign in to your AI drug discovery platform</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Check authentication
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        # Login form
        st.markdown("### Welcome back")
        st.markdown("Enter your credentials to access your account")
        
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col1, col2 = st.columns(2)
            with col1:
                login_btn = st.form_submit_button("Sign in", type="primary", use_container_width=True)
            with col2:
                signup_btn = st.form_submit_button("Create Account", use_container_width=True)
            
            if login_btn:
                if email and password:
                    success, user_data, error = authenticate_user(email, password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.user_data = user_data
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error(error)
                else:
                    st.error("Please enter both email and password")
            
            if signup_btn:
                st.session_state.show_signup = True
                st.rerun()
        
        # Demo credentials
        st.markdown("""
        <div class="demo-box">
            <strong>Demo Account</strong><br>
            Email: admin@pharmqagent.ai<br>
            Password: admin123
        </div>
        """, unsafe_allow_html=True)
        
        # Database status
        database_url = os.getenv('DATABASE_URL')
        if database_url:
            st.success("Connected to Neon PostgreSQL Database")
        else:
            st.warning("Database not configured")
    
    else:
        # Authenticated view
        render_authenticated_app()

def render_signup_form():
    """Render signup form"""
    st.markdown("### Create Account")
    
    with st.form("signup_form"):
        full_name = st.text_input("Full Name", placeholder="Enter your full name")
        email = st.text_input("Email", placeholder="Enter your email")
        organization = st.text_input("Organization (Optional)", placeholder="Enter your organization")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
        
        col1, col2 = st.columns(2)
        with col1:
            create_btn = st.form_submit_button("Create Account", type="primary", use_container_width=True)
        with col2:
            back_btn = st.form_submit_button("Back to Login", use_container_width=True)
        
        if create_btn:
            if full_name and email and password and confirm_password:
                if password == confirm_password:
                    success, error = register_user(email, password, full_name, organization)
                    if success:
                        st.success("Account created successfully! Please sign in.")
                        st.session_state.show_signup = False
                        st.rerun()
                    else:
                        st.error(error)
                else:
                    st.error("Passwords do not match")
            else:
                st.error("Please fill in all required fields")
        
        if back_btn:
            st.session_state.show_signup = False
            st.rerun()

def render_authenticated_app():
    """Render authenticated application"""
    user_data = st.session_state.user_data
    
    st.success(f"Welcome, {user_data['full_name']}!")
    
    # User info
    st.markdown("### User Information")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Name:** {user_data['full_name']}")
        st.write(f"**Email:** {user_data['email']}")
    with col2:
        if user_data.get('organization'):
            st.write(f"**Organization:** {user_data['organization']}")
        st.write(f"**User ID:** {user_data['id']}")
    
    # Quick actions
    st.markdown("### Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🧪 DTI Prediction", use_container_width=True):
            st.info("Drug-Target Interaction prediction - Coming soon!")
    
    with col2:
        if st.button("🤖 AI Agents", use_container_width=True):
            st.info("24 AI agents - Coming soon!")
    
    with col3:
        if st.button("📊 Analytics", use_container_width=True):
            st.info("Usage analytics - Coming soon!")
    
    # Logout
    st.markdown("---")
    if st.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.user_data = None
        st.rerun()

def main():
    """Main application"""
    # Initialize session state
    if 'show_signup' not in st.session_state:
        st.session_state.show_signup = False
    
    # Show appropriate interface
    if st.session_state.get('show_signup', False):
        render_signup_form()
    else:
        render_login_interface()

if __name__ == "__main__":
    main()