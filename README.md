# PharmQAgentAI: Therapeutic Intelligence Platform

A comprehensive AI-driven platform for drug discovery and therapeutics prediction, featuring advanced authentication, 24 specialized AI agents, 20 transformer models, and professional user interface designed for pharmaceutical research.

## 🏗️ Architecture Overview

```
PharmQAgentAI/
├── backend/                    # FastAPI Backend
│   ├── api/
│   │   ├── main.py            # FastAPI application
│   │   └── __init__.py
│   ├── models/
│   │   ├── model_manager.py   # Model loading/management
│   │   ├── prediction_tasks.py # Core prediction logic
│   │   └── __init__.py
│   ├── agents/                 # AI Agent System
│   │   ├── base_agent.py      # Base agent class with Gemini integration
│   │   ├── drug_discovery_assistant.py # Main AI assistant
│   │   ├── research_orchestrator.py # Multi-agent orchestration
│   │   ├── agent_manager.py   # Agent coordination and management
│   │   └── __init__.py
│   ├── utils/
│   │   ├── molecular_utils.py # Molecular data processing
│   │   ├── validation.py      # Input validation
│   │   ├── model_preloader.py # Automatic model loading
│   │   └── __init__.py
│   ├── config/
│   │   ├── model_registry.py  # Model configurations
│   │   └── __init__.py
│   ├── requirements.txt       # Backend dependencies
│   └── __init__.py
├── frontend/                   # Streamlit Frontend
│   ├── app.py                 # Main Streamlit application
│   ├── streamlit_app.py       # API-connected frontend
│   ├── components/            # UI components
│   ├── pages/                 # Multi-page structure
│   ├── assets/                # Static assets
│   └── styles/                # CSS styling
├── .streamlit/
│   └── config.toml           # Streamlit configuration
├── app.py                    # Legacy unified app
├── basic_app.py             # Simplified version
├── demo.html                # HTML demonstration
└── README.md                # This file
```

## 🚀 Key Features

### 🔐 Professional Authentication System
- **PostgreSQL Integration** - Secure database authentication with Neon/Render PostgreSQL
- **EmedChainHub-Style Interface** - Professional login design matching pharmaceutical industry standards
- **User Management** - Registration, login, session management with encrypted passwords
- **Conventional UX** - User information displayed in top-right header following standard patterns
- **Demo Mode** - Quick access for testing and demonstration purposes

### 🤖 Advanced AI Agent System (24 Agents)
- **6 Agent Categories** - Workflow Automation, Collaborative Research, Real-Time Intelligence, Advanced Analytics, Multi-Modal Research, Decision Support
- **Google AI Integration** - Powered by Google Gemini and generative AI technologies
- **Specialized Research Agents** - Domain-specific agents for pharmaceutical research workflows
- **Real-Time Analysis** - Instant AI-powered insights and recommendations
- **Multi-Modal Capabilities** - Text, molecular, and data analysis integration

### 🧬 Transformer Models (20 Total)
- **SciBERT-DTI** - Scientific literature predictions
- **PubMedBERT-DTI** - Biomedical research applications
- **ChemBERTa-DTI** - Chemical structure analysis
- **MolBERT-DTI** - Molecular representation learning
- **GPT2-DTI** - Generative molecular modeling
- **BERT-Base-DTI** - General language understanding
- **T5-Small-DTI** - Text-to-text transformations
- **ELECTRA-Small-DTI** - Efficient transformer architecture
- **ALBERT-Base-DTI** - Lightweight BERT variant
- **DeBERTa-V3-Small** - Enhanced bidirectional encoder
- **XLNet-Base-DTI** - Permutation-based language model
- **BART-Base-DTI** - Denoising autoencoder
- **MPNet-Base-DTI** - Masked and permuted pre-training
- **Longformer-Base-DTI** - Long sequence processing
- **BigBird-Base-DTI** - Sparse attention mechanisms
- **Reformer-DTI** - Memory-efficient transformer
- **Pegasus-Small-DTI** - Abstractive summarization
- **FNet-Base-DTI** - Fourier transform mixing
- **Funnel-Transformer-DTI** - Progressive token reduction
- **LED-Base-DTI** - Long document processing

