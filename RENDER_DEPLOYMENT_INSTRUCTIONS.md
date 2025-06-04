# Manual Render Deployment Configuration

Since Render is auto-detecting Poetry from pyproject.toml, configure manually in the Render dashboard:

## Render Dashboard Settings

1. **Build Command:**
```
pip install -r requirements.txt
```

2. **Start Command:**
```
streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
```

3. **Environment Variables:**
- Key: `HUGGINGFACE_TOKEN`
- Value: Your Hugging Face API token

## Alternative: Remove pyproject.toml

To force pip usage, temporarily rename pyproject.toml:
```bash
mv pyproject.toml pyproject.toml.backup
git add .
git commit -m "Temporarily disable Poetry for Render deployment"
git push origin main
```

## Deployment Steps

1. Delete the current Render service
2. Create new web service from GitHub
3. Select repository: cnusrini/dti-platform
4. Use manual configuration above
5. Add HUGGINGFACE_TOKEN environment variable
6. Deploy

Your PharmQAgentAI platform will deploy with:
- Enhanced table results display
- 20 transformer models from Hugging Face
- Complete sample data system
- Clinical interpretations for non-technical users