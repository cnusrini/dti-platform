"""
Prediction Tasks for PharmQAgentAI
Defines different prediction tasks and their configurations
"""

from typing import Dict, List, Any
from enum import Enum

class TaskType(Enum):
    """Enumeration of available prediction tasks"""
    DTI = "Drug-Target Interaction"
    DTA = "Drug-Target Affinity"
    DDI = "Drug-Drug Interaction"
    ADMET = "ADMET Properties"
    SIMILARITY = "Molecular Similarity"

class PredictionTasks:
    """Manages prediction tasks and their configurations"""
    
    @staticmethod
    def get_task_config(task_type: str) -> Dict[str, Any]:
        """Get configuration for a specific task type"""
        
        configs = {
            "DTI": {
                "name": "Drug-Target Interaction Prediction",
                "description": "Predict whether a drug compound will interact with a target protein",
                "inputs": ["drug_smiles", "target_sequence"],
                "outputs": ["interaction_score", "confidence", "prediction"],
                "models": ["BioBERT-DTI", "DeepDTI", "GraphConv-DTI"],
                "default_model": "BioBERT-DTI",
                "preprocessing": ["smiles_validation", "sequence_validation"]
            },
            
            "DTA": {
                "name": "Drug-Target Affinity Prediction",
                "description": "Predict the binding affinity between a drug and target protein",
                "inputs": ["drug_smiles", "target_sequence"],
                "outputs": ["affinity_value", "binding_strength"],
                "models": ["DeepDTA", "GraphDTA", "AttentionDTA"],
                "default_model": "DeepDTA",
                "preprocessing": ["smiles_validation", "sequence_validation"]
            },
            
            "DDI": {
                "name": "Drug-Drug Interaction Prediction",
                "description": "Predict interactions between two drug compounds",
                "inputs": ["drug1_smiles", "drug2_smiles"],
                "outputs": ["interaction_risk", "risk_level", "recommendation"],
                "models": ["DeepDDI", "MHCADDI", "GraphDDI"],
                "default_model": "DeepDDI",
                "preprocessing": ["smiles_validation", "drug_pair_validation"]
            },
            
            "ADMET": {
                "name": "ADMET Properties Prediction",
                "description": "Predict Absorption, Distribution, Metabolism, Excretion, and Toxicity properties",
                "inputs": ["drug_smiles"],
                "outputs": ["lipophilicity", "solubility", "clearance", "half_life", "toxicity_score"],
                "models": ["ADMETlab", "DeepADMET", "GraphADMET"],
                "default_model": "ADMETlab",
                "preprocessing": ["smiles_validation", "molecular_descriptors"]
            },
            
            "SIMILARITY": {
                "name": "Molecular Similarity Search",
                "description": "Find structurally similar molecules to a query compound",
                "inputs": ["query_smiles"],
                "outputs": ["similar_molecules", "similarity_scores"],
                "models": ["Morgan", "MACCS", "RDKit"],
                "default_model": "Morgan",
                "preprocessing": ["smiles_validation", "fingerprint_generation"]
            }
        }
        
        return configs.get(task_type, {})
    
    @staticmethod
    def get_all_tasks() -> Dict[str, Dict[str, Any]]:
        """Get all available tasks and their configurations"""
        task_types = ["DTI", "DTA", "DDI", "ADMET", "SIMILARITY"]
        return {task: PredictionTasks.get_task_config(task) for task in task_types}
    
    @staticmethod
    def validate_input(task_type: str, input_data: Dict[str, Any]) -> bool:
        """Validate input data for a specific task"""
        config = PredictionTasks.get_task_config(task_type)
        required_inputs = config.get("inputs", [])
        
        for required_input in required_inputs:
            if required_input not in input_data or not input_data[required_input]:
                return False
        
        return True
    
    @staticmethod
    def get_task_description(task_type: str) -> str:
        """Get human-readable description of a task"""
        config = PredictionTasks.get_task_config(task_type)
        return config.get("description", "No description available")
    
    @staticmethod
    def get_available_models(task_type: str) -> List[str]:
        """Get available models for a specific task"""
        config = PredictionTasks.get_task_config(task_type)
        return config.get("models", [])
    
    @staticmethod
    def get_default_model(task_type: str) -> str:
        """Get default model for a specific task"""
        config = PredictionTasks.get_task_config(task_type)
        return config.get("default_model", "")
    
    @staticmethod
    def format_results(task_type: str, raw_results: Dict[str, Any]) -> Dict[str, Any]:
        """Format prediction results for display"""
        
        if task_type == "DTI":
            return {
                "Interaction Score": f"{raw_results.get('interaction_score', 0):.3f}",
                "Confidence": f"{raw_results.get('confidence', 0):.3f}",
                "Prediction": raw_results.get('prediction', 'unknown').capitalize(),
                "Interpretation": PredictionTasks._interpret_dti_results(raw_results)
            }
        
        elif task_type == "DTA":
            return {
                "Affinity (pIC50)": f"{raw_results.get('affinity_value', 0):.2f}",
                "Binding Strength": raw_results.get('binding_strength', 'unknown').capitalize(),
                "Interpretation": PredictionTasks._interpret_dta_results(raw_results)
            }
        
        elif task_type == "DDI":
            return {
                "Interaction Risk": f"{raw_results.get('interaction_risk', 0):.3f}",
                "Risk Level": raw_results.get('risk_level', 'unknown').capitalize(),
                "Recommendation": raw_results.get('recommendation', 'unknown').capitalize(),
                "Interpretation": PredictionTasks._interpret_ddi_results(raw_results)
            }
        
        elif task_type == "ADMET":
            properties = raw_results.get('properties', {})
            return {
                "Lipophilicity (LogP)": f"{properties.get('lipophilicity', 0):.2f}",
                "Solubility (log mol/L)": f"{properties.get('solubility', 0):.2f}",
                "Clearance (mL/min/kg)": f"{properties.get('clearance', 0):.1f}",
                "Half-life (hours)": f"{properties.get('half_life', 0):.1f}",
                "Toxicity Assessment": raw_results.get('toxicity_assessment', 'unknown').capitalize()
            }
        
        elif task_type == "SIMILARITY":
            return {
                "Similar Molecules Found": raw_results.get('total_found', 0),
                "Top Matches": raw_results.get('similar_molecules', [])
            }
        
        return raw_results
    
    @staticmethod
    def _interpret_dti_results(results: Dict[str, Any]) -> str:
        """Interpret DTI prediction results"""
        score = results.get('interaction_score', 0)
        if score > 0.7:
            return "Strong interaction predicted - High therapeutic potential"
        elif score > 0.5:
            return "Moderate interaction predicted - Further validation recommended"
        else:
            return "Weak interaction predicted - Consider alternative targets"
    
    @staticmethod
    def _interpret_dta_results(results: Dict[str, Any]) -> str:
        """Interpret DTA prediction results"""
        affinity = results.get('affinity_value', 0)
        if affinity > 7.0:
            return "High affinity predicted - Excellent drug candidate"
        elif affinity > 5.5:
            return "Moderate affinity - May require optimization"
        else:
            return "Low affinity - Consider structural modifications"
    
    @staticmethod
    def _interpret_ddi_results(results: Dict[str, Any]) -> str:
        """Interpret DDI prediction results"""
        risk = results.get('interaction_risk', 0)
        if risk > 0.7:
            return "High interaction risk - Contraindicated combination"
        elif risk > 0.4:
            return "Moderate risk - Monitor patient closely"
        else:
            return "Low risk - Safe combination"