import streamlit as st
import os
import sys
import traceback
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.model_manager import ModelManager
from models.prediction_tasks import PredictionTasks
from utils.molecular_utils import MolecularUtils
from utils.validation import ValidationUtils
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
        # Health indicator
        health_status = "🟢 Healthy" if len(st.session_state.loaded_models) > 0 else "🔴 No Models"
        st.metric("Status", health_status)
    
    with col3:
        # API Mode indicator
        st.metric("Mode", "Live")
    
    with col4:
        # Model count
        model_count = len(st.session_state.loaded_models)
        st.metric("Loaded Models", f"{model_count}/5")

def render_sidebar():
    """Render the sidebar with task selection and model management"""
    st.sidebar.header("Therapeutic Tasks")
    
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
                    st.sidebar.success(f"{selected_model} loaded successfully!")
                    st.rerun()
                else:
                    st.sidebar.error(f"Failed to load {selected_model}. The transformers library is required for model loading.")
                    st.sidebar.info("To enable model loading, please install the transformers package.")
                    
            except Exception as e:
                st.sidebar.error(f"Error loading model: {str(e)}")
                if "transformers" in str(e).lower():
                    st.sidebar.info("Model loading requires the transformers library to be installed.")
    else:
        st.sidebar.warning(f"No models available for {current_task}")
    
    st.sidebar.divider()
    
    # Sample Data section
    st.sidebar.subheader("📋 Sample Data")
    
    # Sample data for different tasks
    sample_data = {
        'DTI': {
            'drug_smiles': 'CC(=O)OC1=CC=CC=C1C(=O)O',  # Aspirin
            'target_sequence': 'MGSWAEFKQRLAAIGLLMLLKHLLLSLKKFGKLQFSLPSLLQLFCRQRLLPSLLPWLSSSLKVMLLKHL'
        },
        'DTA': {
            'drug_smiles': 'CN1C=NC2=C1C(=O)N(C(=O)N2C)C',  # Caffeine
            'target_sequence': 'MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR'
        },
        'DDI': {
            'drug1_smiles': 'CC(C)CC1=CC=C(C=C1)C(C)C(=O)O',  # Ibuprofen
            'drug2_smiles': 'CC(=O)OC1=CC=CC=C1C(=O)O'  # Aspirin
        },
        'ADMET': {
            'drug_smiles': 'CN1CCN(CC1)CCCC(C2=CC=CC=C2)C3=CC=CC=C3',  # Cetirizine-like
        },
        'Similarity': {
            'query_smiles': 'CCO'  # Ethanol
        }
    }
    
    if st.sidebar.button("🎯 Use Sample Data", use_container_width=True):
        current_samples = sample_data.get(st.session_state.current_task, {})
        
        # Store sample data in session state for the current task
        for key, value in current_samples.items():
            st.session_state[f"sample_{key}"] = value
        
        st.sidebar.success(f"Sample data loaded for {st.session_state.current_task}!")
        st.rerun()
    
    # Display current sample data
    if st.session_state.current_task in sample_data:
        with st.sidebar.expander("View Sample Data"):
            samples = sample_data[st.session_state.current_task]
            for key, value in samples.items():
                st.caption(f"**{key.replace('_', ' ').title()}:**")
                st.code(value[:50] + "..." if len(value) > 50 else value, language="text")
    
    st.sidebar.divider()
    
    # Settings section
    st.sidebar.subheader("Settings")
    
    # Smart mode toggle (placeholder for future feature)
    smart_mode = st.sidebar.toggle("Smart Mode", value=True, disabled=True)
    st.sidebar.caption("Automatically selects best model (Coming Soon)")
    
    # Reset all models
    if st.sidebar.button("Reset All Models", type="secondary", use_container_width=True):
        st.session_state.model_manager.unload_all_models()
        st.session_state.loaded_models.clear()
        st.session_state.prediction_results.clear()
        st.sidebar.success("All models unloaded!")
        st.rerun()
    
    # Display loaded models info
    if st.session_state.loaded_models:
        st.sidebar.subheader("Loaded Models")
        for model_key, model_info in st.session_state.loaded_models.items():
            with st.sidebar.expander(f"{model_info['task']}: {model_info['name']}"):
                st.write(f"**Task:** {model_info['task']}")
                st.write(f"**Loaded:** {model_info['loaded_at'].strftime('%H:%M:%S')}")
                if st.button(f"Unload", key=f"unload_{model_key}"):
                    st.session_state.model_manager.unload_model(model_info['task'], model_info['name'])
                    del st.session_state.loaded_models[model_key]
                    st.rerun()

