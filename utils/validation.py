"""
Validation utilities for PharmQAgentAI
"""

from typing import Dict, Any, List, Optional
import re

class ValidationUtils:
    """Utility class for input validation"""
    
    @staticmethod
    def validate_input_data(task_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate input data for prediction tasks"""
        result = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        if task_type == "DTI":
            if not data.get('drug_smiles'):
                result['errors'].append("Drug SMILES is required")
            elif not ValidationUtils.validate_smiles(data['drug_smiles']):
                result['errors'].append("Invalid SMILES format")
                
            if not data.get('target_sequence'):
                result['errors'].append("Target protein sequence is required")
            elif not ValidationUtils.validate_protein_sequence(data['target_sequence']):
                result['errors'].append("Invalid protein sequence")
        
        elif task_type == "DTA":
            if not data.get('drug_smiles'):
                result['errors'].append("Drug SMILES is required")
            elif not ValidationUtils.validate_smiles(data['drug_smiles']):
                result['errors'].append("Invalid SMILES format")
                
            if not data.get('target_sequence'):
                result['errors'].append("Target protein sequence is required")
            elif not ValidationUtils.validate_protein_sequence(data['target_sequence']):
                result['errors'].append("Invalid protein sequence")
        
        elif task_type == "DDI":
            if not data.get('drug1_smiles'):
                result['errors'].append("First drug SMILES is required")
            elif not ValidationUtils.validate_smiles(data['drug1_smiles']):
                result['errors'].append("Invalid SMILES format for first drug")
                
            if not data.get('drug2_smiles'):
                result['errors'].append("Second drug SMILES is required")
            elif not ValidationUtils.validate_smiles(data['drug2_smiles']):
                result['errors'].append("Invalid SMILES format for second drug")
        
        elif task_type == "ADMET":
            if not data.get('drug_smiles'):
                result['errors'].append("Drug SMILES is required")
            elif not ValidationUtils.validate_smiles(data['drug_smiles']):
                result['errors'].append("Invalid SMILES format")
        
        elif task_type == "SIMILARITY":
            if not data.get('query_smiles'):
                result['errors'].append("Query SMILES is required")
            elif not ValidationUtils.validate_smiles(data['query_smiles']):
                result['errors'].append("Invalid SMILES format")
        
        result['valid'] = len(result['errors']) == 0
        return result
    
    @staticmethod
    def validate_smiles(smiles: str) -> bool:
        """Validate SMILES notation"""
        if not smiles or not isinstance(smiles, str):
            return False
        
        valid_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789()[]=#+-@./\\')
        return all(c in valid_chars for c in smiles)
    
    @staticmethod
    def validate_protein_sequence(sequence: str) -> bool:
        """Validate protein sequence"""
        if not sequence or not isinstance(sequence, str):
            return False
        
        valid_aa = set('ACDEFGHIKLMNPQRSTVWY')
        return all(c.upper() in valid_aa for c in sequence)
    
    @staticmethod
    def validate_model_selection(task: str, model: str) -> bool:
        """Validate model selection for task"""
        valid_models = {
            "DTI": ["BioBERT-DTI", "DeepDTI", "GraphConv-DTI"],
            "DTA": ["DeepDTA", "GraphDTA", "AttentionDTA"],
            "DDI": ["DeepDDI", "MHCADDI", "GraphDDI"],
            "ADMET": ["ADMETlab", "DeepADMET", "GraphADMET"],
            "SIMILARITY": ["Morgan", "MACCS", "RDKit"]
        }
        
        return task in valid_models and model in valid_models[task]

# Backward compatibility functions
def validate_input_data(task_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
    return ValidationUtils.validate_input_data(task_type, data)

def validate_smiles(smiles: str) -> bool:
    return ValidationUtils.validate_smiles(smiles)

def validate_protein_sequence(sequence: str) -> bool:
    return ValidationUtils.validate_protein_sequence(sequence)