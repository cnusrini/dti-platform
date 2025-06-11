"""
Main Application Entry Point for PharmQAgentAI
Handles routing between landing page and authenticated application
"""

import streamlit as st
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import authentication and main app components
from auth.landing_page import (
    render_landing_page, 
    render_auth_forms, 
    render_user_dashboard,
    init_auth_session,
    check_feature_access,
    render_access_denied
)

def main():
    """Main application controller"""
    
    # Configure page
    st.set_page_config(
        page_title="PharmQAgentAI - Therapeutic Intelligence Platform",
        page_icon="🧬",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize authentication session
    init_auth_session()
    
    # Check authentication status
    if not st.session_state.get('authenticated', False):
        # Show landing page and authentication
        render_landing_page()
        
        # Show authentication forms in sidebar or main area
        st.markdown("---")
        st.markdown("### Get Started")
        render_auth_forms()
        
    else:
        # User is authenticated - show main application
        render_authenticated_app()

def render_authenticated_app():
    """Render the main application for authenticated users"""
    
    # Import the main frontend app
    try:
        from frontend.app import main as frontend_main, render_sidebar, render_top_bar
        
        # Render user dashboard in sidebar
        render_user_dashboard()
        
        # Check subscription status
        subscription = st.session_state.get('subscription')
        if not subscription:
            st.error("No active subscription found. Please contact support.")
            return
        
        # Render top bar
        render_top_bar()
        
        # Check if user has access to advanced features
        user_plan = subscription.get('plan_type', 'Starter')
        
        # Add plan-based feature restrictions
        if user_plan == "Starter":
            st.info(f"You're on the {user_plan} plan. Some advanced features require Professional or Enterprise subscription.")
        
        # Render the main application
        frontend_main()
        
        # Track usage
        if 'user_data' in st.session_state:
            from auth.user_management import UserManager
            user_manager = UserManager()
            user_manager.track_usage(
                st.session_state.user_data['id'], 
                'app_access'
            )
            
    except ImportError as e:
        st.error(f"Error loading application: {e}")
        st.info("Please ensure all required modules are installed.")

if __name__ == "__main__":
    main()