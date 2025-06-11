"""
Model registry for PharmQAgentAI
"""

from typing import Dict, List, Any

class ModelRegistry:
    """Central registry for all available models"""
    
    @staticmethod
    def get_model_catalog() -> Dict[str, Dict[str, Any]]:
        """Get complete model catalog"""
        return {
            "DTI": {
                "BioBERT-DTI": {
                    "description": "BioBERT-based drug-target interaction predictor",
                    "version": "1.0.0",
                    "accuracy": 0.89
                },
                "DeepDTI": {
                    "description": "Deep learning DTI prediction model",
                    "version": "2.1.0", 
                    "accuracy": 0.92
                },
                "GraphConv-DTI": {
                    "description": "Graph convolutional DTI predictor",
                    "version": "1.5.0",
                    "accuracy": 0.87
                }
            },
            "DTA": {
                "DeepDTA": {
                    "description": "Deep drug-target affinity predictor",
                    "version": "1.0.0",
                    "rmse": 0.65
                },
                "GraphDTA": {
                    "description": "Graph-based DTA prediction",
                    "version": "1.2.0",
                    "rmse": 0.62
                },
                "AttentionDTA": {
                    "description": "Attention mechanism DTA predictor",
                    "version": "1.1.0",
                    "rmse": 0.58
                }
            },
            "DDI": {
                "DeepDDI": {
                    "description": "Deep learning drug-drug interaction predictor",
                    "version": "1.0.0",
                    "accuracy": 0.85
                },
                "MHCADDI": {
                    "description": "Multi-head cross attention DDI predictor",
                    "version": "2.0.0",
                    "accuracy": 0.88
                },
                "GraphDDI": {
                    "description": "Graph neural network DDI predictor",
                    "version": "1.3.0",
                    "accuracy": 0.86
                }
            },
            "ADMET": {
                "ADMETlab": {
                    "description": "Comprehensive ADMET property predictor",
                    "version": "2.1.0",
                    "accuracy": 0.84
                },
                "DeepADMET": {
                    "description": "Deep learning ADMET predictor",
                    "version": "1.5.0",
                    "accuracy": 0.82
                },
                "GraphADMET": {
                    "description": "Graph-based ADMET predictor",
                    "version": "1.2.0",
                    "accuracy": 0.83
                }
            },
            "SIMILARITY": {
                "Morgan": {
                    "description": "Morgan fingerprint similarity",
                    "version": "1.0.0",
                    "method": "fingerprint"
                },
                "MACCS": {
                    "description": "MACCS keys similarity",
                    "version": "1.0.0",
                    "method": "fingerprint"
                },
                "RDKit": {
                    "description": "RDKit descriptor similarity",
                    "version": "1.0.0",
                    "method": "descriptor"
                }
            }
        }
    
    @staticmethod
    def get_models_for_task(task: str) -> List[str]:
        """Get available models for a specific task"""
        catalog = ModelRegistry.get_model_catalog()
        return list(catalog.get(task, {}).keys())

# Create the MODEL_REGISTRY constant that the app expects
MODEL_REGISTRY = ModelRegistry.get_model_catalog()