"""
FastAPI Backend for PharmQAgentAI
Therapeutic Intelligence Platform API
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.model_manager import ModelManager
from models.prediction_tasks import PredictionTasks
from utils.molecular_utils import MolecularUtils
from utils.validation import ValidationUtils
from utils.model_preloader import ModelPreloader
from config.model_registry import MODEL_REGISTRY, get_available_models

app = FastAPI(
    title="PharmQAgentAI API",
    description="Therapeutic Intelligence Platform with Transformer Models",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
model_manager = ModelManager()
prediction_tasks = PredictionTasks(model_manager)
molecular_utils = MolecularUtils()
validation_utils = ValidationUtils()
model_preloader = ModelPreloader(model_manager)

# Pydantic models
class DTIRequest(BaseModel):
    drug_smiles: str
    target_sequence: str
    model_name: Optional[str] = "SciBERT-DTI"

class DTARequest(BaseModel):
    drug_smiles: str
    target_sequence: str
    affinity_type: str = "IC50"
    model_name: Optional[str] = "DeepDTA-BERT"

class DDIRequest(BaseModel):
    drug1_smiles: str
    drug2_smiles: str
    interaction_type: str = "Unknown"
    model_name: Optional[str] = "DrugBERT-DDI"

class ADMETRequest(BaseModel):
    drug_smiles: str
    properties: List[str]
    model_name: Optional[str] = "ChemBERTa-ADMET"

class SimilarityRequest(BaseModel):
    query_smiles: str
    threshold: float = 0.7
    method: str = "Tanimoto"
    max_results: int = 10

class ModelLoadRequest(BaseModel):
    task: str
    model_name: str

# API Endpoints
@app.get("/")
async def root():
    return {"message": "PharmQAgentAI API", "status": "running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "models_loaded": len(model_manager.get_loaded_models())}

@app.get("/models/available")
async def get_available_models_endpoint(task: Optional[str] = None):
    """Get available models for a specific task or all tasks"""
    try:
        models = get_available_models(task)
        return {"status": "success", "data": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models/loaded")
async def get_loaded_models():
    """Get currently loaded models"""
    try:
        loaded = model_manager.get_loaded_models()
        return {"status": "success", "loaded_models": loaded}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/models/load")
async def load_model(request: ModelLoadRequest):
    """Load a specific model for a task"""
    try:
        # Get model config
        task_models = MODEL_REGISTRY.get(request.task, {})
        if request.model_name not in task_models:
            raise HTTPException(status_code=404, detail="Model not found")
        
        model_config = task_models[request.model_name]
        success = model_manager.load_model(request.task, request.model_name, model_config)
        
        if success:
            return {"status": "success", "message": f"Model {request.model_name} loaded successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to load model")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/models/preload-transformers")
async def preload_transformer_models():
    """Preload all transformer DTI models"""
    try:
        results = model_preloader.preload_transformer_dti_models()
        return {"status": "success", "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/dti")
async def predict_dti(request: DTIRequest):
    """Predict Drug-Target Interaction"""
    try:
        # Validate inputs
        if not validation_utils.validate_smiles(request.drug_smiles):
            raise HTTPException(status_code=400, detail="Invalid SMILES string")
        
        if not validation_utils.validate_protein_sequence(request.target_sequence):
            raise HTTPException(status_code=400, detail="Invalid protein sequence")
        
        # Make prediction
        result = prediction_tasks.predict_dti(request.drug_smiles, request.target_sequence)
        
        if result:
            return {"status": "success", "prediction": result}
        else:
            raise HTTPException(status_code=500, detail="Prediction failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/dta")
async def predict_dta(request: DTARequest):
    """Predict Drug-Target Binding Affinity"""
    try:
        # Validate inputs
        if not validation_utils.validate_smiles(request.drug_smiles):
            raise HTTPException(status_code=400, detail="Invalid SMILES string")
        
        if not validation_utils.validate_protein_sequence(request.target_sequence):
            raise HTTPException(status_code=400, detail="Invalid protein sequence")
        
        # Make prediction
        result = prediction_tasks.predict_dta(
            request.drug_smiles, 
            request.target_sequence, 
            request.affinity_type
        )
        
        if result:
            return {"status": "success", "prediction": result}
        else:
            raise HTTPException(status_code=500, detail="Prediction failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/ddi")
async def predict_ddi(request: DDIRequest):
    """Predict Drug-Drug Interaction"""
    try:
        # Validate inputs
        if not validation_utils.validate_smiles(request.drug1_smiles):
            raise HTTPException(status_code=400, detail="Invalid Drug 1 SMILES string")
        
        if not validation_utils.validate_smiles(request.drug2_smiles):
            raise HTTPException(status_code=400, detail="Invalid Drug 2 SMILES string")
        
        # Make prediction
        result = prediction_tasks.predict_ddi(
            request.drug1_smiles, 
            request.drug2_smiles, 
            request.interaction_type
        )
        
        if result:
            return {"status": "success", "prediction": result}
        else:
            raise HTTPException(status_code=500, detail="Prediction failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/admet")
async def predict_admet(request: ADMETRequest):
    """Predict ADMET Properties"""
    try:
        # Validate inputs
        if not validation_utils.validate_smiles(request.drug_smiles):
            raise HTTPException(status_code=400, detail="Invalid SMILES string")
        
        if not validation_utils.validate_admet_properties(request.properties):
            raise HTTPException(status_code=400, detail="Invalid ADMET properties")
        
        # Make prediction
        result = prediction_tasks.predict_admet(request.drug_smiles, request.properties)
        
        if result:
            return {"status": "success", "prediction": result}
        else:
            raise HTTPException(status_code=500, detail="Prediction failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/similarity")
async def predict_similarity(request: SimilarityRequest):
    """Predict Molecular Similarity"""
    try:
        # Validate inputs
        if not validation_utils.validate_smiles(request.query_smiles):
            raise HTTPException(status_code=400, detail="Invalid SMILES string")
        
        if not validation_utils.validate_similarity_method(request.method):
            raise HTTPException(status_code=400, detail="Invalid similarity method")
        
        # Make prediction
        result = prediction_tasks.predict_similarity(
            request.query_smiles,
            request.threshold,
            request.method,
            request.max_results
        )
        
        if result:
            return {"status": "success", "prediction": result}
        else:
            raise HTTPException(status_code=500, detail="Prediction failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/utils/validate-smiles/{smiles}")
async def validate_smiles_endpoint(smiles: str):
    """Validate SMILES string"""
    try:
        is_valid = validation_utils.validate_smiles(smiles)
        parsed = molecular_utils.parse_smiles(smiles) if is_valid else None
        
        return {
            "status": "success",
            "is_valid": is_valid,
            "parsed_data": parsed
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/utils/molecular-descriptors/{smiles}")
async def get_molecular_descriptors(smiles: str):
    """Calculate molecular descriptors"""
    try:
        if not validation_utils.validate_smiles(smiles):
            raise HTTPException(status_code=400, detail="Invalid SMILES string")
        
        descriptors = molecular_utils.calculate_molecular_descriptors(smiles)
        return {"status": "success", "descriptors": descriptors}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)