# PharmQAgentAI Deployment Guide

## Quick Start

### Local Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/PharmQAgentAI.git
cd PharmQAgentAI
```

2. **Install dependencies**
```bash
pip install -r backend/requirements.txt
pip install streamlit pandas numpy requests torch transformers
```

3. **Set up environment variables**
```bash
export HUGGINGFACE_TOKEN="your_hugging_face_token_here"
```

4. **Run the application**
```bash
# Frontend only (recommended for quick start)
streamlit run frontend/app.py --server.port 5000

# Full backend + frontend (advanced)
# Terminal 1: Start backend
cd backend && python -m uvicorn api.main:app --host 0.0.0.0 --port 8000

# Terminal 2: Start frontend
streamlit run frontend/streamlit_app.py --server.port 5000
```

## Deployment Options

### Option 1: Replit Deployment (Recommended)
- Import repository to Replit
- Set HUGGINGFACE_TOKEN in secrets
- Run: `streamlit run frontend/app.py --server.port 5000`

### Option 2: Streamlit Cloud
- Connect GitHub repository to Streamlit Cloud
- Add HUGGINGFACE_TOKEN to secrets
- Deploy frontend/app.py

### Option 3: Docker Deployment
```bash
# Build image
docker build -t pharmqagentai .

# Run container
docker run -p 5000:5000 -e HUGGINGFACE_TOKEN="your_token" pharmqagentai
```

### Option 4: Heroku Deployment
```bash
# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set HUGGINGFACE_TOKEN="your_token"

# Deploy
git push heroku main
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `HUGGINGFACE_TOKEN` | Your Hugging Face authentication token | Yes |
| `API_BASE_URL` | Backend API URL (for frontend-only deployment) | No |

## Features Available

### Transformer Models (20 Total)
- SciBERT-DTI, PubMedBERT-DTI, ChemBERTa-DTI, MolBERT-DTI
- GPT2-DTI, BERT-Base-DTI, T5-Small-DTI, ELECTRA-Small-DTI
- ALBERT-Base-DTI, DeBERTa-V3-Small, XLNet-Base-DTI, BART-Base-DTI
- MPNet-Base-DTI, Longformer-Base-DTI, BigBird-Base-DTI
- Reformer-DTI, Pegasus-Small-DTI, FNet-Base-DTI
- Funnel-Transformer-DTI, LED-Base-DTI

### Prediction Tasks
1. **Drug-Target Interaction (DTI)** - Binding probability prediction
2. **Drug-Target Affinity (DTA)** - Binding strength calculation
3. **Drug-Drug Interaction (DDI)** - Compound interaction analysis
4. **ADMET Properties** - Pharmacokinetic predictions
5. **Molecular Similarity** - Structure comparison search

### Sample Data Available
- Aspirin + COX-2 (Anti-inflammatory)
- Caffeine + Adenosine (Stimulant)
- Paclitaxel + Tubulin (Anticancer)
- Warfarin + Vitamin K (Anticoagulant)
- Atorvastatin (Cholesterol drug)
- Morphine analogs (Opioid)

## Troubleshooting

### Common Issues

1. **Models not loading**
   - Verify HUGGINGFACE_TOKEN is set correctly
   - Check internet connection for model downloads

2. **Port conflicts**
   - Change port: `--server.port 8501`
   - Kill existing processes: `pkill -f streamlit`

3. **Memory issues**
   - Use smaller models first
   - Increase system memory allocation

### Getting Help

- Check the README.md for detailed documentation
- Review logs for specific error messages
- Ensure all dependencies are installed correctly

## Security Notes

- Never commit your HUGGINGFACE_TOKEN to version control
- Use environment variables for all sensitive data
- The platform only uses verified Hugging Face repositories
- No synthetic data is used - all models provide authentic predictions

## Performance Optimization

- Models are loaded on-demand to optimize memory usage
- Use the model preloader for batch operations
- Backend/frontend separation allows independent scaling
- Temporary model files are automatically cleaned up