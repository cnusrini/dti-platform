# PharmQAgentAI: Therapeutic Intelligence Platform

A comprehensive AI-driven platform for drug discovery and therapeutics prediction, featuring 20 transformer models from verified Hugging Face repositories with complete backend/frontend separation.

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

### Transformer Models (20 Total)
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

## 🛠️ Installation & Setup

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
streamlit run frontend/app.py --server.port 5000
```

### Unified Application
```bash
streamlit run frontend/app.py --server.port 5000
```

## 🔧 Configuration

### Environment Variables
- `HUGGINGFACE_TOKEN` - Your Hugging Face authentication token
- `API_BASE_URL` - Backend API endpoint (default: http://localhost:8000)

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

### DTI Prediction
```python
# Example SMILES and protein sequence
drug_smiles = "CC(=O)OC1=CC=CC=C1C(=O)O"  # Aspirin
target_sequence = "MKVLWAALLVTFLAGCQAKVEQAVETEPEPELR..."

# Make prediction through UI or API
result = predict_dti(drug_smiles, target_sequence)
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

The platform is designed for deployment on Replit with automatic scaling and health monitoring. The backend/frontend separation allows for independent scaling and maintenance.

### Production Setup
1. Configure environment variables
2. Start FastAPI backend service
3. Launch Streamlit frontend
4. Configure load balancing if needed

## 🤝 Contributing

The modular architecture supports easy extension:
- Add new models in `backend/config/model_registry.py`
- Implement new prediction tasks in `backend/models/prediction_tasks.py`
- Create new UI components in `frontend/components/`

## 📝 License

This project implements therapeutic intelligence capabilities with authentic AI models for drug discovery research and development.