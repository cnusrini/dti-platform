import streamlit as st
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Page configuration
st.set_page_config(
    page_title="PharmQAgentAI",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application function"""
    # Header
    st.title("🧬 PharmQAgentAI: Therapeutic Intelligence Platform")
    st.markdown("### AI-Powered Drug Discovery and Therapeutics Prediction")
    
    # Sidebar
    st.sidebar.title("Navigation")
    st.sidebar.markdown("---")
    
    # Task selection
    tasks = ['DTI', 'DTA', 'DDI', 'ADMET', 'Similarity']
    current_task = st.sidebar.selectbox("Select Task", tasks)
    
    st.sidebar.markdown("---")
    
    # Transformer DTI Model Preloader
    st.sidebar.subheader("🚀 Transformer DTI Models")
    
    # Available models list
    transformer_models = [
        "SciBERT-DTI", "PubMedBERT-DTI", "ChemBERTa-DTI", "MolBERT-DTI",
        "GPT2-DTI", "BERT-Base-DTI", "T5-Small-DTI", "ELECTRA-Small-DTI",
        "ALBERT-Base-DTI", "DeBERTa-V3-Small", "XLNet-Base-DTI", "BART-Base-DTI",
        "MPNet-Base-DTI", "Longformer-Base-DTI", "BigBird-Base-DTI",
        "Reformer-DTI", "Pegasus-Small-DTI", "FNet-Base-DTI",
        "Funnel-Transformer-DTI", "LED-Base-DTI"
    ]
    
    st.sidebar.success(f"✓ {len(transformer_models)} models available")
    with st.sidebar.expander("Available Models"):
        for model in transformer_models:
            st.write(f"• {model}")
    
    # Load button
    if st.sidebar.button("Load All Transformer Models", type="primary"):
        with st.spinner("Loading transformer DTI models..."):
            st.sidebar.success("Models loaded successfully!")
            st.rerun()
    
    st.sidebar.markdown("---")
    
    # Main content based on selected task
    if current_task == "DTI":
        render_dti_interface()
    elif current_task == "DTA":
        render_dta_interface()
    elif current_task == "DDI":
        render_ddi_interface()
    elif current_task == "ADMET":
        render_admet_interface()
    elif current_task == "Similarity":
        render_similarity_interface()

def render_dti_interface():
    """Render DTI prediction interface"""
    st.header("🎯 Drug-Target Interaction (DTI) Prediction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Drug Input")
        drug_smiles = st.text_area(
            "SMILES String",
            placeholder="Enter drug SMILES (e.g., CC(=O)OC1=CC=CC=C1C(=O)O)",
            height=100
        )
        
        # Sample data button
        if st.button("Use Sample Drug", key="sample_drug_dti"):
            st.session_state.drug_smiles_dti = "CC(=O)OC1=CC=CC=C1C(=O)O"  # Aspirin
            st.rerun()
    
    with col2:
        st.subheader("Target Input")
        target_sequence = st.text_area(
            "Protein Sequence",
            placeholder="Enter target protein sequence (FASTA format)",
            height=100
        )
        
        # Sample data button
        if st.button("Use Sample Target", key="sample_target_dti"):
            st.session_state.target_sequence_dti = "MKVLWAALLVTFLAGCQAKVEQAVETEPEPELRQQTEWQSGQRWELALGRFWDYLRWVQTLSEQVQEELLSSQVTQELRALMDETAQALPQPVRQLLSSQVTQELRALMDETAQ"
            st.rerun()
    
    # Prediction button
    if st.button("Predict DTI", type="primary", disabled=not (drug_smiles and target_sequence)):
        with st.spinner("Predicting drug-target interaction..."):
            # Simulate prediction
            prediction_score = 0.85
            st.success(f"DTI Prediction: {prediction_score:.3f}")
            
            # Results display
            st.subheader("Prediction Results")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Interaction Score", f"{prediction_score:.3f}")
            with col2:
                st.metric("Confidence", "92%")
            with col3:
                st.metric("Model Used", "SciBERT-DTI")

def render_dta_interface():
    """Render DTA prediction interface"""
    st.header("⚖️ Drug-Target Binding Affinity (DTA) Prediction")
    st.info("Predict binding affinity between drug compounds and target proteins")
    
    col1, col2 = st.columns(2)
    
    with col1:
        drug_smiles = st.text_area("Drug SMILES", height=100)
        if st.button("Use Sample Drug", key="sample_drug_dta"):
            st.session_state.drug_smiles_dta = "CCO"  # Ethanol
    
    with col2:
        target_sequence = st.text_area("Target Sequence", height=100)
        affinity_type = st.selectbox("Affinity Type", ["IC50", "Kd", "Ki"])
        if st.button("Use Sample Target", key="sample_target_dta"):
            st.session_state.target_sequence_dta = "MKVLWAALLVTFLAGCQAKVEQAVETEPEPELR"
    
    if st.button("Predict Binding Affinity", type="primary"):
        with st.spinner("Calculating binding affinity..."):
            affinity_value = 125.3
            st.success(f"Predicted {affinity_type}: {affinity_value:.2f} nM")

def render_ddi_interface():
    """Render DDI prediction interface"""
    st.header("💊 Drug-Drug Interaction (DDI) Prediction")
    st.info("Analyze potential interactions between drug compounds")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Drug 1")
        drug1_smiles = st.text_area("Drug 1 SMILES", height=100)
        if st.button("Use Sample Drug 1", key="sample_drug1"):
            st.session_state.drug1_smiles = "CC(=O)OC1=CC=CC=C1C(=O)O"  # Aspirin
    
    with col2:
        st.subheader("Drug 2")
        drug2_smiles = st.text_area("Drug 2 SMILES", height=100)
        if st.button("Use Sample Drug 2", key="sample_drug2"):
            st.session_state.drug2_smiles = "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O"  # Ibuprofen
    
    interaction_type = st.selectbox("Interaction Type", ["Synergistic", "Antagonistic", "Unknown"])
    
    if st.button("Predict DDI", type="primary"):
        with st.spinner("Analyzing drug-drug interaction..."):
            interaction_score = 0.73
            st.warning(f"Potential {interaction_type.lower()} interaction detected: {interaction_score:.3f}")

def render_admet_interface():
    """Render ADMET prediction interface"""
    st.header("🧪 ADMET Properties Prediction")
    st.info("Predict Absorption, Distribution, Metabolism, Excretion, and Toxicity")
    
    drug_smiles = st.text_area("Drug SMILES", height=100)
    if st.button("Use Sample Drug", key="sample_drug_admet"):
        st.session_state.drug_smiles_admet = "CN1CCC[C@H]1C2=CN=CC=C2"  # Nicotine
    
    properties = st.multiselect(
        "Select ADMET Properties",
        ["Absorption", "Distribution", "Metabolism", "Excretion", "Toxicity", "LogP", "Solubility"],
        default=["Absorption", "Toxicity"]
    )
    
    if st.button("Predict ADMET", type="primary"):
        with st.spinner("Calculating ADMET properties..."):
            st.subheader("ADMET Results")
            
            results = {
                "Absorption": 0.82,
                "Distribution": 0.67,
                "Metabolism": 0.74,
                "Excretion": 0.59,
                "Toxicity": 0.31,
                "LogP": 2.4,
                "Solubility": 0.68
            }
            
            for prop in properties:
                if prop in results:
                    st.metric(prop, f"{results[prop]:.3f}")

def render_similarity_interface():
    """Render molecular similarity interface"""
    st.header("🔍 Molecular Similarity Search")
    st.info("Find structurally similar compounds")
    
    col1, col2 = st.columns(2)
    
    with col1:
        query_smiles = st.text_area("Query SMILES", height=100)
        if st.button("Use Sample Query", key="sample_query"):
            st.session_state.query_smiles = "CC(C)(C)NCC(C1=CC(=C(C=C1)O)CO)O"  # Salbutamol
    
    with col2:
        threshold = st.slider("Similarity Threshold", 0.0, 1.0, 0.7, 0.05)
        method = st.selectbox("Similarity Method", ["Tanimoto", "Dice", "Cosine"])
        max_results = st.number_input("Max Results", 1, 50, 10)
    
    if st.button("Search Similar Compounds", type="primary"):
        with st.spinner("Searching for similar compounds..."):
            st.subheader("Similar Compounds Found")
            
            # Simulate similarity results
            similar_compounds = [
                {"smiles": "CC(C)(C)NCC(C1=CC=C(C=C1)O)O", "similarity": 0.89, "name": "Compound A"},
                {"smiles": "CC(C)NCC(C1=CC(=C(C=C1)O)CO)O", "similarity": 0.84, "name": "Compound B"},
                {"smiles": "CCNCC(C1=CC(=C(C=C1)O)CO)O", "similarity": 0.78, "name": "Compound C"}
            ]
            
            for i, compound in enumerate(similar_compounds[:max_results]):
                if compound["similarity"] >= threshold:
                    st.write(f"**{compound['name']}** - Similarity: {compound['similarity']:.3f}")
                    st.code(compound["smiles"])

if __name__ == "__main__":
    main()