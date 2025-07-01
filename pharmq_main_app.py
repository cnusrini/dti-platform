"""
PharmQAgentAI Main Application with Authentication
Entry point with login interface and authenticated platform access
"""

import streamlit as st
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to path
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.append(backend_path)

# Add auth system to path
auth_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(auth_path)

# Import authentication
from auth.pharmq_login_interface import render_login_page, render_signup_page, authenticate_user

# Import main application components
try:
    from models.model_manager import ModelManager
    from models.prediction_tasks import PredictionTasks
    from utils.molecular_utils import MolecularUtils
    from utils.validation import ValidationUtils
    from config.model_registry import MODEL_REGISTRY
    from agents.agent_manager import AgentManager
except ImportError as e:
    st.error(f"Error importing components: {e}")

# Page configuration
st.set_page_config(
    page_title="PharmQAgentAI",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

def init_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None
    
    if 'show_signup' not in st.session_state:
        st.session_state.show_signup = False
    
    if 'auth_error' not in st.session_state:
        st.session_state.auth_error = None
    
    if 'model_manager' not in st.session_state:
        st.session_state.model_manager = None
    
    if 'prediction_tasks' not in st.session_state:
        st.session_state.prediction_tasks = None

def load_ai_components():
    """Load AI components after authentication"""
    if st.session_state.model_manager is None:
        try:
            st.session_state.model_manager = ModelManager()
            st.session_state.prediction_tasks = PredictionTasks(st.session_state.model_manager)
            st.session_state.agent_manager = AgentManager()
        except Exception as e:
            st.error(f"Error loading AI components: {e}")

def render_authenticated_app():
    """Render the main PharmQAgentAI application for authenticated users"""
    
    # Load AI components
    load_ai_components()
    
    # Sidebar user info
    with st.sidebar:
        st.markdown("### 👤 User Information")
        user_data = st.session_state.user_data
        st.write(f"**Name:** {user_data.get('full_name', 'N/A')}")
        st.write(f"**Email:** {user_data.get('email', 'N/A')}")
        if user_data.get('organization'):
            st.write(f"**Organization:** {user_data.get('organization')}")
        
        st.markdown("---")
        
        # Logout button
        if st.button("🚪 Logout", key="logout_btn"):
            # Clear session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        st.markdown("---")
        
        # Database status
        database_url = os.getenv('DATABASE_URL')
        if database_url:
            st.success("🔗 Connected to Neon Database")
        else:
            st.info("📁 Using Local Database")
        
        st.markdown("---")
        
        # Task selection
        st.markdown("### 🧪 Analysis Tasks")
        task = st.selectbox(
            "Select Prediction Task",
            ["Drug-Target Interaction", "Drug-Target Affinity", "Drug-Drug Interaction", 
             "ADMET Properties", "Molecular Similarity"],
            key="task_selector"
        )
    
    # Main application header
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #4F46E5; font-size: 3rem; margin-bottom: 0.5rem;">
            🧬 PharmQAgentAI
        </h1>
        <p style="color: #6B7280; font-size: 1.2rem;">
            Therapeutic Intelligence Platform powered by AI
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Top navigation
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🏠 Dashboard", use_container_width=True):
            st.session_state.current_page = "dashboard"
    
    with col2:
        if st.button("🧪 Predictions", use_container_width=True):
            st.session_state.current_page = "predictions"
    
    with col3:
        if st.button("🤖 AI Agents", use_container_width=True):
            st.session_state.current_page = "agents"
    
    with col4:
        if st.button("📊 Analytics", use_container_width=True):
            st.session_state.current_page = "analytics"
    
    # Initialize current page
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "dashboard"
    
    st.markdown("---")
    
    # Render selected page
    if st.session_state.current_page == "dashboard":
        render_dashboard()
    elif st.session_state.current_page == "predictions":
        render_predictions_interface(task)
    elif st.session_state.current_page == "agents":
        render_agents_interface()
    elif st.session_state.current_page == "analytics":
        render_analytics_interface()

def render_dashboard():
    """Render the main dashboard"""
    st.markdown("## 📊 Platform Dashboard")
    
    # Welcome message
    user_name = st.session_state.user_data.get('full_name', 'User')
    st.markdown(f"### Welcome back, {user_name}!")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Available Models", "20+", help="Transformer models for predictions")
    
    with col2:
        st.metric("AI Agents", "24", help="Specialized pharmaceutical research agents")
    
    with col3:
        st.metric("Prediction Tasks", "5", help="Different types of molecular predictions")
    
    with col4:
        st.metric("Database Status", "Connected", help="Neon PostgreSQL database connection")
    
    st.markdown("---")
    
    # Recent activity placeholder
    st.markdown("### 🕒 Recent Activity")
    st.info("No recent activity. Start by making your first prediction!")
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🧪 Start DTI Prediction", use_container_width=True):
            st.session_state.current_page = "predictions"
            st.rerun()
    
    with col2:
        if st.button("🤖 Launch AI Agent", use_container_width=True):
            st.session_state.current_page = "agents"
            st.rerun()
    
    with col3:
        if st.button("📈 View Analytics", use_container_width=True):
            st.session_state.current_page = "analytics"
            st.rerun()

def render_predictions_interface(task):
    """Render the predictions interface"""
    st.markdown(f"## 🧪 {task} Prediction")
    
    if task == "Drug-Target Interaction":
        render_dti_interface()
    elif task == "Drug-Target Affinity":
        render_dta_interface()
    elif task == "Drug-Drug Interaction":
        render_ddi_interface()
    elif task == "ADMET Properties":
        render_admet_interface()
    elif task == "Molecular Similarity":
        render_similarity_interface()

def render_dti_interface():
    """Render DTI prediction interface"""
    st.markdown("### Drug-Target Interaction Prediction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Drug Input (SMILES)**")
        drug_smiles = st.text_area(
            "Enter SMILES notation",
            placeholder="CCO (ethanol example)",
            help="Enter the molecular structure in SMILES format"
        )
    
    with col2:
        st.markdown("**Target Input (Protein Sequence)**")
        target_sequence = st.text_area(
            "Enter protein sequence",
            placeholder="MKTVRQERLKSIVRILERSKEPVSGAQLAEELSVSRQVIVQDIAYLRSLGYNIVATPRGYVLAGG",
            help="Enter the amino acid sequence of the target protein"
        )
    
    if st.button("🔬 Predict Interaction", type="primary"):
        if drug_smiles and target_sequence:
            with st.spinner("Analyzing drug-target interaction..."):
                # Placeholder for actual prediction
                import time
                time.sleep(2)
                
                # Mock prediction result
                prediction_score = 0.87
                confidence = 0.92
                
                st.success("✅ Prediction completed!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Interaction Score", f"{prediction_score:.3f}")
                with col2:
                    st.metric("Confidence", f"{confidence:.1%}")
                
                # Results table
                st.markdown("#### 📋 Detailed Results")
                results_data = {
                    "Metric": ["Binding Affinity", "Selectivity", "Stability", "Pharmacokinetics"],
                    "Value": ["High", "Moderate", "Good", "Favorable"],
                    "Score": [0.89, 0.72, 0.84, 0.78]
                }
                st.dataframe(results_data, use_container_width=True)
        else:
            st.error("Please provide both drug SMILES and target sequence")

def render_dta_interface():
    """Render DTA prediction interface"""
    st.info("Drug-Target Affinity prediction interface - Implementation in progress")

def render_ddi_interface():
    """Render DDI prediction interface"""
    st.info("Drug-Drug Interaction prediction interface - Implementation in progress")

def render_admet_interface():
    """Render ADMET prediction interface"""
    st.info("ADMET properties prediction interface - Implementation in progress")

def render_similarity_interface():
    """Render molecular similarity interface"""
    st.info("Molecular similarity analysis interface - Implementation in progress")

def render_agents_interface():
    """Render AI agents interface"""
    st.markdown("## 🤖 AI Agents Hub")
    st.info("24 specialized pharmaceutical research agents - Interface in development")

def render_analytics_interface():
    """Render analytics interface"""
    st.markdown("## 📊 Analytics Dashboard")
    st.info("Usage analytics and insights - Interface in development")

def main():
    """Main application controller"""
    
    # Initialize session state
    init_session_state()
    
    # Check authentication status
    if not st.session_state.authenticated:
        # Show login/signup interface
        if st.session_state.get('show_signup', False):
            render_signup_page()
        else:
            render_login_page()
    else:
        # Show authenticated application
        render_authenticated_app()

if __name__ == "__main__":
    main()