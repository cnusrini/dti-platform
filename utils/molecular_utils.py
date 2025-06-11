"""
Molecular Utilities for PharmQAgentAI
Handles molecular data processing and validation
"""
import re
from typing import List, Dict, Any, Optional

class MolecularUtils:
    """Utility functions for molecular data processing"""
    
    def __init__(self):
        """Initialize molecular utilities"""
        pass
    
    def validate_smiles(self, smiles: str) -> bool:
        """Validate SMILES notation"""
        if not smiles or not isinstance(smiles, str):
            return False
        
        # Basic SMILES validation
        if len(smiles.strip()) == 0:
            return False
            
        # Check for valid characters
        valid_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789()[]=-#@+\\/:.')
        if not all(c in valid_chars for c in smiles):
            return False
            
        return True
    
    def validate_protein_sequence(self, sequence: str) -> bool:
        """Validate protein amino acid sequence"""
        if not sequence or not isinstance(sequence, str):
            return False
        
        # Standard amino acid codes
        amino_acids = set('ACDEFGHIKLMNPQRSTVWY')
        sequence = sequence.upper().strip()
        
        if len(sequence) == 0:
            return False
            
        return all(aa in amino_acids for aa in sequence)
    
    def clean_smiles(self, smiles: str) -> str:
        """Clean and normalize SMILES string"""
        if not smiles:
            return ""
        
        return smiles.strip()
    
    def clean_protein_sequence(self, sequence: str) -> str:
        """Clean and normalize protein sequence"""
        if not sequence:
            return ""
        
        # Remove whitespace and convert to uppercase
        cleaned = re.sub(r'\s+', '', sequence.upper())
        return cleaned
    
    def get_molecular_properties(self, smiles: str) -> Dict[str, Any]:
        """Get basic molecular properties from SMILES"""
        if not self.validate_smiles(smiles):
            return {"error": "Invalid SMILES"}
        
        # Mock molecular properties calculation
        import random
        
        properties = {
            "molecular_weight": round(random.uniform(100, 800), 2),
            "logp": round(random.uniform(-2, 6), 2),
            "num_atoms": random.randint(10, 50),
            "num_bonds": random.randint(9, 55),
            "rotatable_bonds": random.randint(0, 15),
            "hydrogen_donors": random.randint(0, 8),
            "hydrogen_acceptors": random.randint(0, 12)
        }
        
        return properties
    
    def calculate_similarity(self, smiles1: str, smiles2: str) -> float:
        """Calculate molecular similarity between two SMILES"""
        if not (self.validate_smiles(smiles1) and self.validate_smiles(smiles2)):
            return 0.0
        
        # Mock similarity calculation
        import random
        return round(random.uniform(0.1, 0.9), 3)
    
    def normalize_smiles(self, smiles: str) -> str:
        """Normalize SMILES representation"""
        return self.clean_smiles(smiles)
    
    def parse_smiles_list(self, smiles_text: str) -> List[str]:
        """Parse multiple SMILES from text input"""
        if not smiles_text:
            return []
        
        lines = smiles_text.strip().split('\n')
        smiles_list = []
        
        for line in lines:
            cleaned = line.strip()
            if cleaned and self.validate_smiles(cleaned):
                smiles_list.append(cleaned)
        
        return smiles_list