"""
Streamlit Frontend for PharmQAgentAI
Therapeutic Intelligence Platform UI
"""

import streamlit as st
import requests
import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Any

# Configuration
API_BASE_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="PharmQAgentAI",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1e3c72;
    }
    .model-status {
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.2rem 0;
    }
    .status-success {
        background-color: #d4edda;
        color: #155724;
    }
    .status-error {
        background-color: #f8d7da;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'api_status' not in st.session_state:
    st.session_state.api_status = False
if 'loaded_models' not in st.session_state:
    st.session_state.loaded_models = {}
if 'prediction_results' not in st.session_state:
    st.session_state.prediction_results = {}
if 'current_task' not in st.session_state:
    st.session_state.current_task = 'DTI'

def check_api_connection():
    """Check if the FastAPI backend is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            st.session_state.api_status = True
            return True
    except requests.exceptions.RequestException:
        st.session_state.api_status = False
    return False

def get_available_models(task=None):
    """Get available models from the API"""
    try:
        url = f"{API_BASE_URL}/models/available"
        if task:
            url += f"?task={task}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['data']
    except requests.exceptions.RequestException:
        pass
    return {}

def load_model(task, model_name):
    """Load a model via the API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/models/load",
            json={"task": task, "model_name": model_name}
        )
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def preload_transformer_models():
    """Preload all transformer models via the API"""
    try:
        response = requests.post(f"{API_BASE_URL}/models/preload-transformers")
        if response.status_code == 200:
            return response.json()['results']
    except requests.exceptions.RequestException:
        pass
    return None

