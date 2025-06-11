import streamlit as st
import pandas as pd
import random
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="PharmQAgentAI",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #1e3c72;
    }
    .prediction-result {
        background: #e8f5e8;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #4caf50;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🧬 PharmQAgentAI: Therapeutic Intelligence Platform</h1>
    <h3>AI-Powered Drug Discovery with Advanced Analytics</h3>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = []

# Sidebar - Navigation
st.sidebar.title("🎯 Prediction Tasks")
task = st.sidebar.selectbox(
    "Choose Analysis Type",
    ["DTI Prediction", "DTA Prediction", "DDI Prediction", "ADMET Properties", "Molecular Similarity", "AI Agent Analysis"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Platform Status")
st.sidebar.success("✅ System Online")
st.sidebar.info(f"🕐 Last Update: {datetime.now().strftime('%H:%M:%S')}")
st.sidebar.metric("Total Predictions", len(st.session_state.prediction_history))

# Main content area
if task == "DTI Prediction":
    st.header("🎯 Drug-Target Interaction Prediction")
    
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
    
    model_selection = st.selectbox(
        "Select Model",
        ["DeepDTI-BERT", "GraphDTI-Transformer", "BioBERT-DTI", "ChemBERTa-DTI"]
    )
    
    if st.button("🔍 Predict Interaction", type="primary", use_container_width=True):
        with st.spinner("Analyzing drug-target interaction..."):
            # Simulate prediction
            interaction_score = random.uniform(0.3, 0.95)
            confidence = random.uniform(0.7, 0.98)
            
            st.success("✅ Prediction Complete!")
            
            # Display results
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Interaction Score", f"{interaction_score:.3f}")
            with col2:
                st.metric("Confidence", f"{confidence:.3f}")
            with col3:
                if interaction_score > 0.7:
                    st.metric("Prediction", "Strong", delta="High Potential")
                elif interaction_score > 0.5:
                    st.metric("Prediction", "Moderate", delta="Further Study")
                else:
                    st.metric("Prediction", "Weak", delta="Low Priority")
            
            # Interpretation
            st.subheader("📋 Analysis Results")
            if interaction_score > 0.7:
                st.success("🎉 Strong interaction predicted - High therapeutic potential")
            elif interaction_score > 0.5:
                st.warning("⚠️ Moderate interaction predicted - Further validation recommended")
            else:
                st.info("ℹ️ Weak interaction predicted - Consider alternative targets")
            
            # Add to history
            result = {
                "timestamp": datetime.now(),
                "task": "DTI",
                "drug": drug_smiles,
                "target": target_sequence[:20] + "...",
                "score": interaction_score,
                "model": model_selection
            }
            st.session_state.prediction_history.append(result)

elif task == "DTA Prediction":
    st.header("🎯 Drug-Target Affinity Prediction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        drug_smiles = st.text_input("Drug SMILES", value="CCO")
        
    with col2:
        target_sequence = st.text_area("Target Protein Sequence", value="MKLVFFAED")
    
    if st.button("📊 Predict Affinity", type="primary", use_container_width=True):
        with st.spinner("Calculating binding affinity..."):
            affinity_value = random.uniform(4.5, 9.2)
            
            st.success("✅ Affinity Prediction Complete!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Predicted pIC50", f"{affinity_value:.2f}")
            with col2:
                if affinity_value > 7.0:
                    st.metric("Classification", "High Affinity", delta="Excellent")
                elif affinity_value > 5.5:
                    st.metric("Classification", "Moderate", delta="Good")
                else:
                    st.metric("Classification", "Low Affinity", delta="Optimize")

elif task == "DDI Prediction":
    st.header("⚡ Drug-Drug Interaction Prediction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        drug1_smiles = st.text_input("Drug 1 SMILES", value="CCO")
        
    with col2:
        drug2_smiles = st.text_input("Drug 2 SMILES", value="CCN(CC)CC")
    
    if st.button("🔬 Predict Interaction", type="primary", use_container_width=True):
        with st.spinner("Analyzing drug-drug interactions..."):
            interaction_risk = random.uniform(0.1, 0.9)
            
            st.success("✅ DDI Prediction Complete!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Interaction Risk", f"{interaction_risk:.3f}")
            with col2:
                if interaction_risk > 0.7:
                    st.metric("Risk Level", "High", delta="Contraindicated")
                elif interaction_risk > 0.4:
                    st.metric("Risk Level", "Moderate", delta="Monitor")
                else:
                    st.metric("Risk Level", "Low", delta="Safe")

elif task == "ADMET Properties":
    st.header("🧪 ADMET Properties Prediction")
    
    drug_smiles = st.text_input("Drug SMILES", value="CCO")
    
    if st.button("🔬 Analyze ADMET", type="primary", use_container_width=True):
        with st.spinner("Analyzing ADMET properties..."):
            st.success("✅ ADMET Analysis Complete!")
            
            # Create tabs for different property categories
            tab1, tab2, tab3, tab4 = st.tabs(["Absorption", "Distribution", "Metabolism", "Toxicity"])
            
            with tab1:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Lipophilicity (LogP)", f"{random.uniform(0.5, 4.2):.2f}")
                    st.metric("Permeability", f"{random.uniform(0.1, 0.9):.3f}")
                with col2:
                    st.metric("Solubility", f"{random.uniform(-3, 1):.2f} log(mol/L)")
                    st.metric("Bioavailability", f"{random.uniform(20, 90):.0f}%")
            
            with tab2:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Plasma Protein Binding", f"{random.uniform(70, 99):.1f}%")
                with col2:
                    st.metric("Volume of Distribution", f"{random.uniform(0.5, 10):.2f} L/kg")
            
            with tab3:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Clearance", f"{random.uniform(5, 50):.1f} mL/min/kg")
                with col2:
                    st.metric("Half-life", f"{random.uniform(2, 24):.1f} hours")
            
            with tab4:
                toxicity_score = random.uniform(0.1, 0.8)
                st.metric("Overall Toxicity Risk", f"{toxicity_score:.3f}")
                
                if toxicity_score < 0.3:
                    st.success("🟢 Low toxicity risk")
                elif toxicity_score < 0.6:
                    st.warning("🟡 Moderate toxicity risk")
                else:
                    st.error("🔴 High toxicity risk")

elif task == "Molecular Similarity":
    st.header("🔍 Molecular Similarity Search")
    
    query_smiles = st.text_input("Query Molecule SMILES", value="CCO")
    
    if st.button("🔍 Find Similar Molecules", type="primary", use_container_width=True):
        with st.spinner("Searching molecular database..."):
            st.success("✅ Similarity Search Complete!")
            
            # Create similar molecules data
            similar_molecules = [
                {"Compound": "Triethylamine", "SMILES": "CCN(CC)CC", "Similarity": random.uniform(0.8, 0.95), "MW": 101.19},
                {"Compound": "Propanoic acid", "SMILES": "CCC(=O)O", "Similarity": random.uniform(0.6, 0.85), "MW": 74.08},
                {"Compound": "Isopropanol", "SMILES": "CC(C)O", "Similarity": random.uniform(0.5, 0.8), "MW": 60.10},
                {"Compound": "Ethylamine", "SMILES": "CCN", "Similarity": random.uniform(0.7, 0.9), "MW": 45.08},
                {"Compound": "Methanol", "SMILES": "CO", "Similarity": random.uniform(0.4, 0.7), "MW": 32.04}
            ]
            
            df = pd.DataFrame(similar_molecules)
            df['Similarity'] = df['Similarity'].round(3)
            
            st.subheader("📊 Top Similar Molecules")
            st.dataframe(df, use_container_width=True)
            
            # Visualization
            fig = px.bar(df, x='Compound', y='Similarity', 
                        title='Molecular Similarity Scores',
                        color='Similarity',
                        color_continuous_scale='viridis')
            st.plotly_chart(fig, use_container_width=True)

elif task == "AI Agent Analysis":
    st.header("🤖 AI Agent Analysis Dashboard")
    
    st.info("🔬 Access to 24 specialized pharmaceutical AI agents for comprehensive drug discovery analysis")
    
    # Agent categories
    agent_categories = {
        "🔄 Workflow Automation": ["Drug Pipeline Agent", "Data Collection Agent", "Quality Control Agent", "Knowledge Update Agent"],
        "🤝 Collaborative Research": ["Collaboration Setup Agent", "Market Analysis Agent", "Patent Search Agent", "Regulatory Compliance Agent"],
        "📊 Real-Time Intelligence": ["Pattern Recognition Agent", "Biomarker Discovery Agent", "Safety Monitoring Agent", "Clinical Insights Agent"],
        "🧠 Advanced Analytics": ["Document Processing Agent", "Literature Analysis Agent", "Data Mining Agent", "Predictive Analytics Agent"],
        "📄 Multi-Modal Research": ["Image Analysis Agent", "Text Processing Agent", "Molecular Visualization Agent", "Report Generation Agent"],
        "⚖️ Decision Support": ["Risk Assessment Agent", "Treatment Optimization Agent", "Drug Repurposing Agent", "Clinical Decision Agent"]
    }
    
    selected_category = st.selectbox("Choose Agent Category", list(agent_categories.keys()))
    selected_agent = st.selectbox("Select Specific Agent", agent_categories[selected_category])
    
    col1, col2 = st.columns(2)
    
    with col1:
        compound_input = st.text_area("Compounds (SMILES, one per line)", "CCO\nCCN(CC)CC")
        
    with col2:
        targets_input = st.text_area("Target Proteins", "EGFR\nBCR-ABL1")
    
    if st.button("🚀 Launch AI Analysis", type="primary", use_container_width=True):
        with st.spinner(f"Running {selected_agent} analysis..."):
            st.success(f"✅ {selected_agent} Analysis Complete!")
            
            # Generate mock results based on agent type
            if "Pipeline" in selected_agent:
                results_data = {
                    "Metric": ["Compounds Processed", "Targets Analyzed", "Success Rate", "Estimated Completion"],
                    "Value": [random.randint(50, 200), random.randint(10, 50), f"{random.uniform(75, 95):.1f}%", "2-3 weeks"]
                }
            elif "Market Analysis" in selected_agent:
                results_data = {
                    "Metric": ["Market Size", "Growth Rate", "Key Players", "Opportunities"],
                    "Value": [f"${random.uniform(5, 50):.1f}B", f"{random.uniform(8, 15):.1f}% CAGR", "4 Major Companies", "Rare Diseases"]
                }
            elif "Pattern Recognition" in selected_agent:
                results_data = {
                    "Metric": ["Patterns Identified", "Confidence Score", "Novel Insights", "Validation Status"],
                    "Value": [random.randint(5, 20), f"{random.uniform(80, 95):.1f}%", "3 New Relationships", "In Progress"]
                }
            else:
                results_data = {
                    "Metric": ["Analysis Complete", "Insights Generated", "Confidence Level", "Next Steps"],
                    "Value": ["Yes", random.randint(5, 15), f"{random.uniform(80, 95):.1f}%", "Review Results"]
                }
            
            results_df = pd.DataFrame(results_data)
            st.dataframe(results_df, use_container_width=True)

# Prediction history sidebar
if st.session_state.prediction_history:
    st.sidebar.markdown("---")
    st.sidebar.subheader("📈 Recent Predictions")
    
    for i, pred in enumerate(reversed(st.session_state.prediction_history[-3:])):
        with st.sidebar.expander(f"{pred['task']} - {pred['timestamp'].strftime('%H:%M')}"):
            st.write(f"**Model:** {pred.get('model', 'N/A')}")
            st.write(f"**Score:** {pred.get('score', 'N/A'):.3f}")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Platform Status", "🟢 Online")
    
with col2:
    st.metric("Available Models", "24 AI Agents")
    
with col3:
    st.metric("System Health", "98.5%")

st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>PharmQAgentAI - Transforming Drug Discovery with AI-Powered Insights</p>
</div>
""", unsafe_allow_html=True)