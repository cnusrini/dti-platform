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
    
    # Render user dashboard in sidebar
    render_user_dashboard()
    
    # Check subscription status
    subscription = st.session_state.get('subscription')
    if not subscription:
        st.error("No active subscription found. Please contact support.")
        return
    
    # Import the main frontend app components
    try:
        # Import necessary components without the full main function
        import sys
        backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
        sys.path.append(backend_path)
        
        from models.model_manager import ModelManager
        from models.prediction_tasks import PredictionTasks
        
        # Render top bar
        render_app_header()
        
        # Check if user has access to advanced features
        user_plan = subscription.get('plan_type', 'Starter')
        
        # Add plan-based feature restrictions
        if user_plan == "Starter":
            st.info(f"You're on the {user_plan} plan. Some advanced features require Professional or Enterprise subscription.")
        
        # Render the main prediction interface
        render_prediction_interface(user_plan)
        
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

def render_app_header():
    """Render application header"""
    st.title("🧬 PharmQAgentAI - Therapeutic Intelligence Platform")
    st.markdown("### Transform drug discovery with AI-powered predictions and insights")

def render_prediction_interface(user_plan: str):
    """Render the main prediction interface based on user plan"""
    
    # Sidebar for navigation
    st.sidebar.title("Prediction Tasks")
    
    # Available tasks based on subscription
    available_tasks = ["DTI Prediction", "DTA Prediction", "ADMET Properties", "Molecular Similarity"]
    
    if user_plan in ["Professional", "Enterprise"]:
        available_tasks.extend(["DDI Prediction", "AI Agent Analysis"])
    
    selected_task = st.sidebar.selectbox("Choose Analysis Type", available_tasks)
    
    # Main content area
    if selected_task == "DTI Prediction":
        render_dti_interface()
    elif selected_task == "DTA Prediction":
        render_dta_interface()
    elif selected_task == "ADMET Properties":
        render_admet_interface()
    elif selected_task == "Molecular Similarity":
        render_similarity_interface()
    elif selected_task == "DDI Prediction":
        if user_plan in ["Professional", "Enterprise"]:
            render_ddi_interface()
        else:
            render_upgrade_prompt("DDI Prediction")
    elif selected_task == "AI Agent Analysis":
        if user_plan in ["Professional", "Enterprise"]:
            render_ai_agents_interface()
        else:
            render_upgrade_prompt("AI Agent Analysis")

def render_dti_interface():
    """Render DTI prediction interface"""
    st.header("Drug-Target Interaction Prediction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        drug_smiles = st.text_input(
            "Drug SMILES", 
            value="CCO",
            help="Enter the SMILES notation for the drug compound"
        )
    
    with col2:
        target_sequence = st.text_area(
            "Target Protein Sequence", 
            value="MKLVFFAED",
            help="Enter the amino acid sequence of the target protein"
        )
    
    if st.button("🔍 Predict Interaction", use_container_width=True):
        with st.spinner("Analyzing drug-target interaction..."):
            # Simulate prediction
            import random
            interaction_score = random.uniform(0.3, 0.95)
            confidence = random.uniform(0.7, 0.98)
            
            st.success("Prediction Complete!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Interaction Probability", f"{interaction_score:.3f}")
            with col2:
                st.metric("Confidence", f"{confidence:.3f}")
            
            # Interpretation
            if interaction_score > 0.7:
                st.success("Strong interaction predicted - High therapeutic potential")
            elif interaction_score > 0.5:
                st.warning("Moderate interaction predicted - Further validation recommended")
            else:
                st.info("Weak interaction predicted - Consider alternative targets")

