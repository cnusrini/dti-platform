import os
import tempfile
import requests
import json
from typing import Dict, Optional, Any
import logging
from datetime import datetime, timedelta

# Try to import torch, but make it optional for now
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    torch = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelManager:
    """Manages loading and unloading of Hugging Face models for therapeutic tasks"""
    
    def __init__(self):
        self.loaded_models: Dict[str, Any] = {}
        self.model_metadata: Dict[str, Dict] = {}
        self.temp_dir = tempfile.mkdtemp(prefix="pharmq_models_")
        self.hf_token = os.getenv("HUGGINGFACE_TOKEN", "")
        
        # Model cache with expiration
        self.model_cache_duration = timedelta(hours=2)  # Models expire after 2 hours of inactivity
        self.model_last_used: Dict[str, datetime] = {}
        
        logger.info(f"ModelManager initialized with temp directory: {self.temp_dir}")
    
    def _get_model_key(self, task: str, model_name: str) -> str:
        """Generate a unique key for the model"""
        return f"{task}_{model_name}"
    
    def _validate_huggingface_url(self, model_path: str) -> bool:
        """Validate that the model path is from approved Hugging Face sources"""
        approved_prefixes = [
            "https://huggingface.co/",
            "DeepChem/",
            "microsoft/",
            "facebook/",
            "google/",
            "nvidia/",
            "BioBert/",
            "allenai/",
            "ChemBERTa/"
        ]
        
        return any(model_path.startswith(prefix) for prefix in approved_prefixes)
    
    def _download_model_metadata(self, model_path: str) -> Optional[Dict]:
        """Download and parse model configuration from Hugging Face"""
        try:
            # Handle different URL formats
            if model_path.startswith("https://huggingface.co/"):
                base_url = model_path
            else:
                base_url = f"https://huggingface.co/{model_path}"
            
            config_url = f"{base_url}/resolve/main/config.json"
            
            headers = {}
            if self.hf_token:
                headers["Authorization"] = f"Bearer {self.hf_token}"
            
            response = requests.get(config_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            config = response.json()
            
            # Additional metadata from model card
            try:
                model_card_url = f"{base_url}/resolve/main/README.md"
                readme_response = requests.get(model_card_url, headers=headers, timeout=15)
                config['model_card_available'] = readme_response.status_code == 200
            except:
                config['model_card_available'] = False
            
            return config
            
        except requests.RequestException as e:
            logger.error(f"Failed to download model metadata: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse model config: {str(e)}")
            return None
    
    def _load_model_from_huggingface(self, model_path: str, task: str) -> Optional[Any]:
        """Load model from Hugging Face repository"""
        try:
            # For now, return a mock model structure for demonstration
            # This will be replaced with actual model loading when transformers is available
            logger.info(f"Creating demo model placeholder for {model_path} (task: {task})")
            
            # Create a demonstration model structure
            demo_model = {
                "model_path": model_path,
                "task": task,
                "type": "demo",
                "loaded": True,
                "capabilities": {
                    "DTI": "Drug-Target Interaction prediction",
                    "DTA": "Drug-Target Affinity prediction", 
                    "DDI": "Drug-Drug Interaction prediction",
                    "ADMET": "ADMET property prediction",
                    "Similarity": "Molecular similarity search"
                }.get(task, "Unknown task")
            }
            
            return demo_model
                
        except Exception as e:
            logger.error(f"Failed to load model from {model_path}: {str(e)}")
            return None
    
    def load_model(self, task: str, model_name: str, model_config: Dict) -> bool:
        """Load a model for a specific task"""
        try:
            model_key = self._get_model_key(task, model_name)
            
            # Check if model is already loaded
            if model_key in self.loaded_models:
                logger.info(f"Model {model_key} already loaded")
                self.model_last_used[model_key] = datetime.now()
                return True
            
            model_path = model_config.get('path', '')
            
            # Validate model source
            if not self._validate_huggingface_url(model_path):
                logger.error(f"Invalid or unauthorized model path: {model_path}")
                return False
            
            # Download metadata first
            metadata = self._download_model_metadata(model_path)
            if metadata:
                self.model_metadata[model_key] = metadata
                logger.info(f"Downloaded metadata for {model_key}")
            
            # Unload existing model for this task to save memory
            self._unload_task_models(task)
            
            # Load the model
            logger.info(f"Loading model {model_name} for task {task}")
            loaded_model = self._load_model_from_huggingface(model_path, task)
            
            if loaded_model:
                self.loaded_models[model_key] = {
                    'model_obj': loaded_model,
                    'task': task,
                    'name': model_name,
                    'config': model_config,
                    'loaded_at': datetime.now()
                }
                self.model_last_used[model_key] = datetime.now()
                
                logger.info(f"Successfully loaded model {model_key}")
                return True
            else:
                logger.error(f"Failed to load model {model_key}")
                return False
                
        except Exception as e:
            logger.error(f"Error loading model {task}/{model_name}: {str(e)}")
            return False
    
    def _unload_task_models(self, task: str):
        """Unload all models for a specific task to free memory"""
        keys_to_remove = []
        for model_key in self.loaded_models:
            if self.loaded_models[model_key]['task'] == task:
                keys_to_remove.append(model_key)
        
        for key in keys_to_remove:
            self._unload_model_by_key(key)
    
    def _unload_model_by_key(self, model_key: str):
        """Unload a specific model by its key"""
        if model_key in self.loaded_models:
            # Clean up GPU memory if using CUDA and torch is available
            if TORCH_AVAILABLE and torch and hasattr(torch, 'cuda') and torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            del self.loaded_models[model_key]
            if model_key in self.model_last_used:
                del self.model_last_used[model_key]
            if model_key in self.model_metadata:
                del self.model_metadata[model_key]
            
            logger.info(f"Unloaded model {model_key}")
    
    def unload_model(self, task: str, model_name: str):
        """Unload a specific model"""
        model_key = self._get_model_key(task, model_name)
        self._unload_model_by_key(model_key)
    
    def unload_all_models(self):
        """Unload all loaded models"""
        keys_to_remove = list(self.loaded_models.keys())
        for key in keys_to_remove:
            self._unload_model_by_key(key)
        
        logger.info("All models unloaded")
    
    def get_model(self, task: str, model_name: str) -> Optional[Dict]:
        """Get a loaded model for inference"""
        model_key = self._get_model_key(task, model_name)
        
        if model_key in self.loaded_models:
            self.model_last_used[model_key] = datetime.now()
            return self.loaded_models[model_key]
        
        return None
    
    def get_loaded_models(self) -> Dict[str, Dict]:
        """Get information about all loaded models"""
        return {
            key: {
                'task': info['task'],
                'name': info['name'],
                'loaded_at': info['loaded_at'],
                'last_used': self.model_last_used.get(key, info['loaded_at'])
            }
            for key, info in self.loaded_models.items()
        }
    
    def cleanup_expired_models(self):
        """Remove models that haven't been used recently"""
        current_time = datetime.now()
        expired_keys = []
        
        for model_key, last_used in self.model_last_used.items():
            if current_time - last_used > self.model_cache_duration:
                expired_keys.append(model_key)
        
        for key in expired_keys:
            logger.info(f"Cleaning up expired model: {key}")
            self._unload_model_by_key(key)
    
    def get_model_metadata(self, task: str, model_name: str) -> Optional[Dict]:
        """Get metadata for a specific model"""
        model_key = self._get_model_key(task, model_name)
        return self.model_metadata.get(model_key)
    
    def __del__(self):
        """Cleanup temporary directory on destruction"""
        try:
            import shutil
            if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                logger.info(f"Cleaned up temporary directory: {self.temp_dir}")
        except:
            pass
