"""
Landing Page and Authentication Interface for PharmQAgentAI
"""

import streamlit as st
from auth.user_management import UserManager, SubscriptionPlans
from datetime import datetime

def render_landing_page():
    """Render the main landing page with pricing and signup"""
    
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #1f77b4; font-size: 3rem; margin-bottom: 0.5rem;">
            PharmQAgentAI
        </h1>
        <h2 style="color: #666; font-size: 1.5rem; font-weight: 300;">
            Therapeutic Intelligence Platform
        </h2>
        <p style="font-size: 1.2rem; color: #888; max-width: 600px; margin: 0 auto;">
            Transform drug discovery with 24 specialized AI agents, advanced molecular predictions, 
            and comprehensive pharmaceutical intelligence
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero Section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://via.placeholder.com/600x300/1f77b4/ffffff?text=PharmQAgentAI+Platform", use_column_width=True)
    
    st.markdown("---")
    
    # Value Proposition
    st.markdown("### Why Choose PharmQAgentAI?")
    
    value_col1, value_col2, value_col3 = st.columns(3)
    
    with value_col1:
        st.markdown("""
        **🧠 24 AI Agents**
        - Drug Discovery Workflow
        - Risk Assessment & Optimization
        - Market Intelligence
        - Regulatory Compliance
        """)
    
    with value_col2:
        st.markdown("""
        **🔬 Advanced Predictions**
        - Drug-Target Interactions
        - ADMET Properties
        - Molecular Similarity
        - Safety Assessments
        """)
    
    with value_col3:
        st.markdown("""
        **📊 Professional Interface**
        - User-friendly dashboards
        - Visual data presentation
        - Real-time analytics
        - Export capabilities
        """)
    
    st.markdown("---")
    
    # Subscription Plans
    st.markdown("### Choose Your Plan")
    
    plan_col1, plan_col2, plan_col3 = st.columns(3)
    
    plans = SubscriptionPlans.PLANS
    
    with plan_col1:
        render_plan_card("Starter", plans["Starter"])
    
    with plan_col2:
        render_plan_card("Professional", plans["Professional"], featured=True)
    
    with plan_col3:
        render_plan_card("Enterprise", plans["Enterprise"])