def render_dti_interface():
    """Render DTI prediction interface"""
    st.header("Drug-Target Interaction Prediction")
    st.caption("Predict interaction probability between a compound and a protein target")
    
    col1, col2 = st.columns(2)
    
    with col1:
        drug_smiles = st.text_area(
            "Drug SMILES",
            value=st.session_state.get('sample_drug_smiles', ''),
            placeholder="Enter SMILES string (e.g., CCO for ethanol)",
            help="Simplified Molecular Input Line Entry System notation"
        )
        
        # File upload option
        uploaded_file = st.file_uploader(
            "Or upload SMILES file",
            type=['txt', 'smi'],
            help="Upload a file containing SMILES strings"
        )
        
        if uploaded_file:
            content = uploaded_file.read().decode('utf-8')
            drug_smiles = content.strip().split('\n')[0]  # Take first line
    
    with col2:
        target_sequence = st.text_area(
            "Target Protein Sequence",
            value=st.session_state.get('sample_target_sequence', ''),
            placeholder="Enter protein sequence in FASTA format",
            help="Amino acid sequence of the target protein"
        )
    
    # Prediction button
    predict_button = st.button("Predict DTI", type="primary", use_container_width=True)
    
    if predict_button:
        # Validation
        if not drug_smiles or not target_sequence:
            st.error("Please provide both drug SMILES and target sequence")
            return
        
        # Check if model is loaded
        model_key = f"DTI_{st.session_state.get('model_selector_DTI', '')}"
        if model_key not in st.session_state.loaded_models:
            st.error("Please load a DTI model first")
            return
        
        # Validate SMILES
        if not st.session_state.validation_utils.validate_smiles(drug_smiles):
            st.error("Invalid SMILES string provided")
            return
        
        # Validate protein sequence
        if not st.session_state.validation_utils.validate_protein_sequence(target_sequence):
            st.error("Invalid protein sequence provided")
            return
        
        # Make prediction
        with st.spinner("Making DTI prediction..."):
            try:
                result = st.session_state.prediction_tasks.predict_dti(
                    drug_smiles, target_sequence
                )
                
                if result:
                    st.session_state.prediction_results['DTI'] = result
                    st.success("Prediction completed successfully!")
                else:
                    st.error("Prediction failed. Please check your inputs and try again.")
            except Exception as e:
                st.error(f"Prediction error: {str(e)}")
                st.exception(e)

def render_dta_interface():
    """Render DTA prediction interface"""
    st.header("Drug-Target Binding Affinity Prediction")
    st.caption("Predict binding affinity (IC50/Kd/Ki) between drug and protein")
    
    col1, col2 = st.columns(2)
    
    with col1:
        drug_smiles = st.text_area(
            "Drug SMILES",
            value=st.session_state.get('sample_drug_smiles', ''),
            placeholder="Enter SMILES string",
            help="Simplified Molecular Input Line Entry System notation"
        )
        
        affinity_type = st.selectbox(
            "Affinity Type",
            ["IC50", "Kd", "Ki"],
            help="Type of binding affinity to predict"
        )
    
    with col2:
        target_sequence = st.text_area(
            "Target Protein Sequence",
            value=st.session_state.get('sample_target_sequence', ''),
            placeholder="Enter protein sequence",
            help="Amino acid sequence of the target protein"
        )
    
    predict_button = st.button("Predict Binding Affinity", type="primary", use_container_width=True)
    
    if predict_button:
        if not drug_smiles or not target_sequence:
            st.error("Please provide both drug SMILES and target sequence")
            return
        
        model_key = f"DTA_{st.session_state.get('model_selector_DTA', '')}"
        if model_key not in st.session_state.loaded_models:
            st.error("Please load a DTA model first")
            return
        
        if not st.session_state.validation_utils.validate_smiles(drug_smiles):
            st.error("Invalid SMILES string provided")
            return
        
        if not st.session_state.validation_utils.validate_protein_sequence(target_sequence):
            st.error("Invalid protein sequence provided")
            return
        
        with st.spinner("Predicting binding affinity..."):
            try:
                result = st.session_state.prediction_tasks.predict_dta(
                    drug_smiles, target_sequence, affinity_type
                )
                
                if result:
                    st.session_state.prediction_results['DTA'] = result
                    st.success("Prediction completed successfully!")
                else:
                    st.error("Prediction failed. Please check your inputs and try again.")
            except Exception as e:
                st.error(f"Prediction error: {str(e)}")

