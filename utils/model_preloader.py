"""
Model Preloader for PharmQAgentAI

This module handles automatic preloading of DeepPurpose DTI models
from the Hugging Face repository for enhanced therapeutic intelligence.
"""

import asyncio
import logging
from typing import List, Dict, Any
from config.model_registry import get_available_models

logger = logging.getLogger(__name__)

class ModelPreloader:
    """Handles automatic preloading of therapeutic models"""
    
    def __init__(self, model_manager):
        self.model_manager = model_manager
        self.preload_status = {}
        
    def get_transformer_dti_models(self) -> List[Dict[str, Any]]:
        """Get all transformer-based DTI models from registry"""
        dti_models = get_available_models("DTI")
        transformer_models = []
        
        for model_name, model_config in dti_models.items():
            if model_config.get("model_type") == "transformer":
                transformer_models.append({
                    "name": model_name,
                    "config": model_config
                })
        
        return transformer_models
    
    def preload_transformer_dti_models(self) -> Dict[str, Any]:
        """Preload all transformer-based DTI models"""
        logger.info("Starting transformer DTI model preloading...")
        
        models_to_load = self.get_transformer_dti_models()
        preload_results = {
            "total_models": len(models_to_load),
            "loaded_successfully": 0,
            "failed_models": [],
            "success_models": []
        }
        
        for model_info in models_to_load:
            model_name = model_info["name"]
            model_config = model_info["config"]
            
            try:
                logger.info(f"Preloading {model_name}...")
                success = self.model_manager.load_model("DTI", model_name, model_config)
                
                if success:
                    preload_results["loaded_successfully"] += 1
                    preload_results["success_models"].append(model_name)
                    self.preload_status[model_name] = "loaded"
                    logger.info(f"Successfully preloaded {model_name}")
                else:
                    preload_results["failed_models"].append({
                        "name": model_name,
                        "error": "Failed to load model"
                    })
                    self.preload_status[model_name] = "failed"
                    logger.error(f"Failed to preload {model_name}")
                    
            except Exception as e:
                error_msg = str(e)
                preload_results["failed_models"].append({
                    "name": model_name,
                    "error": error_msg
                })
                self.preload_status[model_name] = "failed"
                logger.error(f"Error preloading {model_name}: {error_msg}")
        
        logger.info(f"Preloading complete: {preload_results['loaded_successfully']}/{preload_results['total_models']} models loaded")
        return preload_results
    
    def get_preload_status(self) -> Dict[str, str]:
        """Get current preload status for all models"""
        return self.preload_status.copy()
    
    def is_model_preloaded(self, model_name: str) -> bool:
        """Check if a specific model has been preloaded"""
        return self.preload_status.get(model_name) == "loaded"
    
    def get_preloaded_models(self) -> List[str]:
        """Get list of successfully preloaded models"""
        return [name for name, status in self.preload_status.items() if status == "loaded"]