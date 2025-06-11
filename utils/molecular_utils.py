"""
Molecular utilities for PharmQAgentAI
"""

import re
from typing import List, Dict, Optional

class MolecularUtils:
    """Utility class for molecular operations"""
    
    @staticmethod
    def validate_smiles(smiles: str) -> bool:
        """Validate SMILES notation"""
        if not smiles or not isinstance(smiles, str):
            return False
        
        # Basic SMILES validation
        valid_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789()[]=#+-@./\\')
        return all(c in valid_chars for c in smiles)
    
    @staticmethod
    def validate_protein_sequence(sequence: str) -> bool:
        """Validate protein sequence"""
        if not sequence or not isinstance(sequence, str):
            return False
        
        # Valid amino acid codes
        valid_aa = set('ACDEFGHIKLMNPQRSTVWY')
        return all(c.upper() in valid_aa for c in sequence)
    
    @staticmethod
    def parse_molecular_formula(formula: str) -> Dict[str, int]:
        """Parse molecular formula and return element counts"""
        if not formula:
            return {}
        
        pattern = r'([A-Z][a-z]?)(\d*)'
        matches = re.findall(pattern, formula)
        
        result = {}
        for element, count in matches:
            count = int(count) if count else 1
            result[element] = count
        
        return result
    
    @staticmethod
    def calculate_molecular_weight(formula: str) -> float:
        """Calculate molecular weight from formula"""
        atomic_weights = {
            'H': 1.008, 'C': 12.011, 'N': 14.007, 'O': 15.999,
            'F': 18.998, 'P': 30.974, 'S': 32.065, 'Cl': 35.453,
            'Br': 79.904, 'I': 126.904
        }
        
        elements = MolecularUtils.parse_molecular_formula(formula)
        weight = 0.0
        
        for element, count in elements.items():
            if element in atomic_weights:
                weight += atomic_weights[element] * count
        
        return weight
    
    @staticmethod
    def sanitize_smiles(smiles: str) -> str:
        """Sanitize SMILES string"""
        if not smiles:
            return ""
        return smiles.strip().upper()

# Backward compatibility functions
def validate_smiles(smiles: str) -> bool:
    return MolecularUtils.validate_smiles(smiles)

def validate_protein_sequence(sequence: str) -> bool:
    return MolecularUtils.validate_protein_sequence(sequence)

def parse_molecular_formula(formula: str) -> Dict[str, int]:
    return MolecularUtils.parse_molecular_formula(formula)