def render_ddi_interface():
    """Render DDI prediction interface"""
    st.header("Drug-Drug Interaction Prediction")
    st.caption("Predict synergistic or adverse interactions between drug pairs")
    
    col1, col2 = st.columns(2)
    
    with col1:
        drug1_smiles = st.text_area(
            "Drug 1 SMILES",
            value=st.session_state.get('sample_drug1_smiles', ''),
            placeholder="Enter SMILES for first drug",
            help="SMILES notation for the first drug"
        )
    
    with col2:
        drug2_smiles = st.text_area(
            "Drug 2 SMILES",
            value=st.session_state.get('sample_drug2_smiles', ''),
            placeholder="Enter SMILES for second drug",
            help="SMILES notation for the second drug"
        )
    
    interaction_type = st.selectbox(
        "Interaction Type",
        ["Synergistic", "Antagonistic", "Additive", "Unknown"],
        help="Type of interaction to analyze"
    )
    
    predict_button = st.button("Predict Drug Interaction", type="primary", use_container_width=True)
    
    if predict_button:
        if not drug1_smiles or not drug2_smiles:
            st.error("Please provide SMILES for both drugs")
            return
        
        model_key = f"DDI_{st.session_state.get('model_selector_DDI', '')}"
        if model_key not in st.session_state.loaded_models:
            st.error("Please load a DDI model first")
            return
        
        if not st.session_state.validation_utils.validate_smiles(drug1_smiles):
            st.error("Invalid SMILES string for Drug 1")
            return
        
        if not st.session_state.validation_utils.validate_smiles(drug2_smiles):
            st.error("Invalid SMILES string for Drug 2")
            return
        
        with st.spinner("Predicting drug interaction..."):
            try:
                result = st.session_state.prediction_tasks.predict_ddi(
                    drug1_smiles, drug2_smiles, interaction_type
                )
                
                if result:
                    st.session_state.prediction_results['DDI'] = result
                    st.success("Prediction completed successfully!")
                else:
                    st.error("Prediction failed. Please check your inputs and try again.")
            except Exception as e:
                st.error(f"Prediction error: {str(e)}")

def render_admet_interface():
    """Render ADMET prediction interface"""
    st.header("ADMET Properties Prediction")
    st.caption("Predict Absorption, Distribution, Metabolism, Excretion, and Toxicity")
    
    col1, col2 = st.columns(2)
    
    with col1:
        drug_smiles = st.text_area(
            "Drug SMILES",
            value=st.session_state.get('sample_drug_smiles', ''),
            placeholder="Enter SMILES string",
            help="SMILES notation for the compound"
        )
    
    with col2:
        admet_properties = st.multiselect(
            "ADMET Properties",
            ["Absorption", "Distribution", "Metabolism", "Excretion", "Toxicity", "LD50", "logP", "Solubility"],
            default=["Absorption", "Toxicity"],
            help="Select properties to predict"
        )
    
    predict_button = st.button("Predict ADMET", type="primary", use_container_width=True)
    
    if predict_button:
        if not drug_smiles:
            st.error("Please provide drug SMILES")
            return
        
        if not admet_properties:
            st.error("Please select at least one ADMET property")
            return
        
        model_key = f"ADMET_{st.session_state.get('model_selector_ADMET', '')}"
        if model_key not in st.session_state.loaded_models:
            st.error("Please load an ADMET model first")
            return
        
        if not st.session_state.validation_utils.validate_smiles(drug_smiles):
            st.error("Invalid SMILES string provided")
            return
        
        with st.spinner("Predicting ADMET properties..."):
            try:
                result = st.session_state.prediction_tasks.predict_admet(
                    drug_smiles, admet_properties
                )
                
                if result:
                    st.session_state.prediction_results['ADMET'] = result
                    st.success("Prediction completed successfully!")
                else:
                    st.error("Prediction failed. Please check your inputs and try again.")
            except Exception as e:
                st.error(f"Prediction error: {str(e)}")