### Prediction Tasks
1. **Drug-Target Interaction (DTI)** - Predict binding probability
2. **Drug-Target Affinity (DTA)** - Calculate binding strength (IC50/Kd/Ki)
3. **Drug-Drug Interaction (DDI)** - Analyze compound interactions
4. **ADMET Properties** - Predict pharmacokinetic properties
5. **Molecular Similarity** - Find structurally similar compounds

### AI-Powered Analysis Features

#### 🧠 Intelligent Drug Discovery Assistant
Advanced AI agent powered by Google Gemini-1.5-flash that provides contextual analysis of prediction results:

- **Explain Results** - Plain-language explanations of prediction outcomes
- **Clinical Interpretation** - Medical relevance and therapeutic implications
- **Safety Assessment** - Risk analysis and contraindication identification
- **Custom Analysis** - Answer specific questions about compounds and targets
- **Conversation History** - Maintains context across multiple queries
- **Real-time Processing** - Instant AI responses with scientific accuracy

The assistant integrates seamlessly with all prediction tasks, appearing contextually after results are generated. It preserves prediction displays during analysis and maintains comprehensive conversation history for research continuity.

#### 🔄 Multi-Agent Research Orchestration
Sophisticated multi-agent system that coordinates specialized AI agents for comprehensive drug discovery research:

- **Research Agent** - Scientific literature analysis and data gathering
- **Analysis Agent** - Molecular data processing and insight generation  
- **Validation Agent** - Cross-referencing against known databases and standards
- **Reporting Agent** - Compilation of findings into comprehensive research reports

**Orchestration Workflow:**
1. Compound data and prediction results are distributed to specialized agents
2. Each agent performs domain-specific analysis in parallel
3. Results are aggregated and cross-validated
4. Comprehensive reports are generated with actionable insights
5. Findings are presented with scientific references and confidence metrics

**Agent Capabilities:**
- Autonomous research task execution
- Knowledge synthesis from multiple sources
- Quality validation and error detection
- Report generation with citations
- Interactive query processing

## 🛠️ Installation & Setup

### Local Development
```bash
# Clone repository
git clone https://github.com/yourusername/pharmqagentai.git
cd pharmqagentai

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="your_postgresql_connection_string"
export HUGGINGFACE_TOKEN="your_huggingface_token"
export GOOGLE_AI_API_KEY="your_google_ai_key"

# Run application
streamlit run frontend/app.py --server.port 5000
```

### Quick Start with Demo
```bash
# Run with demo authentication (no database required)
streamlit run frontend/app.py --server.port 5000
# Click "Use Demo" button to bypass authentication
```

## 🔧 Configuration

### Required Environment Variables
- `DATABASE_URL` - PostgreSQL connection string (e.g., `postgresql://user:pass@host:port/db`)
- `HUGGINGFACE_TOKEN` - Your Hugging Face authentication token for model access
- `GOOGLE_AI_API_KEY` - Google AI API key for advanced agent features (optional)

### Database Setup
PharmQAgentAI uses PostgreSQL for user authentication and session management:

**For Local Development:**
- Use Neon, Supabase, or local PostgreSQL instance
- Set DATABASE_URL environment variable

**For Production Deployment:**
- Render PostgreSQL (recommended)
- Any PostgreSQL-compatible database service

The application automatically creates required tables on first run:
- `pharmq_users` - User accounts and authentication
- `pharmq_subscriptions` - User subscription management  
- `pharmq_usage_tracking` - Feature usage analytics

### Streamlit Configuration (.streamlit/config.toml)
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000