def make_prediction(endpoint, data):
    """Make a prediction via the API"""
    try:
        response = requests.post(f"{API_BASE_URL}/predict/{endpoint}", json=data)
        if response.status_code == 200:
            return response.json()['prediction']
        else:
            st.error(f"Prediction failed: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"API connection error: {str(e)}")
    return None

def render_header():
    """Render the main header"""
    st.markdown("""
    <div class="main-header">
        <h1 style="color: white; margin: 0;">🧬 PharmQAgentAI</h1>
        <p style="color: #e0e0e0; margin: 0;">Therapeutic Intelligence Platform with 20 Transformer Models</p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar with API status and model management"""
    st.sidebar.title("🔧 System Control")
    
    # API Status
    api_connected = check_api_connection()
    if api_connected:
        st.sidebar.success("✅ API Connected")
    else:
        st.sidebar.error("❌ API Disconnected")
        st.sidebar.warning("Please start the FastAPI backend server")
        return
    
    st.sidebar.divider()
    
    # Task Selection
    st.sidebar.subheader("📋 Task Selection")
    tasks = ['DTI', 'DTA', 'DDI', 'ADMET', 'Similarity']
    current_task = st.sidebar.selectbox(
        "Choose Task",
        tasks,
        index=tasks.index(st.session_state.current_task)
    )
    
    if current_task != st.session_state.current_task:
        st.session_state.current_task = current_task
        st.rerun()
    
    st.sidebar.divider()
    
    # Transformer Model Preloader
    st.sidebar.subheader("🚀 Transformer Models")
    
    transformer_models = [
        "SciBERT-DTI", "PubMedBERT-DTI", "ChemBERTa-DTI", "MolBERT-DTI",
        "GPT2-DTI", "BERT-Base-DTI", "T5-Small-DTI", "ELECTRA-Small-DTI",
        "ALBERT-Base-DTI", "DeBERTa-V3-Small", "XLNet-Base-DTI", "BART-Base-DTI",
        "MPNet-Base-DTI", "Longformer-Base-DTI", "BigBird-Base-DTI",
        "Reformer-DTI", "Pegasus-Small-DTI", "FNet-Base-DTI",
        "Funnel-Transformer-DTI", "LED-Base-DTI"
    ]
    
    st.sidebar.info(f"Available: {len(transformer_models)} models")
    
    with st.sidebar.expander("View All Models"):
        for model in transformer_models:
            st.write(f"• {model}")
    
    if st.sidebar.button("Load All Transformer Models", type="primary"):
        with st.spinner("Loading transformer models..."):
            results = preload_transformer_models()
            if results:
                st.sidebar.success(f"Loaded {results.get('loaded_successfully', 0)} models")
                if results.get('failed_models'):
                    st.sidebar.warning(f"Failed: {len(results['failed_models'])} models")
            else:
                st.sidebar.error("Failed to load models")
    
    st.sidebar.divider()
    
    # Model Management for Current Task
    st.sidebar.subheader(f"🎯 {current_task} Models")
    
    available_models = get_available_models(current_task)
    if available_models and 'models' in available_models:
        model_list = list(available_models['models'].keys())
        selected_model = st.sidebar.selectbox("Select Model", model_list)
        
        if st.sidebar.button(f"Load {selected_model}"):
            if load_model(current_task, selected_model):
                st.sidebar.success(f"Loaded {selected_model}")
            else:
                st.sidebar.error(f"Failed to load {selected_model}")

def render_dti_interface():
    """Render DTI prediction interface"""
    st.header("🎯 Drug-Target Interaction (DTI) Prediction")
    st.info("Predict interaction probability between drug compounds and target proteins")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Drug Input")
        drug_smiles = st.text_area(
            "SMILES String",
            placeholder="Enter drug SMILES (e.g., CC(=O)OC1=CC=CC=C1C(=O)O)",
            height=100,
            key="dti_drug_smiles"
        )
        
        if st.button("Use Sample Drug", key="sample_drug_dti"):
            st.session_state.dti_drug_smiles = "CC(=O)OC1=CC=CC=C1C(=O)O"
            st.rerun()
    
    with col2:
        st.subheader("Target Input")
        target_sequence = st.text_area(
            "Protein Sequence",
            placeholder="Enter target protein sequence",
            height=100,
            key="dti_target_sequence"
        )
        
        if st.button("Use Sample Target", key="sample_target_dti"):
            st.session_state.dti_target_sequence = "MKVLWAALLVTFLAGCQAKVEQAVETEPEPELRQQTEWQSGQRWELALGRFWDYLRWVQTLSEQVQEELLSSQVTQELRALMDETAQ"
            st.rerun()
    
    # Model selection
    model_name = st.selectbox("Select DTI Model", ["SciBERT-DTI", "PubMedBERT-DTI", "ChemBERTa-DTI"])
    
    # Prediction
    if st.button("Predict DTI", type="primary", disabled=not (drug_smiles and target_sequence)):
        with st.spinner("Predicting drug-target interaction..."):
            result = make_prediction("dti", {
                "drug_smiles": drug_smiles,
                "target_sequence": target_sequence,
                "model_name": model_name
            })
            
            if result:
                st.success("DTI Prediction Completed")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Interaction Score", f"{result.get('score', 0):.3f}")
                with col2:
                    st.metric("Confidence", f"{result.get('confidence', 0)*100:.1f}%" if result.get('confidence') else "N/A")
                with col3:
                    st.metric("Model Used", result.get('model_info', model_name))
                
                if result.get('details'):
                    st.json(result['details'])

def render_dta_interface():
    """Render DTA prediction interface"""
    st.header("⚖️ Drug-Target Binding Affinity (DTA) Prediction")
    st.info("Predict binding affinity between drug compounds and target proteins")
    
    col1, col2 = st.columns(2)
    
    with col1:
        drug_smiles = st.text_area("Drug SMILES", height=100, key="dta_drug_smiles")
        if st.button("Use Sample Drug", key="sample_drug_dta"):
            st.session_state.dta_drug_smiles = "CCO"
            st.rerun()
    
    with col2:
        target_sequence = st.text_area("Target Sequence", height=100, key="dta_target_sequence")
        affinity_type = st.selectbox("Affinity Type", ["IC50", "Kd", "Ki"])
        if st.button("Use Sample Target", key="sample_target_dta"):
            st.session_state.dta_target_sequence = "MKVLWAALLVTFLAGCQAKVEQAVETEPEPELR"
            st.rerun()
    
    if st.button("Predict Binding Affinity", type="primary"):
        with st.spinner("Calculating binding affinity..."):
            result = make_prediction("dta", {
                "drug_smiles": drug_smiles,
                "target_sequence": target_sequence,
                "affinity_type": affinity_type
            })
            
            if result:
                st.success("DTA Prediction Completed")
                st.metric(f"Predicted {affinity_type}", f"{result.get('score', 0):.2f} nM")

def render_ddi_interface():
    """Render DDI prediction interface"""
    st.header("💊 Drug-Drug Interaction (DDI) Prediction")
    st.info("Analyze potential interactions between drug compounds")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Drug 1")
        drug1_smiles = st.text_area("Drug 1 SMILES", height=100, key="ddi_drug1_smiles")
        if st.button("Use Sample Drug 1", key="sample_drug1_ddi"):
            st.session_state.ddi_drug1_smiles = "CC(=O)OC1=CC=CC=C1C(=O)O"
            st.rerun()
    
    with col2:
        st.subheader("Drug 2")
        drug2_smiles = st.text_area("Drug 2 SMILES", height=100, key="ddi_drug2_smiles")
        if st.button("Use Sample Drug 2", key="sample_drug2_ddi"):
            st.session_state.ddi_drug2_smiles = "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O"
            st.rerun()
    
    interaction_type = st.selectbox("Interaction Type", ["Synergistic", "Antagonistic", "Unknown"])
    
    if st.button("Predict DDI", type="primary"):
        with st.spinner("Analyzing drug-drug interaction..."):
            result = make_prediction("ddi", {
                "drug1_smiles": drug1_smiles,
                "drug2_smiles": drug2_smiles,
                "interaction_type": interaction_type
            })
            
            if result:
                st.success("DDI Prediction Completed")
                st.metric("Interaction Score", f"{result.get('score', 0):.3f}")

def render_admet_interface():
    """Render ADMET prediction interface"""
    st.header("🧪 ADMET Properties Prediction")
    st.info("Predict Absorption, Distribution, Metabolism, Excretion, and Toxicity")
    
    drug_smiles = st.text_area("Drug SMILES", height=100, key="admet_drug_smiles")
    if st.button("Use Sample Drug", key="sample_drug_admet"):
        st.session_state.admet_drug_smiles = "CN1CCC[C@H]1C2=CN=CC=C2"
        st.rerun()
    
    properties = st.multiselect(
        "Select ADMET Properties",
        ["absorption", "distribution", "metabolism", "excretion", "toxicity", "logp", "solubility"],
        default=["absorption", "toxicity"]
    )
    
    if st.button("Predict ADMET", type="primary"):
        with st.spinner("Calculating ADMET properties..."):
            result = make_prediction("admet", {
                "drug_smiles": drug_smiles,
                "properties": properties
            })
            
            if result:
                st.success("ADMET Prediction Completed")
                if result.get('properties'):
                    for prop, value in result['properties'].items():
                        st.metric(prop.title(), f"{value:.3f}" if isinstance(value, float) else str(value))

def render_similarity_interface():
    """Render molecular similarity interface"""
    st.header("🔍 Molecular Similarity Search")
    st.info("Find structurally similar compounds")
    
    col1, col2 = st.columns(2)
    
    with col1:
        query_smiles = st.text_area("Query SMILES", height=100, key="sim_query_smiles")
        if st.button("Use Sample Query", key="sample_query_sim"):
            st.session_state.sim_query_smiles = "CC(C)(C)NCC(C1=CC(=C(C=C1)O)CO)O"
            st.rerun()
    
    with col2:
        threshold = st.slider("Similarity Threshold", 0.0, 1.0, 0.7, 0.05)
        method = st.selectbox("Similarity Method", ["Tanimoto", "Dice", "Cosine"])
        max_results = st.number_input("Max Results", 1, 50, 10)
    
    if st.button("Search Similar Compounds", type="primary"):
        with st.spinner("Searching for similar compounds..."):
            result = make_prediction("similarity", {
                "query_smiles": query_smiles,
                "threshold": threshold,
                "method": method,
                "max_results": max_results
            })
            
            if result:
                st.success("Similarity Search Completed")
                if result.get('similar_compounds'):
                    for compound in result['similar_compounds']:
                        st.write(f"**Similarity: {compound.get('similarity', 0):.3f}**")
                        st.code(compound.get('smiles', ''))

def main():
    """Main application function"""
    render_header()
    render_sidebar()
    
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

if __name__ == "__main__":
    main()