def render_similarity_interface():
    """Render molecular similarity interface"""
    st.header("Molecular Similarity Search")
    st.caption("Find similar drugs based on structure or embeddings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        query_smiles = st.text_area(
            "Query SMILES",
            value=st.session_state.get('sample_query_smiles', ''),
            placeholder="Enter SMILES for query compound",
            help="SMILES notation for the query molecule"
        )
        
        similarity_threshold = st.slider(
            "Similarity Threshold",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.05,
            help="Minimum similarity score (Tanimoto coefficient)"
        )
    
    with col2:
        similarity_method = st.selectbox(
            "Similarity Method",
            ["Tanimoto", "Dice", "Cosine", "Euclidean"],
            help="Method for calculating molecular similarity"
        )
        
        max_results = st.number_input(
            "Max Results",
            min_value=1,
            max_value=100,
            value=10,
            help="Maximum number of similar compounds to return"
        )
    
    predict_button = st.button("Find Similar Compounds", type="primary", use_container_width=True)
    
    if predict_button:
        if not query_smiles:
            st.error("Please provide query SMILES")
            return
        
        model_key = f"Similarity_{st.session_state.get('model_selector_Similarity', '')}"
        if model_key not in st.session_state.loaded_models:
            st.error("Please load a Similarity model first")
            return
        
        if not st.session_state.validation_utils.validate_smiles(query_smiles):
            st.error("Invalid SMILES string provided")
            return
        
        with st.spinner("Searching for similar compounds..."):
            try:
                result = st.session_state.prediction_tasks.predict_similarity(
                    query_smiles, similarity_threshold, similarity_method, max_results
                )
                
                if result:
                    st.session_state.prediction_results['Similarity'] = result
                    st.success("Similarity search completed successfully!")
                else:
                    st.error("Similarity search failed. Please check your inputs and try again.")
            except Exception as e:
                st.error(f"Similarity search error: {str(e)}")

def render_prediction_results():
    """Render prediction results section"""
    current_task = st.session_state.current_task
    
    if current_task in st.session_state.prediction_results:
        result = st.session_state.prediction_results[current_task]
        
        st.divider()
        st.subheader("Prediction Results")
        
        # Results display
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Prediction Score",
                f"{result.get('score', 'N/A'):.4f}" if isinstance(result.get('score'), (int, float)) else result.get('score', 'N/A'),
                help="Main prediction value"
            )
        
        with col2:
            status = result.get('status', 'Unknown')
            status_color = "🟢" if status == "Success" else "🔴"
            st.metric("Status", f"{status_color} {status}")
        
        with col3:
            model_info = result.get('model_info', 'Unknown Model')
            st.metric("Model Used", model_info)
        
        # Additional result details
        if 'details' in result and result['details']:
            st.subheader("Detailed Results")
            
            if isinstance(result['details'], dict):
                for key, value in result['details'].items():
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.write(f"**{key}:**")
                    with col2:
                        if isinstance(value, (int, float)):
                            st.write(f"{value:.4f}")
                        else:
                            st.write(str(value))
            else:
                st.write(result['details'])
        
        # Confidence explanation
        if 'confidence' in result:
            with st.expander("Confidence Explanation"):
                st.write(f"**Confidence Score:** {result['confidence']:.4f}")
                if 'confidence_explanation' in result:
                    st.write(result['confidence_explanation'])
                else:
                    st.write("High confidence indicates reliable prediction based on training data similarity.")
        
        # Clear results button
        if st.button("Clear Results", type="secondary"):
            if current_task in st.session_state.prediction_results:
                del st.session_state.prediction_results[current_task]
            st.rerun()

def main():
    """Main application function"""
    try:
        # Render top bar
        render_top_bar()
        
        # Create layout
        render_sidebar()
        
        # Main content area
        st.divider()
        
        # Render task-specific interface
        current_task = st.session_state.current_task
        
        if current_task == 'DTI':
            render_dti_interface()
        elif current_task == 'DTA':
            render_dta_interface()
        elif current_task == 'DDI':
            render_ddi_interface()
        elif current_task == 'ADMET':
            render_admet_interface()
        elif current_task == 'Similarity':
            render_similarity_interface()
        
        # Render prediction results if available
        render_prediction_results()
        
        # Footer
        st.divider()
        st.caption("PharmQAgentAI - Therapeutic Intelligence Platform | Powered by Hugging Face Models")
        
    except Exception as e:
        st.error("An unexpected error occurred in the application")
        st.exception(e)
        
        # Emergency reset button
        if st.button("Reset Application", type="primary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

if __name__ == "__main__":
    main()
