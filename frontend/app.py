"""
PharmQAgentAI Frontend Application
Therapeutic Intelligence Platform with Backend/Frontend Architecture
"""

import streamlit as st
import sys
import os
from datetime import datetime

# Add backend to path
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.append(backend_path)

from models.model_manager import ModelManager
from models.prediction_tasks import PredictionTasks
from utils.molecular_utils import MolecularUtils
from utils.validation import ValidationUtils
from utils.model_preloader import ModelPreloader
from config.model_registry import MODEL_REGISTRY
from agents.agent_manager import agent_manager

# Page configuration
st.set_page_config(
    page_title="PharmQAgentAI",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to match emedchainhub.com design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Reset and base styling */
    .main .block-container {
        padding: 1rem 2rem;
        max-width: 1200px;
        background: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Dark professional header */
    .main-header {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(30, 41, 59, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Modern card design */
    .prediction-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
        transition: all 0.3s ease;
    }
    
    .prediction-card:hover {
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        transform: translateY(-2px);
    }
    
    /* Sophisticated button styling with multiple selectors */
    .stButton > button,
    button[kind="primary"],
    button[kind="secondary"],
    .stButton button,
    button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 0.025em !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.24) !important;
        font-size: 14px !important;
        line-height: 1.5 !important;
        text-decoration: none !important;
        text-shadow: none !important;
    }
    
    .stButton > button *,
    button[kind="primary"] *,
    button[kind="secondary"] *,
    .stButton button *,
    button * {
        color: #ffffff !important;
    }
    
    .stButton > button:hover,
    button[kind="primary"]:hover,
    button[kind="secondary"]:hover,
    .stButton button:hover,
    button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important;
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.32) !important;
        transform: translateY(-1px) !important;
        color: #ffffff !important;
    }
    
    .stButton > button:hover *,
    button[kind="primary"]:hover *,
    button[kind="secondary"]:hover *,
    .stButton button:hover *,
    button:hover * {
        color: #ffffff !important;
    }
    
    .stButton > button:focus,
    button[kind="primary"]:focus,
    button[kind="secondary"]:focus,
    .stButton button:focus,
    button:focus {
        color: #ffffff !important;
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3) !important;
    }
    
    .stButton > button:active,
    button[kind="primary"]:active,
    button[kind="secondary"]:active,
    .stButton button:active,
    button:active {
        color: #ffffff !important;
        background: linear-gradient(135deg, #1e40af 0%, #1d4ed8 100%) !important;
    }
    
    /* Sidebar with modern design */
    .css-1d391kg {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        border-right: 1px solid #e2e8f0;
    }
    
    /* Enhanced metrics */
    .metric-container {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.75rem 0;
        text-align: center;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
        transition: all 0.3s ease;
    }
    
    .metric-container:hover {
        border-color: #3b82f6;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.1);
    }
    
    /* Professional table styling */
    .stDataFrame {
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
    }
    
    /* Modern input fields */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        background: white;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 16px rgba(59, 130, 246, 0.12);
        outline: none;
    }
    
    /* Status indicators */
    .success-indicator {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        display: inline-block;
    }
    
    .warning-indicator {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        display: inline-block;
    }
    
    .error-indicator {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        display: inline-block;
    }
    
    /* Progress bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #3b82f6 0%, #1d4ed8 100%);
        border-radius: 8px;
    }
    
    /* Modern tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: white;
        border-radius: 12px;
        padding: 0.5rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #64748b;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.24);
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        background: white;
    }
    
    /* Typography */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        color: #1e293b;
    }
    
    p, div {
        font-family: 'Inter', sans-serif;
        color: #475569;
    }
    
    /* Professional accent */
    .professional-accent {
        color: #3b82f6;
        font-weight: 600;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    header {visibility: hidden;}
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        .main-header {
            padding: 1.5rem;
        }
        .prediction-card {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'model_manager' not in st.session_state:
    st.session_state.model_manager = ModelManager()
if 'prediction_tasks' not in st.session_state:
    st.session_state.prediction_tasks = PredictionTasks(st.session_state.model_manager)
if 'molecular_utils' not in st.session_state:
    st.session_state.molecular_utils = MolecularUtils()
if 'validation_utils' not in st.session_state:
    st.session_state.validation_utils = ValidationUtils()
if 'model_preloader' not in st.session_state:
    st.session_state.model_preloader = ModelPreloader(st.session_state.model_manager)
if 'current_task' not in st.session_state:
    st.session_state.current_task = 'DTI'
if 'loaded_models' not in st.session_state:
    st.session_state.loaded_models = {}
if 'prediction_results' not in st.session_state:
    st.session_state.prediction_results = {}
if 'ai_chat_history' not in st.session_state:
    st.session_state.ai_chat_history = []
if 'agent_analysis' not in st.session_state:
    st.session_state.agent_analysis = {}
if 'show_results_after_analysis' not in st.session_state:
    st.session_state.show_results_after_analysis = False

def render_top_bar():
    """Render the top navigation bar"""
    st.markdown("""
    <div class="main-header">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
            <div style="flex: 1;">
                <h1 style="margin: 0; font-size: 1.8rem; color: white; font-family: 'Inter', sans-serif; font-weight: 700; line-height: 1.2;">🧬 PharmQAgentAI</h1>
                <p style="margin: 0.2rem 0 0 0; font-size: 0.9rem; color: #cbd5e1; font-family: 'Inter', sans-serif; font-weight: 400; opacity: 0.8;">Advanced Therapeutic Intelligence Platform</p>
            </div>
            <div style="display: flex; gap: 1rem; align-items: center;">
                <div style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.16); border-radius: 8px; padding: 0.6rem 1rem; text-align: center; min-width: 90px;">
                    <div style="color: #e2e8f0; font-weight: 600; font-size: 0.75rem; font-family: 'Inter', sans-serif; margin-bottom: 0.1rem;">Models</div>
                    <div style="color: #60a5fa; font-size: 1.4rem; font-weight: 700; line-height: 1;">{}</div>
                </div>
                <div style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.16); border-radius: 8px; padding: 0.6rem 1rem; text-align: center; min-width: 80px;">
                    <div style="color: #e2e8f0; font-weight: 600; font-size: 0.75rem; font-family: 'Inter', sans-serif; margin-bottom: 0.1rem;">Status</div>
                    <div style="color: {}; font-size: 1rem; font-weight: 600; line-height: 1;">{}</div>
                </div>
            </div>
        </div>
    </div>
    """.format(
        len(st.session_state.model_manager.get_loaded_models()) if st.session_state.model_manager else 0,
        "#10b981" if st.session_state.loaded_models else "#f59e0b",
        "Ready" if st.session_state.loaded_models else "Standby"
    ), unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar with task selection and model management"""
    st.sidebar.title("Navigation")
    st.sidebar.markdown("---")
    
    # Task selection
    tasks = ['DTI', 'DTA', 'DDI', 'ADMET', 'Similarity']
    current_task = st.sidebar.selectbox(
        "Select Task",
        tasks,
        index=tasks.index(st.session_state.current_task),
        key="task_selector"
    )
    
    if current_task != st.session_state.current_task:
        st.session_state.current_task = current_task
        st.rerun()
    
    st.sidebar.divider()
    
    # Transformer DTI Model Preloader
    st.sidebar.subheader("🚀 Transformer DTI Models")
    
    # Preload status display
    preload_status = st.session_state.model_preloader.get_preload_status()
    preloaded_models = st.session_state.model_preloader.get_preloaded_models()
    
    if preloaded_models:
        st.sidebar.success(f"✓ {len(preloaded_models)} models loaded")
        with st.sidebar.expander("Loaded Models"):
            for model in preloaded_models:
                st.write(f"• {model}")
    
    # Preload all transformer DTI models button
    if st.sidebar.button("Load All Transformer Models", key="preload_all_models", type="primary"):
        with st.spinner("Loading all transformer DTI models..."):
            preload_results = st.session_state.model_preloader.preload_transformer_dti_models()
            
            # Update session state with loaded models
            for model_name in preload_results['success_models']:
                model_key = f"DTI_{model_name}"
                st.session_state.loaded_models[model_key] = {
                    'task': 'DTI',
                    'name': model_name,
                    'loaded_at': datetime.now()
                }
            
            if preload_results['loaded_successfully'] > 0:
                st.sidebar.success(f"Successfully loaded {preload_results['loaded_successfully']} models!")
            
            if preload_results['failed_models']:
                st.sidebar.warning(f"{len(preload_results['failed_models'])} models failed to load")
                
            st.rerun()
    
    st.sidebar.divider()
    
    # Model selector for current task
    st.sidebar.subheader(f"{current_task} Models")
    
    available_models = MODEL_REGISTRY.get(current_task, {})
    if available_models:
        model_options = list(available_models.keys())
        selected_model = st.sidebar.selectbox(
            "Choose Model",
            model_options,
            key=f"model_selector_{current_task}"
        )
        
        # Model loading
        col1, col2 = st.sidebar.columns([2, 1])
        with col1:
            load_button = st.button(
                f"Load {selected_model}",
                key=f"load_button_{current_task}",
                use_container_width=True
            )
        with col2:
            # Model status indicator
            model_key = f"{current_task}_{selected_model}"
            if model_key in st.session_state.loaded_models:
                st.success("✓")
            else:
                st.error("✗")
        
        # Model reference link
        model_config = available_models.get(selected_model, {})
        model_url = model_config.get('url')
        if model_url:
            st.sidebar.markdown(f"🔗 [View {selected_model} on Hugging Face]({model_url})")
        
        # Model description
        model_description = model_config.get('description')
        if model_description:
            st.sidebar.caption(model_description)
        
        if load_button:
            try:
                with st.spinner(f"Loading {selected_model}..."):
                    success = st.session_state.model_manager.load_model(
                        current_task, 
                        selected_model, 
                        available_models[selected_model]
                    )
                    
                    if success:
                        st.session_state.loaded_models[model_key] = {
                            'task': current_task,
                            'name': selected_model,
                            'loaded_at': datetime.now()
                        }
                        st.sidebar.success(f"Loaded {selected_model}")
                        st.rerun()
                    else:
                        st.sidebar.error(f"Failed to load {selected_model}")
            except Exception as e:
                st.sidebar.error(f"Error loading model: {str(e)}")
    
    # Sample Data Section
    st.sidebar.divider()
    st.sidebar.subheader("📋 Quick Test Data")
    st.sidebar.caption("One-click loading with authentic molecular examples")
    
    # Sample data selector
    sample_sets = {
        "Aspirin + COX-2": {"type": "DTI", "drug": "CC(=O)OC1=CC=CC=C1C(=O)O", "description": "Anti-inflammatory"},
        "Caffeine + Adenosine": {"type": "DTI", "drug": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C", "description": "Stimulant"},
        "Paclitaxel + Tubulin": {"type": "DTA", "drug": "CC1=C2C(C(=O)C3(C(CC4C(C3C(C(C2(C)C)(CC1OC(=O)C(C(C5=CC=CC=C5)NC(=O)C6=CC=CC=C6)O)O)OC(=O)C7=CC=CC=C7)(CO4)OC(=O)C)O)C)OC(=O)C", "description": "Anticancer"},
        "Warfarin + Vitamin K": {"type": "DDI", "drug1": "CC1=CC2=C(C=C1)SC(=O)NC2=O", "drug2": "CC(CCCC(C)CCCC(C)CCCC(C)C)C", "description": "Anticoagulant"},
        "Atorvastatin Properties": {"type": "ADMET", "drug": "CC(C)C1=C(C(=C(N1CC[C@H](C[C@H](CC(=O)O)O)O)C2=CC=C(C=C2)F)C3=CC=CC=C3)C(=O)NC4=CC=CC=C4", "description": "Cholesterol drug"},
        "Morphine Analogs": {"type": "Similarity", "drug": "CN1CC[C@]23C4=C5C=CC(=C4C(=O)CC[C@H]2[C@H]1CC6=C3C(=C(C=C6)O)O5)O", "description": "Opioid analgesic"}
    }
    
    selected_sample = st.sidebar.selectbox(
        "Choose Sample Dataset",
        list(sample_sets.keys()),
        format_func=lambda x: f"{sample_sets[x]['type']}: {sample_sets[x]['description']}"
    )
    
    if st.sidebar.button("Load Selected Sample", type="primary", key="load_selected_sample"):
        sample = sample_sets[selected_sample]
        task_type = sample["type"]
        
        if task_type == "DTI":
            st.session_state.dti_drug_smiles = sample["drug"]
            st.session_state.dti_target_sequence = "MKVLWAALLVTFLAGCQAKVEQAVETEPEPELRQQTEWQSGQRWELALGRFWDYLRWVQTLSEQVQEELLSSQVTQELRALMDETAQALPQPVRQLLSSQVTQELRALMDETAQ"
            st.session_state.current_task = "DTI"
        elif task_type == "DTA":
            st.session_state.dta_drug_smiles = sample["drug"]
            st.session_state.dta_target_sequence = "MKVLWAALLVTFLAGCQAKVEQAVETEPEPELRQQTEWQSGQRWELALGRFWDYLRWVQTLSEQVQEELLSSQVTQELRALMDETAQALPQPVRQLLSSQVTQELRALMDETAQ"
            st.session_state.current_task = "DTA"
        elif task_type == "DDI":
            st.session_state.ddi_drug1_smiles = sample["drug1"]
            st.session_state.ddi_drug2_smiles = sample["drug2"]
            st.session_state.current_task = "DDI"
        elif task_type == "ADMET":
            st.session_state.admet_drug_smiles = sample["drug"]
            st.session_state.current_task = "ADMET"
        elif task_type == "Similarity":
            st.session_state.sim_query_smiles = sample["drug"]
            st.session_state.current_task = "Similarity"
        
        st.sidebar.success(f"Loaded {sample['description']} sample")
        st.rerun()
    
    # Additional quick samples
    with st.sidebar.expander("More Examples"):
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Ibuprofen", key="quick_ibuprofen", use_container_width=True):
                st.session_state.dti_drug_smiles = "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O"
                st.session_state.current_task = "DTI"
                st.rerun()
        
        with col2:
            if st.button("Acetaminophen", key="quick_acetaminophen", use_container_width=True):
                st.session_state.dti_drug_smiles = "CC(=O)NC1=CC=C(C=C1)O"
                st.session_state.current_task = "DTI"
                st.rerun()
        
        with col1:
            if st.button("Dopamine", key="quick_dopamine", use_container_width=True):
                st.session_state.dti_drug_smiles = "C1=CC(=C(C=C1CCN)O)O"
                st.session_state.current_task = "DTI"
                st.rerun()
        
        with col2:
            if st.button("Insulin", key="quick_insulin", use_container_width=True):
                st.session_state.dti_target_sequence = "GIVEQCCTSICSLYQLENYCNFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN"
                st.session_state.current_task = "DTI"
                st.rerun()
    
    # Model Reference Center
    st.sidebar.divider()
    st.sidebar.subheader("📚 Model Reference")
    
    if st.sidebar.button("View All Models", use_container_width=True):
        with st.sidebar.expander("Model Library", expanded=True):
            for task, models in MODEL_REGISTRY.items():
                st.write(f"**{task} Models:**")
                for model_name, config in models.items():
                    model_url = config.get('url')
                    if model_url:
                        st.markdown(f"• [🔗 {model_name}]({model_url})")
                    else:
                        st.write(f"• {model_name}")
                st.divider()
    
    # Cleanup models
    if st.sidebar.button("Unload All Models", type="secondary", use_container_width=True):
        st.session_state.model_manager.unload_all_models()
        st.session_state.loaded_models = {}
        st.sidebar.success("All models unloaded")
        st.rerun()

def render_dti_interface():
    """Render DTI prediction interface"""
    st.header("🎯 Drug-Target Interaction (DTI) Prediction")
    st.info("Predict interaction probability between drug compounds and target proteins using transformer models")
    
    # Get sample data from session state if loaded via sidebar
    default_drug = getattr(st.session_state, 'dti_drug_smiles', "")
    default_target = getattr(st.session_state, 'dti_target_sequence', "")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Drug Input")
        drug_smiles = st.text_area(
            "SMILES String",
            value=default_drug,
            placeholder="Enter drug SMILES (e.g., CC(=O)OC1=CC=CC=C1C(=O)O)",
            height=100,
            key="dti_drug_input"
        )
    
    with col2:
        st.subheader("Target Input")
        target_sequence = st.text_area(
            "Protein Sequence",
            value=default_target,
            placeholder="Enter target protein sequence (FASTA format)",
            height=100,
            key="dti_target_input"
        )
    
    # Prediction
    if st.button("Predict DTI", type="primary", disabled=not (drug_smiles and target_sequence)):
        with st.spinner("Predicting drug-target interaction..."):
            try:
                result = st.session_state.prediction_tasks.predict_dti(drug_smiles, target_sequence)
                
                if result:
                    st.success("DTI Prediction Completed")
                    
                    # Store prediction results for AI analysis
                    st.session_state.prediction_results['DTI'] = result
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        score = result.get('score', 0.0)
                        if isinstance(score, (int, float)):
                            st.metric("Interaction Score", f"{score:.3f}")
                        else:
                            st.metric("Interaction Score", str(score))
                    
                    with col2:
                        confidence = result.get('confidence')
                        if confidence:
                            st.metric("Confidence", f"{confidence*100:.1f}%")
                        else:
                            st.metric("Confidence", "N/A")
                    
                    with col3:
                        model_info = result.get('model_info', 'Unknown')
                        st.metric("Model Used", model_info)
                        
                        # Add model reference link
                        if model_info != 'Unknown':
                            model_config = MODEL_REGISTRY.get('DTI', {}).get(model_info, {})
                            model_url = model_config.get('url')
                            if model_url:
                                st.markdown(f"🔗 [View on Hugging Face]({model_url})", unsafe_allow_html=True)
                    
                    # Model Information Section
                    if model_info != 'Unknown':
                        with st.expander("📊 Model Information", expanded=False):
                            model_config = MODEL_REGISTRY.get('DTI', {}).get(model_info, {})
                            if model_config:
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.write(f"**Description:** {model_config.get('description', 'N/A')}")
                                    st.write(f"**Model Type:** {model_config.get('model_type', 'N/A')}")
                                    st.write(f"**Dataset:** {model_config.get('dataset', 'N/A')}")
                                
                                with col2:
                                    performance = model_config.get('performance', {})
                                    if performance:
                                        st.write("**Performance Metrics:**")
                                        for metric, value in performance.items():
                                            if metric != 'dataset':
                                                st.write(f"• {metric.upper()}: {value}")
                                
                                model_url = model_config.get('url')
                                if model_url:
                                    st.markdown(f"🔗 **[View Model on Hugging Face]({model_url})**")
                    
                    # Additional details in table format
                    if result.get('details'):
                        st.subheader("Detailed Analysis")
                        
                        # Create a beautiful results table
                        details_data = []
                        for key, value in result['details'].items():
                            if isinstance(value, dict):
                                for sub_key, sub_value in value.items():
                                    details_data.append({
                                        "Property": f"{key.replace('_', ' ').title()} - {sub_key.replace('_', ' ').title()}",
                                        "Value": str(sub_value),
                                        "Category": key.replace('_', ' ').title()
                                    })
                            else:
                                details_data.append({
                                    "Property": key.replace('_', ' ').title(),
                                    "Value": str(value),
                                    "Category": "General"
                                })
                        
                        if details_data:
                            import pandas as pd
                            df = pd.DataFrame(details_data)
                            st.dataframe(
                                df,
                                use_container_width=True,
                                hide_index=True,
                                column_config={
                                    "Property": st.column_config.TextColumn(
                                        "Property",
                                        help="Analysis parameter"
                                    ),
                                    "Value": st.column_config.TextColumn(
                                        "Value",
                                        help="Predicted or calculated value"
                                    ),
                                    "Category": st.column_config.TextColumn(
                                        "Category",
                                        help="Result category"
                                    )
                                }
                            )
                else:
                    st.error("Prediction failed. Please ensure a model is loaded.")
            
            except Exception as e:
                st.error(f"Prediction error: {str(e)}")

def render_dta_interface():
    """Render DTA prediction interface"""
    st.header("⚖️ Drug-Target Binding Affinity (DTA) Prediction")
    st.info("Predict binding affinity values between drug compounds and target proteins")
    
    col1, col2 = st.columns(2)
    
    with col1:
        drug_smiles = st.text_area("Drug SMILES", height=100, key="dta_drug_smiles")
    
    with col2:
        target_sequence = st.text_area("Target Sequence", height=100, key="dta_target_sequence")
        affinity_type = st.selectbox("Affinity Type", ["IC50", "Kd", "Ki"])
    
    if st.button("Predict Binding Affinity", type="primary", disabled=not (drug_smiles and target_sequence)):
        with st.spinner("Calculating binding affinity..."):
            try:
                result = st.session_state.prediction_tasks.predict_dta(drug_smiles, target_sequence, affinity_type)
                
                if result:
                    st.success("DTA Prediction Completed")
                    
                    # Store prediction results for AI analysis
                    st.session_state.prediction_results['DTA'] = result
                    
                    score = result.get('score', 0.0)
                    st.metric(f"Predicted {affinity_type}", f"{score:.2f} nM" if isinstance(score, (int, float)) else str(score))
                else:
                    st.error("Prediction failed. Please ensure a model is loaded.")
            
            except Exception as e:
                st.error(f"Prediction error: {str(e)}")

def render_ddi_interface():
    """Render DDI prediction interface"""
    st.header("💊 Drug-Drug Interaction (DDI) Prediction")
    st.info("Analyze potential interactions between drug compounds")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Drug 1")
        drug1_smiles = st.text_area("Drug 1 SMILES", height=100, key="ddi_drug1_smiles")
    
    with col2:
        st.subheader("Drug 2")
        drug2_smiles = st.text_area("Drug 2 SMILES", height=100, key="ddi_drug2_smiles")
    
    interaction_type = st.selectbox("Interaction Type", ["Synergistic", "Antagonistic", "Unknown"])
    
    if st.button("Predict DDI", type="primary", disabled=not (drug1_smiles and drug2_smiles)):
        with st.spinner("Analyzing drug-drug interaction..."):
            try:
                result = st.session_state.prediction_tasks.predict_ddi(drug1_smiles, drug2_smiles, interaction_type)
                
                if result:
                    st.success("DDI Prediction Completed")
                    
                    # Store prediction results for AI analysis
                    st.session_state.prediction_results['DDI'] = result
                    
                    score = result.get('score', 0.0)
                    if isinstance(score, (int, float)):
                        if score > 0.5:
                            st.warning(f"Potential {interaction_type.lower()} interaction detected: {score:.3f}")
                        else:
                            st.info(f"Low interaction probability: {score:.3f}")
                    else:
                        st.info(f"Interaction result: {str(score)}")
                else:
                    st.error("Prediction failed. Please ensure a model is loaded.")
            
            except Exception as e:
                st.error(f"Prediction error: {str(e)}")

def render_admet_interface():
    """Render ADMET prediction interface"""
    st.header("🧪 ADMET Properties Prediction")
    st.info("Predict Absorption, Distribution, Metabolism, Excretion, and Toxicity properties")
    
    drug_smiles = st.text_area("Drug SMILES", height=100, key="admet_drug_smiles")
    
    properties = st.multiselect(
        "Select ADMET Properties",
        ["absorption", "distribution", "metabolism", "excretion", "toxicity", "ld50", "logp", "solubility", "bioavailability", "clearance"],
        default=["absorption", "toxicity"]
    )
    
    if st.button("Predict ADMET", type="primary", disabled=not (drug_smiles and properties)):
        with st.spinner("Calculating ADMET properties..."):
            try:
                result = st.session_state.prediction_tasks.predict_admet(drug_smiles, properties)
                
                if result:
                    st.success("ADMET Prediction Completed")
                    
                    # Store prediction results for AI analysis
                    st.session_state.prediction_results['ADMET'] = result
                    
                    if result.get('properties'):
                        st.subheader("ADMET Analysis Results")
                        
                        # Create comprehensive ADMET results table
                        admet_data = []
                        property_descriptions = {
                            'absorption': 'How well the drug is absorbed into the bloodstream',
                            'distribution': 'How the drug spreads throughout the body',
                            'metabolism': 'How quickly the drug is broken down',
                            'excretion': 'How efficiently the drug is eliminated',
                            'toxicity': 'Potential harmful effects (lower is better)',
                            'ld50': 'Lethal dose for 50% of test subjects (mg/kg)',
                            'logp': 'Fat solubility measure (affects distribution)',
                            'solubility': 'Water solubility (affects absorption)',
                            'bioavailability': 'Percentage that reaches circulation',
                            'clearance': 'Rate of drug elimination from body'
                        }
                        
                        safety_ranges = {
                            'toxicity': {'low': 0.3, 'high': 0.7},
                            'ld50': {'low': 100, 'high': 1000},
                            'logp': {'low': -0.4, 'high': 5.6},
                            'solubility': {'low': 0.01, 'high': 1.0},
                            'bioavailability': {'low': 0.3, 'high': 1.0},
                            'absorption': {'low': 0.5, 'high': 1.0},
                            'distribution': {'low': 0.3, 'high': 1.0}
                        }
                        
                        for prop, value in result['properties'].items():
                            # Determine safety status
                            safety_status = "Unknown"
                            status_color = "🔵"
                            
                            if prop in safety_ranges:
                                ranges = safety_ranges[prop]
                                if isinstance(value, (int, float)):
                                    if prop == 'toxicity':  # Lower is better for toxicity
                                        if value < ranges['low']:
                                            safety_status = "Excellent"
                                            status_color = "🟢"
                                        elif value < ranges['high']:
                                            safety_status = "Acceptable"
                                            status_color = "🟡"
                                        else:
                                            safety_status = "Concerning"
                                            status_color = "🔴"
                                    else:  # Higher is better for others
                                        if value > ranges['high']:
                                            safety_status = "Excellent"
                                            status_color = "🟢"
                                        elif value > ranges['low']:
                                            safety_status = "Good"
                                            status_color = "🟡"
                                        else:
                                            safety_status = "Poor"
                                            status_color = "🔴"
                            
                            # Format value for display
                            if isinstance(value, float):
                                display_value = f"{value:.3f}"
                            elif isinstance(value, int):
                                display_value = str(value)
                            else:
                                display_value = str(value)
                            
                            admet_data.append({
                                "Property": prop.replace('_', ' ').title(),
                                "Value": display_value,
                                "Status": f"{status_color} {safety_status}",
                                "Description": property_descriptions.get(prop, "Drug property measurement")
                            })
                        
                        if admet_data:
                            import pandas as pd
                            df = pd.DataFrame(admet_data)
                            
                            st.dataframe(
                                df,
                                use_container_width=True,
                                hide_index=True,
                                column_config={
                                    "Property": st.column_config.TextColumn(
                                        "ADMET Property",
                                        help="Pharmacokinetic parameter",
                                        width="medium"
                                    ),
                                    "Value": st.column_config.TextColumn(
                                        "Predicted Value",
                                        help="Model prediction result",
                                        width="small"
                                    ),
                                    "Status": st.column_config.TextColumn(
                                        "Safety Assessment",
                                        help="Clinical interpretation",
                                        width="medium"
                                    ),
                                    "Description": st.column_config.TextColumn(
                                        "What This Means",
                                        help="Plain language explanation",
                                        width="large"
                                    )
                                }
                            )
                            
                            # Summary insights
                            st.subheader("Clinical Insights")
                            
                            excellent_count = sum(1 for item in admet_data if "Excellent" in item["Status"])
                            concerning_count = sum(1 for item in admet_data if "Concerning" in item["Status"])
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Excellent Properties", excellent_count)
                            with col2:
                                st.metric("Total Analyzed", len(admet_data))
                            with col3:
                                st.metric("Concerning Properties", concerning_count)
                            
                            if concerning_count > 0:
                                st.warning("Some properties may require optimization before clinical use.")
                            elif excellent_count >= len(admet_data) // 2:
                                st.success("Overall favorable pharmacokinetic profile.")
                            else:
                                st.info("Mixed pharmacokinetic profile - further evaluation recommended.")
                else:
                    st.error("Prediction failed. Please ensure a model is loaded.")
            
            except Exception as e:
                st.error(f"Prediction error: {str(e)}")

def render_similarity_interface():
    """Render molecular similarity interface"""
    st.header("🔍 Molecular Similarity Search")
    st.info("Find structurally similar compounds using molecular fingerprints")
    
    col1, col2 = st.columns(2)
    
    with col1:
        query_smiles = st.text_area("Query SMILES", height=100, key="sim_query_smiles")
    
    with col2:
        threshold = st.slider("Similarity Threshold", 0.0, 1.0, 0.7, 0.05)
        method = st.selectbox("Similarity Method", ["Tanimoto", "Dice", "Cosine", "Euclidean", "Jaccard"])
        max_results = st.number_input("Max Results", 1, 50, 10)
    
    if st.button("Search Similar Compounds", type="primary", disabled=not query_smiles):
        with st.spinner("Searching for similar compounds..."):
            try:
                result = st.session_state.prediction_tasks.predict_similarity(
                    query_smiles, threshold, method, max_results
                )
                
                if result:
                    st.success("Similarity Search Completed")
                    
                    # Store prediction results for AI analysis
                    st.session_state.prediction_results['Similarity'] = result
                    
                    if result.get('similar_compounds'):
                        st.subheader("Similar Compounds Found")
                        
                        for i, compound in enumerate(result['similar_compounds']):
                            with st.expander(f"Compound {i+1} - Similarity: {compound.get('similarity', 0):.3f}"):
                                st.code(compound.get('smiles', ''))
                                if compound.get('name'):
                                    st.write(f"**Name:** {compound['name']}")
                    else:
                        st.warning("No similar compounds found above the threshold.")
                else:
                    st.error("Search failed. Please ensure a model is loaded.")
            
            except Exception as e:
                st.error(f"Search error: {str(e)}")

def render_ai_analysis_section():
    """Render AI-powered analysis section for prediction results"""
    st.markdown("### 🤖 AI-Powered Analysis")
    
    # Check agent status
    agent_status = agent_manager.get_agent_status()
    
    if not agent_status.get('enabled', False):
        st.info("AI analysis requires Google AI API key configuration. Once enabled, get intelligent insights about your prediction results.")
        return
    
    st.success("AI Analysis Available")
    
    # Get the current prediction results
    current_results = st.session_state.prediction_results
    task_type = st.session_state.current_task
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Analysis options
        analysis_type = st.selectbox(
            "Choose Analysis Type:",
            [
                "Explain Results",
                "Clinical Interpretation", 
                "Optimization Suggestions",
                "Safety Assessment",
                "Ask Custom Question"
            ],
            key="analysis_type"
        )
        
        if analysis_type == "Ask Custom Question":
            user_question = st.text_area(
                "Ask about your results:",
                placeholder="e.g., 'How can I improve the bioavailability of this compound?'",
                height=80,
                key="custom_analysis_question"
            )
        else:
            user_question = None
    
    with col2:
        st.markdown("**Available Data:**")
        if current_results:
            for task, results in current_results.items():
                st.write(f"• {task}: {len(results) if isinstance(results, list) else 1} results")
        else:
            st.write("No prediction results available")
    
    # Analysis button
    analyze_button = st.button(
        f"🔍 Get AI {analysis_type}",
        disabled=not current_results or (analysis_type == "Ask Custom Question" and not user_question),
        type="primary",
        use_container_width=True
    )
    
    if analyze_button:
        with st.spinner("AI is analyzing your results..."):
            import asyncio
            
            try:
                # Prepare analysis request
                if analysis_type == "Ask Custom Question":
                    analysis_prompt = user_question
                else:
                    analysis_prompt = f"Provide {analysis_type.lower()} for these {task_type} prediction results"
                
                # Run AI analysis
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                if analysis_type in ["Explain Results", "Ask Custom Question"]:
                    response = loop.run_until_complete(
                        agent_manager.explain_results(task_type, current_results)
                    )
                else:
                    response = loop.run_until_complete(
                        agent_manager.process_drug_query(
                            analysis_prompt, 
                            {"prediction_results": current_results, "task_type": task_type}
                        )
                    )
                    response = response.get('response', 'No analysis generated')
                
                loop.close()
                
                # Store analysis results
                if 'ai_analysis_history' not in st.session_state:
                    st.session_state.ai_analysis_history = []
                
                st.session_state.ai_analysis_history.append({
                    "type": analysis_type,
                    "question": user_question if analysis_type == "Ask Custom Question" else analysis_type,
                    "results": response,
                    "task": task_type,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Set flag to show results in separate container to avoid clearing prediction display
                st.session_state.show_results_after_analysis = True
                
            except Exception as e:
                st.error(f"Analysis error: {str(e)}")
    
    # Display analysis history
    if hasattr(st.session_state, 'ai_analysis_history') and st.session_state.ai_analysis_history:
        st.markdown("### 📊 Analysis Results")
        
        # Show the most recent analysis immediately if flag is set
        if st.session_state.show_results_after_analysis:
            latest_analysis = st.session_state.ai_analysis_history[-1]
            st.success("AI Analysis completed!")
            
            with st.container():
                st.markdown(f"**Analysis Type:** {latest_analysis['type']}")
                if latest_analysis['question'] != latest_analysis['type']:
                    st.markdown(f"**Question:** {latest_analysis['question']}")
                st.markdown(f"**AI Response:**")
                st.write(latest_analysis['results'])
                st.caption(f"Task: {latest_analysis['task']} | Generated: {latest_analysis['timestamp']}")
            
            # Reset the flag
            st.session_state.show_results_after_analysis = False
        
        # Show expandable history of all analyses
        with st.expander(f"Analysis History ({len(st.session_state.ai_analysis_history)} total)", expanded=False):
            for i, analysis in enumerate(reversed(st.session_state.ai_analysis_history)):
                st.markdown(f"**{i+1}. {analysis['type']}:** {analysis['question'][:100]}...")
                st.write(analysis['results'][:200] + "..." if len(analysis['results']) > 200 else analysis['results'])
                st.caption(f"Task: {analysis['task']} | Time: {analysis['timestamp']}")
                if i < len(st.session_state.ai_analysis_history) - 1:
                    st.divider()
        
        # Clear analysis history
        if st.button("🗑️ Clear Analysis History"):
            st.session_state.ai_analysis_history = []
            st.session_state.show_results_after_analysis = False
            st.success("Analysis history cleared")

def main():
    """Main application function"""
    render_top_bar()
    render_sidebar()
    
    st.divider()
    
    # Main content based on selected task
    if st.session_state.current_task == "DTI":
        render_dti_interface()
    elif st.session_state.current_task == "DTA":
        render_dta_interface()
    elif st.session_state.current_task == "DDI":
        render_ddi_interface()
    elif st.session_state.current_task == "ADMET":
        render_admet_interface()
    elif st.session_state.current_task == "Similarity":
        render_similarity_interface()
    

    
    # AI Assistant - Contextual Analysis Section
    if st.session_state.prediction_results:
        st.divider()
        render_ai_analysis_section()
    
    # Footer
    st.divider()
    st.caption("PharmQAgentAI - Therapeutic Intelligence Platform | Backend/Frontend Architecture")

if __name__ == "__main__":
    main()