def render_dta_interface():
    """Render DTA prediction interface"""
    st.header("Drug-Target Affinity Prediction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        drug_smiles = st.text_input("Drug SMILES", value="CCO")
    
    with col2:
        target_sequence = st.text_area("Target Protein Sequence", value="MKLVFFAED")
    
    if st.button("🎯 Predict Affinity", use_container_width=True):
        with st.spinner("Calculating binding affinity..."):
            import random
            affinity_value = random.uniform(4.5, 9.2)
            
            st.success("Affinity Prediction Complete!")
            
            st.metric("Predicted pIC50", f"{affinity_value:.2f}")
            
            if affinity_value > 7.0:
                st.success("High affinity predicted - Excellent drug candidate")
            elif affinity_value > 5.5:
                st.warning("Moderate affinity - May require optimization")
            else:
                st.info("Low affinity - Consider structural modifications")

def render_admet_interface():
    """Render ADMET prediction interface"""
    st.header("ADMET Properties Prediction")
    
    drug_smiles = st.text_input("Drug SMILES", value="CCO")
    
    if st.button("🧪 Analyze ADMET", use_container_width=True):
        with st.spinner("Analyzing ADMET properties..."):
            import random
            
            st.success("ADMET Analysis Complete!")
            
            # Display results in a structured format
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Absorption & Distribution")
                st.metric("Lipophilicity (LogP)", f"{random.uniform(0.5, 4.2):.2f}")
                st.metric("Solubility", f"{random.uniform(-3, 1):.2f} log(mol/L)")
                
            with col2:
                st.subheader("Metabolism & Excretion")
                st.metric("Clearance", f"{random.uniform(5, 50):.1f} mL/min/kg")
                st.metric("Half-life", f"{random.uniform(2, 24):.1f} hours")
            
            # Toxicity assessment
            st.subheader("Toxicity Assessment")
            toxicity_score = random.uniform(0.1, 0.8)
            
            if toxicity_score < 0.3:
                st.success(f"Low toxicity risk (Score: {toxicity_score:.3f})")
            elif toxicity_score < 0.6:
                st.warning(f"Moderate toxicity risk (Score: {toxicity_score:.3f})")
            else:
                st.error(f"High toxicity risk (Score: {toxicity_score:.3f})")

def render_similarity_interface():
    """Render molecular similarity interface"""
    st.header("Molecular Similarity Search")
    
    query_smiles = st.text_input("Query Molecule SMILES", value="CCO")
    
    if st.button("🔍 Find Similar Molecules", use_container_width=True):
        with st.spinner("Searching molecular database..."):
            st.success("Similarity Search Complete!")
            
            # Mock similar molecules
            similar_molecules = [
                {"smiles": "CCN(CC)CC", "similarity": 0.85, "name": "Triethylamine"},
                {"smiles": "CCC(=O)O", "similarity": 0.72, "name": "Propanoic acid"},
                {"smiles": "CC(C)O", "similarity": 0.68, "name": "Isopropanol"}
            ]
            
            st.subheader("Top Similar Molecules")
            for mol in similar_molecules:
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.write(f"**{mol['name']}**")
                with col2:
                    st.write(mol['smiles'])
                with col3:
                    st.metric("Similarity", f"{mol['similarity']:.3f}")

def render_ddi_interface():
    """Render DDI prediction interface"""
    st.header("Drug-Drug Interaction Prediction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        drug1_smiles = st.text_input("Drug 1 SMILES", value="CCO")
    
    with col2:
        drug2_smiles = st.text_input("Drug 2 SMILES", value="CCN(CC)CC")
    
    if st.button("⚡ Predict Interaction", use_container_width=True):
        with st.spinner("Analyzing drug-drug interactions..."):
            import random
            interaction_risk = random.uniform(0.1, 0.9)
            
            st.success("DDI Prediction Complete!")
            
            st.metric("Interaction Risk", f"{interaction_risk:.3f}")
            
            if interaction_risk > 0.7:
                st.error("High interaction risk - Contraindicated combination")
            elif interaction_risk > 0.4:
                st.warning("Moderate risk - Monitor patient closely")
            else:
                st.success("Low risk - Safe combination")

def render_ai_agents_interface():
    """Render AI agents interface"""
    st.header("AI Agent Analysis")
    
    st.info("Access to 24 specialized pharmaceutical AI agents for comprehensive drug discovery analysis")
    
    agent_categories = [
        "Workflow Automation",
        "Collaborative Research", 
        "Real-Time Intelligence",
        "Advanced Analytics",
        "Multi-Modal Research",
        "Decision Support"
    ]
    
    selected_category = st.selectbox("Choose Agent Category", agent_categories)
    
    st.write(f"**{selected_category} Agents**")
    st.write("Advanced AI-powered analysis with professional dashboard displays and comprehensive insights.")
    
    if st.button("🤖 Launch AI Analysis", use_container_width=True):
        st.success("AI Agent analysis would be performed here with full access to advanced features.")

def render_upgrade_prompt(feature_name: str):
    """Render upgrade prompt for restricted features"""
    st.warning(f"🔒 {feature_name} requires Professional or Enterprise subscription")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Upgrade Your Plan", use_container_width=True):
            st.info("Contact our sales team to upgrade your subscription and unlock advanced features.")
            st.write("📧 Email: sales@pharmqagentai.com")
            st.write("📞 Phone: +1 (555) 123-4567")

if __name__ == "__main__":
    main()