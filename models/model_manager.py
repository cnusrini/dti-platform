"""
Model Manager for PharmQAgentAI
Handles model loading, caching, and management
"""
import os
import tempfile
import logging
from typing import Dict, Any, Optional

class ModelManager:
    """Manages AI models for pharmaceutical predictions"""
    
    def __init__(self):
        """Initialize the model manager"""
        self.temp_dir = tempfile.mkdtemp(prefix="pharmq_models_")
        self.loaded_models = {}
        self.model_cache = {}
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"ModelManager initialized with temp directory: {self.temp_dir}")
    
    def get_available_models(self, task: str = None) -> Dict[str, Any]:
        """Get available models for a specific task"""
        models = {
            "DTI": {
                "DeepDTI": {"type": "transformer", "status": "available"},
                "GraphDTI": {"type": "graph", "status": "available"}
            },
            "DTA": {
                "DeepDTA": {"type": "transformer", "status": "available"},
                "AttentionDTA": {"type": "attention", "status": "available"}
            },
            "DDI": {
                "DrugBAN": {"type": "transformer", "status": "available"},
                "MHCADDI": {"type": "multihead", "status": "available"}
            },
            "ADMET": {
                "ADMETlab": {"type": "ensemble", "status": "available"},
                "ChemProp": {"type": "graph", "status": "available"}
            },
            "Similarity": {
                "MolBERT": {"type": "transformer", "status": "available"},
                "ChemBERTa": {"type": "transformer", "status": "available"}
            }
        }
        
        if task:
            return models.get(task, {})
        return models
    
    def load_model(self, task: str, model_name: str) -> bool:
        """Load a specific model"""
        try:
            model_key = f"{task}_{model_name}"
            
            if model_key in self.loaded_models:
                self.logger.info(f"Model {model_key} already loaded")
                return True
            
            # Simulate model loading
            self.loaded_models[model_key] = {
                "task": task,
                "name": model_name,
                "status": "loaded",
                "loaded_at": "2024-01-01"
            }
            
            self.logger.info(f"Successfully loaded model: {model_key}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load model {task}_{model_name}: {e}")
            return False
    
    def is_model_loaded(self, task: str, model_name: str) -> bool:
        """Check if a model is loaded"""
        model_key = f"{task}_{model_name}"
        return model_key in self.loaded_models
    
    def get_loaded_models(self) -> Dict[str, Any]:
        """Get all loaded models"""
        return self.loaded_models
    
    def unload_model(self, task: str, model_name: str) -> bool:
        """Unload a specific model"""
        model_key = f"{task}_{model_name}"
        
        if model_key in self.loaded_models:
            del self.loaded_models[model_key]
            self.logger.info(f"Unloaded model: {model_key}")
            return True
        
        return False
    
    def get_model_info(self, task: str, model_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific model"""
        model_key = f"{task}_{model_name}"
        return self.loaded_models.get(model_key)