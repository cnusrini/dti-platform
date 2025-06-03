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

# Page configuration
st.set_page_config(
    page_title="PharmQAgentAI",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

def render_top_bar():
    """Render the top navigation bar"""
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    
    with col1:
        st.title("🧬 PharmQAgentAI")
        st.caption("Therapeutic Intelligence Platform")
    
    with col2:
        if st.session_state.model_manager:
            loaded_count = len(st.session_state.model_manager.get_loaded_models())
            st.metric("Loaded Models", loaded_count)
    
    with col3:
        st.metric("Architecture", "Backend/Frontend")
    
    with col4:
        if st.session_state.loaded_models:
            st.success("🟢 Ready")
        else:
            st.warning("🟡 Standby")

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
    
    # Cleanup models
    st.sidebar.divider()
    if st.sidebar.button("Unload All Models", type="secondary"):
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
        
        if st.button("Use Sample Drug", key="sample_drug_dti"):
            st.session_state.dti_drug_smiles = "CC(=O)OC1=CC=CC=C1C(=O)O"  # Aspirin
            st.rerun()
    
    with col2:
        st.subheader("Target Input")
        target_sequence = st.text_area(
            "Protein Sequence",
            value=default_target,
            placeholder="Enter target protein sequence (FASTA format)",
            height=100,
            key="dti_target_input"
        )
        
        if st.button("Use Sample Target", key="sample_target_dti"):
            st.session_state.dti_target_sequence = "MKVLWAALLVTFLAGCQAKVEQAVETEPEPELRQQTEWQSGQRWELALGRFWDYLRWVQTLSEQVQEELLSSQVTQELRALMDETAQ"
            st.rerun()
    
    # Prediction
    if st.button("Predict DTI", type="primary", disabled=not (drug_smiles and target_sequence)):
        with st.spinner("Predicting drug-target interaction..."):
            try:
                result = st.session_state.prediction_tasks.predict_dti(drug_smiles, target_sequence)
                
                if result:
                    st.success("DTI Prediction Completed")
                    
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
                    
                    # Additional details
                    if result.get('details'):
                        st.subheader("Detailed Results")
                        st.json(result['details'])
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
        if st.button("Use Sample Drug", key="sample_drug_dta"):
            st.session_state.dta_drug_smiles = "CCO"  # Ethanol
            st.rerun()
    
    with col2:
        target_sequence = st.text_area("Target Sequence", height=100, key="dta_target_sequence")
        affinity_type = st.selectbox("Affinity Type", ["IC50", "Kd", "Ki"])
        if st.button("Use Sample Target", key="sample_target_dta"):
            st.session_state.dta_target_sequence = "MKVLWAALLVTFLAGCQAKVEQAVETEPEPELR"
            st.rerun()
    
    if st.button("Predict Binding Affinity", type="primary", disabled=not (drug_smiles and target_sequence)):
        with st.spinner("Calculating binding affinity..."):
            try:
                result = st.session_state.prediction_tasks.predict_dta(drug_smiles, target_sequence, affinity_type)
                
                if result:
                    st.success("DTA Prediction Completed")
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
        if st.button("Use Sample Drug 1", key="sample_drug1_ddi"):
            st.session_state.ddi_drug1_smiles = "CC(=O)OC1=CC=CC=C1C(=O)O"  # Aspirin
            st.rerun()
    
    with col2:
        st.subheader("Drug 2")
        drug2_smiles = st.text_area("Drug 2 SMILES", height=100, key="ddi_drug2_smiles")
        if st.button("Use Sample Drug 2", key="sample_drug2_ddi"):
            st.session_state.ddi_drug2_smiles = "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O"  # Ibuprofen
            st.rerun()
    
    interaction_type = st.selectbox("Interaction Type", ["Synergistic", "Antagonistic", "Unknown"])
    
    if st.button("Predict DDI", type="primary", disabled=not (drug1_smiles and drug2_smiles)):
        with st.spinner("Analyzing drug-drug interaction..."):
            try:
                result = st.session_state.prediction_tasks.predict_ddi(drug1_smiles, drug2_smiles, interaction_type)
                
                if result:
                    st.success("DDI Prediction Completed")
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
    if st.button("Use Sample Drug", key="sample_drug_admet"):
        st.session_state.admet_drug_smiles = "CN1CCC[C@H]1C2=CN=CC=C2"  # Nicotine
        st.rerun()
    
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
                    
                    if result.get('properties'):
                        st.subheader("ADMET Results")
                        
                        # Display results in columns
                        cols = st.columns(3)
                        for i, (prop, value) in enumerate(result['properties'].items()):
                            with cols[i % 3]:
                                if isinstance(value, (int, float)):
                                    st.metric(prop.title(), f"{value:.3f}")
                                else:
                                    st.metric(prop.title(), str(value))
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
        if st.button("Use Sample Query", key="sample_query_sim"):
            st.session_state.sim_query_smiles = "CC(C)(C)NCC(C1=CC(=C(C=C1)O)CO)O"  # Salbutamol
            st.rerun()
    
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
    
    # Footer
    st.divider()
    st.caption("PharmQAgentAI - Therapeutic Intelligence Platform | Backend/Frontend Architecture")

if __name__ == "__main__":
    main()