def render_plan_card(plan_name: str, plan_details: dict, featured: bool = False):
    """Render individual subscription plan card"""
    
    border_color = "#1f77b4" if featured else "#ddd"
    background_color = "#f8f9fa" if featured else "#fff"
    
    card_html = f"""
    <div style="
        border: 2px solid {border_color};
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        background-color: {background_color};
        height: 400px;
        position: relative;
    ">
        <h3 style="color: #1f77b4; text-align: center; margin-bottom: 0.5rem;">
            {plan_name}
            {"⭐" if featured else ""}
        </h3>
        <h2 style="text-align: center; color: #333; margin-bottom: 0.5rem;">
            {plan_details['price']}
        </h2>
        <p style="text-align: center; color: #666; font-size: 0.9rem; margin-bottom: 1rem;">
            {plan_details['description']}
        </p>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)
    
    # Features list
    st.markdown("**Features:**")
    for feature in plan_details['features']:
        st.write(f"✓ {feature}")
    
    # Subscribe button
    if st.button(f"Choose {plan_name}", key=f"select_{plan_name}", use_container_width=True):
        st.session_state.selected_plan = plan_name
        st.session_state.show_signup = True
        st.rerun()

def render_auth_forms():
    """Render login and signup forms"""
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    user_manager = UserManager()
    
    with tab1:
        render_login_form(user_manager)
    
    with tab2:
        render_signup_form(user_manager)

def render_login_form(user_manager: UserManager):
    """Render login form"""
    
    st.markdown("### Welcome Back")
    
    with st.form("login_form"):
        email = st.text_input("Email Address", placeholder="your@email.com")
        password = st.text_input("Password", type="password")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            login_clicked = st.form_submit_button("Login", use_container_width=True)
        
        if login_clicked:
            if email and password:
                user_data = user_manager.authenticate_user(email, password)
                
                if user_data:
                    st.session_state.authenticated = True
                    st.session_state.user_data = user_data
                    
                    # Get subscription
                    subscription = user_manager.get_user_subscription(user_data['id'])
                    st.session_state.subscription = subscription
                    
                    st.success(f"Welcome back, {user_data['full_name']}!")
                    st.rerun()
                else:
                    st.error("Invalid email or password")
            else:
                st.error("Please fill in all fields")

def render_signup_form(user_manager: UserManager):
    """Render signup form"""
    
    selected_plan = st.session_state.get('selected_plan', 'Professional')
    
    st.markdown(f"### Join PharmQAgentAI - {selected_plan} Plan")
    
    plan_details = SubscriptionPlans.get_plan_features(selected_plan)
    st.info(f"You're signing up for the {selected_plan} plan at {plan_details.get('price', 'N/A')}")
    
    with st.form("signup_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name*", placeholder="John Doe")
            email = st.text_input("Email Address*", placeholder="john@company.com")
        
        with col2:
            organization = st.text_input("Organization", placeholder="Your Company/University")
            password = st.text_input("Password*", type="password")
        
        confirm_password = st.text_input("Confirm Password*", type="password")
        
        # Terms and conditions
        terms_accepted = st.checkbox("I accept the Terms of Service and Privacy Policy")
        
        signup_clicked = st.form_submit_button("Create Account & Subscribe", use_container_width=True)
        
        if signup_clicked:
            if not all([full_name, email, password, confirm_password]):
                st.error("Please fill in all required fields")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif len(password) < 8:
                st.error("Password must be at least 8 characters long")
            elif not terms_accepted:
                st.error("Please accept the terms and conditions")
            else:
                # Register user
                if user_manager.register_user(email, password, full_name, organization):
                    # Authenticate the new user
                    user_data = user_manager.authenticate_user(email, password)
                    
                    if user_data:
                        # Create subscription
                        duration_days = 30 if selected_plan != "Enterprise" else 365
                        user_manager.create_subscription(
                            user_data['id'], 
                            selected_plan, 
                            duration_days
                        )
                        
                        # Set session state
                        st.session_state.authenticated = True
                        st.session_state.user_data = user_data
                        
                        subscription = user_manager.get_user_subscription(user_data['id'])
                        st.session_state.subscription = subscription
                        
                        st.success(f"Account created successfully! Welcome to PharmQAgentAI, {full_name}!")
                        st.balloons()
                        
                        # Show payment simulation
                        st.info("🎉 Your subscription is now active! You can start using the platform immediately.")
                        
                        st.rerun()
                else:
                    st.error("Email address already exists. Please use a different email or try logging in.")

def render_user_dashboard():
    """Render user dashboard with account info"""
    
    user_data = st.session_state.get('user_data', {})
    subscription = st.session_state.get('subscription', {})
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Account Information")
    st.sidebar.markdown(f"**Name:** {user_data.get('full_name', 'Unknown')}")
    st.sidebar.markdown(f"**Email:** {user_data.get('email', 'Unknown')}")
    
    if subscription:
        plan_type = subscription.get('plan_type', 'No Plan')
        st.sidebar.markdown(f"**Plan:** {plan_type}")
        st.sidebar.markdown(f"**Status:** {subscription.get('payment_status', 'Unknown')}")
    
    if st.sidebar.button("Logout"):
        # Clear session state
        for key in ['authenticated', 'user_data', 'subscription']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

def check_feature_access(feature: str) -> bool:
    """Check if current user has access to a specific feature"""
    
    if not st.session_state.get('authenticated', False):
        return False
    
    subscription = st.session_state.get('subscription')
    if not subscription:
        return False
    
    plan_type = subscription.get('plan_type')
    return SubscriptionPlans.check_feature_access(plan_type, feature)

def render_access_denied(feature_name: str, required_plan: str):
    """Render access denied message with upgrade option"""
    
    st.warning(f"🔒 {feature_name} requires {required_plan} subscription")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Upgrade Your Plan", use_container_width=True):
            st.session_state.show_upgrade = True
            st.rerun()

def init_auth_session():
    """Initialize authentication session state"""
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None
    if 'subscription' not in st.session_state:
        st.session_state.subscription = None
    if 'selected_plan' not in st.session_state:
        st.session_state.selected_plan = 'Professional'
    if 'show_signup' not in st.session_state:
        st.session_state.show_signup = False