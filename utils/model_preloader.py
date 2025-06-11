"""
Model Preloader for PharmQAgentAI
Handles background model loading and caching
"""
import logging
from typing import Dict, List, Any

class ModelPreloader:
    """Handles preloading of models for better performance"""
    
    def __init__(self, model_manager):
        """Initialize model preloader"""
        self.model_manager = model_manager
        self.logger = logging.getLogger(__name__)
        self.preload_status = {}
    
    def preload_all_models(self) -> Dict[str, bool]:
        """Preload all available models"""
        results = {}
        
        # Get all available models
        all_models = self.model_manager.get_available_models()
        
        for task, models in all_models.items():
            for model_name in models.keys():
                success = self.model_manager.load_model(task, model_name)
                model_key = f"{task}_{model_name}"
                results[model_key] = success
                self.preload_status[model_key] = success
        
        self.logger.info(f"Preloaded {len(results)} models")
        return results
    
    def preload_task_models(self, task: str) -> Dict[str, bool]:
        """Preload models for a specific task"""
        results = {}
        
        task_models = self.model_manager.get_available_models(task)
        
        for model_name in task_models.keys():
            success = self.model_manager.load_model(task, model_name)
            model_key = f"{task}_{model_name}"
            results[model_key] = success
            self.preload_status[model_key] = success
        
        self.logger.info(f"Preloaded {len(results)} models for task {task}")
        return results
    
    def get_preload_status(self) -> Dict[str, bool]:
        """Get current preload status"""
        return self.preload_status.copy()
    
    def get_preloaded_models(self) -> Dict[str, Any]:
        """Get all preloaded models with their information"""
        preloaded = {}
        for model_key, status in self.preload_status.items():
            if status:
                task, model_name = model_key.split('_', 1)
                preloaded[model_key] = {
                    "task": task,
                    "model_name": model_name,
                    "status": "loaded"
                }
        return preloaded
    
    def is_preloaded(self, task: str, model_name: str) -> bool:
        """Check if a specific model is preloaded"""
        model_key = f"{task}_{model_name}"
        return self.preload_status.get(model_key, False)