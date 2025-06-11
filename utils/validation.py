"""
Validation Utilities for PharmQAgentAI
Input validation and data quality checks
"""
import re
from typing import Dict, List, Any, Tuple

class ValidationUtils:
    """Utility functions for input validation"""
    
    def __init__(self):
        """Initialize validation utilities"""
        self.amino_acids = set('ACDEFGHIKLMNPQRSTVWY')
    
    def validate_input_data(self, data: Dict[str, Any], task: str) -> Tuple[bool, str]:
        """Validate input data for specific prediction tasks"""
        
        if task == "DTI":
            return self._validate_dti_input(data)
        elif task == "DTA":
            return self._validate_dta_input(data)
        elif task == "DDI":
            return self._validate_ddi_input(data)
        elif task == "ADMET":
            return self._validate_admet_input(data)
        elif task == "Similarity":
            return self._validate_similarity_input(data)
        else:
            return False, f"Unknown task: {task}"
    
    def _validate_dti_input(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate DTI prediction input"""
        if 'drug_smiles' not in data:
            return False, "Drug SMILES is required"
        
        if 'target_sequence' not in data:
            return False, "Target protein sequence is required"
        
        if not self.validate_smiles(data['drug_smiles']):
            return False, "Invalid SMILES format"
        
        if not self.validate_protein_sequence(data['target_sequence']):
            return False, "Invalid protein sequence"
        
        return True, "Valid input"
    
    def _validate_dta_input(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate DTA prediction input"""
        return self._validate_dti_input(data)  # Same validation as DTI
    
    def _validate_ddi_input(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate DDI prediction input"""
        if 'drug1_smiles' not in data:
            return False, "First drug SMILES is required"
        
        if 'drug2_smiles' not in data:
            return False, "Second drug SMILES is required"
        
        if not self.validate_smiles(data['drug1_smiles']):
            return False, "Invalid SMILES format for first drug"
        
        if not self.validate_smiles(data['drug2_smiles']):
            return False, "Invalid SMILES format for second drug"
        
        return True, "Valid input"
    
    def _validate_admet_input(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate ADMET prediction input"""
        if 'drug_smiles' not in data:
            return False, "Drug SMILES is required"
        
        if not self.validate_smiles(data['drug_smiles']):
            return False, "Invalid SMILES format"
        
        return True, "Valid input"
    
    def _validate_similarity_input(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate similarity search input"""
        if 'query_smiles' not in data:
            return False, "Query SMILES is required"
        
        if not self.validate_smiles(data['query_smiles']):
            return False, "Invalid SMILES format"
        
        return True, "Valid input"
    
    def validate_smiles(self, smiles: str) -> bool:
        """Validate SMILES notation"""
        if not smiles or not isinstance(smiles, str):
            return False
        
        smiles = smiles.strip()
        if len(smiles) == 0:
            return False
        
        # Basic SMILES validation
        valid_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789()[]=-#@+\\/:.')
        return all(c in valid_chars for c in smiles)
    
    def validate_protein_sequence(self, sequence: str) -> bool:
        """Validate protein amino acid sequence"""
        if not sequence or not isinstance(sequence, str):
            return False
        
        sequence = sequence.upper().strip()
        if len(sequence) == 0:
            return False
        
        return all(aa in self.amino_acids for aa in sequence)
    
    def sanitize_input(self, text: str) -> str:
        """Sanitize text input"""
        if not text:
            return ""
        
        return text.strip()
    
    def validate_model_selection(self, task: str, model_name: str) -> bool:
        """Validate model selection for task"""
        valid_models = {
            "DTI": ["DeepDTI", "GraphDTI"],
            "DTA": ["DeepDTA", "AttentionDTA"],
            "DDI": ["DrugBAN", "MHCADDI"],
            "ADMET": ["ADMETlab", "ChemProp"],
            "Similarity": ["MolBERT", "ChemBERTa"]
        }
        
        return task in valid_models and model_name in valid_models[task]