[browser]
gatherUsageStats = false
```

## 📊 API Endpoints

### Model Management
- `GET /models/available` - List available models
- `GET /models/loaded` - Show loaded models
- `POST /models/load` - Load specific model
- `POST /models/preload-transformers` - Load all transformer models

### Predictions
- `POST /predict/dti` - Drug-Target Interaction
- `POST /predict/dta` - Drug-Target Affinity
- `POST /predict/ddi` - Drug-Drug Interaction
- `POST /predict/admet` - ADMET Properties
- `POST /predict/similarity` - Molecular Similarity

### Utilities
- `GET /utils/validate-smiles/{smiles}` - Validate SMILES strings
- `GET /utils/molecular-descriptors/{smiles}` - Calculate descriptors

## 🧪 Usage Examples

### DTI Prediction with AI Analysis
```python
# Example SMILES and protein sequence
drug_smiles = "CC(=O)OC1=CC=CC=C1C(=O)O"  # Aspirin
target_sequence = "MKVLWAALLVTFLAGCQAKVEQAVETEPEPELR..."

# Make prediction through UI or API
result = predict_dti(drug_smiles, target_sequence)

# AI analysis automatically available after prediction
# - Explain Results: Plain-language interpretation
# - Clinical Interpretation: Medical relevance
# - Safety Assessment: Risk analysis
# - Custom Questions: Specific compound inquiries
```

### AI Agent Workflow
```python
# Multi-agent research orchestration
compound_data = {"smiles": drug_smiles, "name": "Aspirin"}
prediction_results = {"DTI": result}

# Agents work in parallel:
# 1. Research Agent - Literature analysis
# 2. Analysis Agent - Data processing
# 3. Validation Agent - Database cross-reference
# 4. Reporting Agent - Comprehensive report generation

research_report = orchestrate_research(compound_data, prediction_results)
```

### Model Loading
```python
# Load all transformer models
preload_results = preload_transformer_models()
print(f"Loaded {preload_results['loaded_successfully']} models")
```

## 🔐 Data Integrity

- All models sourced from verified Hugging Face repositories
- Authentic metadata validation for each model
- Secure API authentication with user-provided tokens
- No synthetic or placeholder data used in predictions

## 📈 Performance Metrics

Each model includes authentic performance data:
- **Accuracy/F1 Score** for classification tasks
- **MSE/RMSE** for regression tasks
- **Confidence Intervals** for binding predictions
- **Dataset Sources** (BindingDB, ChEMBL, etc.)

## 🚀 Deployment

### Render Deployment (Recommended)

PharmQAgentAI is optimized for Render deployment with PostgreSQL integration.

**Quick Steps:**
1. **Create PostgreSQL Database** on Render
2. **Create Web Service** connected to your GitHub repository
3. **Configure Environment Variables**
4. **Deploy**

**Render Configuration:**
```bash
# Build Command
pip install -r requirements.txt

# Start Command  
streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0

# Environment Variables
DATABASE_URL=postgresql://user:pass@host:port/database
HUGGINGFACE_TOKEN=your_huggingface_token
GOOGLE_AI_API_KEY=your_google_ai_key
```

**Detailed Deployment Guide:** See `RENDER_DEPLOYMENT_GUIDE.md` for complete instructions.

### Other Deployment Options

**Streamlit Cloud:**
- Connect GitHub repository
- Add secrets: `DATABASE_URL`, `HUGGINGFACE_TOKEN`, `GOOGLE_AI_API_KEY`
- Deploy directly from `frontend/app.py`

**Docker/Heroku:**
- Use provided `Procfile` and `runtime.txt`
- Configure PostgreSQL add-on
- Set environment variables

### Requirements
- PostgreSQL database (Render, Neon, Supabase, etc.)
- Hugging Face account with API token
- Google AI API key (optional, for advanced features)

## 🤝 Contributing

The modular architecture supports easy extension:
- Add new models in `backend/config/model_registry.py`
- Implement new prediction tasks in `backend/models/prediction_tasks.py`
- Create new UI components in `frontend/components/`

## 📝 License

This project implements therapeutic intelligence capabilities with authentic AI models for drug discovery research and development.