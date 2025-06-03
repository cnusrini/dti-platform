import re
import numpy as np
from typing import Dict, List, Optional, Tuple, Union
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MolecularUtils:
    """Utility functions for molecular data processing and analysis"""
    
    def __init__(self):
        # Common SMILES patterns for validation
        self.smiles_pattern = re.compile(r'^[A-Za-z0-9@+\-\[\]()=#\\/\\\\.:]+$')
        
        # Atomic symbols for validation
        self.valid_atoms = {
            'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',
            'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca',
            'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
            'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr',
            'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn',
            'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd',
            'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb',
            'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg',
            'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn'
        }
        
        # Amino acid single letter codes
        self.amino_acids = set('ACDEFGHIKLMNPQRSTVWY')
        
    def validate_smiles(self, smiles: str) -> bool:
        """
        Validate SMILES string format
        
        Args:
            smiles: SMILES string to validate
            
        Returns:
            bool: True if valid SMILES format, False otherwise
        """
        try:
            if not smiles or not isinstance(smiles, str):
                return False
            
            # Remove whitespace
            smiles = smiles.strip()
            
            if len(smiles) == 0:
                return False
            
            # Basic pattern matching
            if not self.smiles_pattern.match(smiles):
                return False
            
            # Check for balanced brackets
            if not self._check_balanced_brackets(smiles):
                return False
            
            # Check for valid atomic symbols
            if not self._check_valid_atoms(smiles):
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"SMILES validation error: {str(e)}")
            return False
    
    def _check_balanced_brackets(self, smiles: str) -> bool:
        """Check if brackets are balanced in SMILES string"""
        bracket_pairs = {'(': ')', '[': ']'}
        stack = []
        
        for char in smiles:
            if char in bracket_pairs:
                stack.append(bracket_pairs[char])
            elif char in bracket_pairs.values():
                if not stack or stack.pop() != char:
                    return False
        
        return len(stack) == 0
    
    def _check_valid_atoms(self, smiles: str) -> bool:
        """Check if SMILES contains valid atomic symbols"""
        # Extract potential atomic symbols
        atom_pattern = re.compile(r'[A-Z][a-z]?')
        atoms = atom_pattern.findall(smiles)
        
        # Check if all found atoms are valid
        for atom in atoms:
            if atom not in self.valid_atoms:
                # Allow some common SMILES-specific symbols
                if atom not in ['Cl', 'Br']:
                    return False
        
        return True
    
    def parse_smiles(self, smiles: str) -> Dict:
        """
        Parse SMILES string and extract basic molecular information
        
        Args:
            smiles: SMILES string to parse
            
        Returns:
            Dict: Molecular information including atoms, bonds, etc.
        """
        try:
            if not self.validate_smiles(smiles):
                return {"error": "Invalid SMILES string"}
            
            # Basic parsing without RDKit
            atoms = re.findall(r'[A-Z][a-z]?', smiles)
            atom_counts = {}
            
            for atom in atoms:
                atom_counts[atom] = atom_counts.get(atom, 0) + 1
            
            # Count bonds (simplified)
            single_bonds = smiles.count('-') if '-' in smiles else len(atoms) - 1
            double_bonds = smiles.count('=')
            triple_bonds = smiles.count('#')
            aromatic_bonds = len(re.findall(r'[a-z]', smiles))
            
            # Estimate molecular weight (simplified)
            atomic_weights = {
                'H': 1.008, 'C': 12.011, 'N': 14.007, 'O': 15.999,
                'F': 18.998, 'P': 30.974, 'S': 32.065, 'Cl': 35.453,
                'Br': 79.904, 'I': 126.904
            }
            
            molecular_weight = sum(
                atomic_weights.get(atom, 12.011) * count
                for atom, count in atom_counts.items()
            )
            
            return {
                "smiles": smiles,
                "atom_counts": atom_counts,
                "total_atoms": sum(atom_counts.values()),
                "bonds": {
                    "single": single_bonds,
                    "double": double_bonds,
                    "triple": triple_bonds,
                    "aromatic": aromatic_bonds
                },
                "estimated_molecular_weight": round(molecular_weight, 2),
                "has_rings": '(' in smiles or ')' in smiles,
                "has_aromatic": any(c.islower() for c in smiles if c.isalpha())
            }
            
        except Exception as e:
            logger.error(f"SMILES parsing error: {str(e)}")
            return {"error": f"Parsing failed: {str(e)}"}
    
    def calculate_molecular_descriptors(self, smiles: str) -> Dict:
        """
        Calculate basic molecular descriptors without RDKit
        
        Args:
            smiles: SMILES string
            
        Returns:
            Dict: Basic molecular descriptors
        """
        try:
            parsed = self.parse_smiles(smiles)
            if "error" in parsed:
                return parsed
            
            atom_counts = parsed["atom_counts"]
            
            # Basic descriptors
            heavy_atoms = sum(count for atom, count in atom_counts.items() if atom != 'H')
            
            # Lipinski's Rule of Five approximations
            estimated_logp = self._estimate_logp(atom_counts)
            hbd = atom_counts.get('O', 0) + atom_counts.get('N', 0)  # Simplified H-bond donors
            hba = atom_counts.get('O', 0) + atom_counts.get('N', 0)  # Simplified H-bond acceptors
            
            # Drug-likeness score (simplified)
            drug_like_score = self._calculate_drug_likeness(
                parsed["estimated_molecular_weight"], estimated_logp, hbd, hba
            )
            
            return {
                "molecular_weight": parsed["estimated_molecular_weight"],
                "heavy_atom_count": heavy_atoms,
                "estimated_logp": round(estimated_logp, 2),
                "hbd": hbd,
                "hba": hba,
                "rotatable_bonds": self._estimate_rotatable_bonds(smiles),
                "aromatic_rings": self._count_aromatic_rings(smiles),
                "drug_likeness_score": round(drug_like_score, 3),
                "lipinski_violations": self._count_lipinski_violations(
                    parsed["estimated_molecular_weight"], estimated_logp, hbd, hba
                )
            }
            
        except Exception as e:
            logger.error(f"Descriptor calculation error: {str(e)}")
            return {"error": f"Calculation failed: {str(e)}"}
    
    def _estimate_logp(self, atom_counts: Dict) -> float:
        """Estimate LogP using simple atomic contributions"""
        # Simplified LogP estimation
        logp_contributions = {
            'C': 0.2, 'H': 0.0, 'N': -0.3, 'O': -0.4,
            'F': 0.0, 'Cl': 0.5, 'Br': 0.7, 'I': 1.0,
            'S': 0.1, 'P': 0.0
        }
        
        logp = sum(
            logp_contributions.get(atom, 0.0) * count
            for atom, count in atom_counts.items()
        )
        
        return logp
    
    def _estimate_rotatable_bonds(self, smiles: str) -> int:
        """Estimate number of rotatable bonds"""
        # Count single bonds between non-terminal carbons (simplified)
        single_bonds = smiles.count('C-C') + smiles.count('C-N') + smiles.count('C-O')
        return max(0, single_bonds - 1)  # Subtract 1 for terminal bonds
    
    def _count_aromatic_rings(self, smiles: str) -> int:
        """Count aromatic rings (simplified)"""
        # Count lowercase letters which typically indicate aromaticity
        aromatic_chars = sum(1 for c in smiles if c.islower() and c.isalpha())
        return aromatic_chars // 6  # Approximate rings (benzene = 6 atoms)
    
    def _calculate_drug_likeness(self, mw: float, logp: float, hbd: int, hba: int) -> float:
        """Calculate a simple drug-likeness score"""
        score = 1.0
        
        # Penalize violations of Lipinski's Rule of Five
        if mw > 500: score -= 0.2
        if logp > 5: score -= 0.2
        if hbd > 5: score -= 0.2
        if hba > 10: score -= 0.2
        
        # Bonus for optimal ranges
        if 150 <= mw <= 350: score += 0.1
        if 1 <= logp <= 3: score += 0.1
        
        return max(0.0, min(1.0, score))
    
    def _count_lipinski_violations(self, mw: float, logp: float, hbd: int, hba: int) -> int:
        """Count violations of Lipinski's Rule of Five"""
        violations = 0
        
        if mw > 500: violations += 1
        if logp > 5: violations += 1
        if hbd > 5: violations += 1
        if hba > 10: violations += 1
        
        return violations
    
    def validate_protein_sequence(self, sequence: str) -> bool:
        """
        Validate protein sequence format
        
        Args:
            sequence: Protein sequence string
            
        Returns:
            bool: True if valid protein sequence, False otherwise
        """
        try:
            if not sequence or not isinstance(sequence, str):
                return False
            
            # Remove whitespace and convert to uppercase
            clean_sequence = ''.join(sequence.split()).upper()
            
            if len(clean_sequence) == 0:
                return False
            
            # Check if all characters are valid amino acids
            return all(aa in self.amino_acids for aa in clean_sequence)
            
        except Exception as e:
            logger.error(f"Protein sequence validation error: {str(e)}")
            return False
    
    def parse_protein_sequence(self, sequence: str) -> Dict:
        """
        Parse protein sequence and extract basic information
        
        Args:
            sequence: Protein sequence string
            
        Returns:
            Dict: Protein sequence information
        """
        try:
            if not self.validate_protein_sequence(sequence):
                return {"error": "Invalid protein sequence"}
            
            clean_sequence = ''.join(sequence.split()).upper()
            
            # Count amino acids
            aa_counts = {}
            for aa in clean_sequence:
                aa_counts[aa] = aa_counts.get(aa, 0) + 1
            
            # Calculate basic properties
            length = len(clean_sequence)
            
            # Estimate molecular weight (average AA weight ~110 Da)
            estimated_mw = length * 110
            
            # Count hydrophobic residues
            hydrophobic = set('AILMFWYV')
            hydrophobic_count = sum(aa_counts.get(aa, 0) for aa in hydrophobic)
            hydrophobicity = hydrophobic_count / length if length > 0 else 0
            
            # Count charged residues
            positive = set('KRH')
            negative = set('DE')
            positive_count = sum(aa_counts.get(aa, 0) for aa in positive)
            negative_count = sum(aa_counts.get(aa, 0) for aa in negative)
            net_charge = positive_count - negative_count
            
            return {
                "sequence": clean_sequence,
                "length": length,
                "amino_acid_counts": aa_counts,
                "estimated_molecular_weight": estimated_mw,
                "hydrophobicity": round(hydrophobicity, 3),
                "net_charge": net_charge,
                "positive_residues": positive_count,
                "negative_residues": negative_count,
                "composition": {
                    "hydrophobic": round(hydrophobicity, 3),
                    "polar": round((aa_counts.get('S', 0) + aa_counts.get('T', 0) + 
                                  aa_counts.get('N', 0) + aa_counts.get('Q', 0)) / length, 3),
                    "charged": round((positive_count + negative_count) / length, 3)
                }
            }
            
        except Exception as e:
            logger.error(f"Protein sequence parsing error: {str(e)}")
            return {"error": f"Parsing failed: {str(e)}"}
    
    def calculate_similarity(self, smiles1: str, smiles2: str, method: str = "Tanimoto") -> float:
        """
        Calculate molecular similarity between two SMILES strings
        
        Args:
            smiles1: First SMILES string
            smiles2: Second SMILES string
            method: Similarity method (Tanimoto, Dice, etc.)
            
        Returns:
            float: Similarity score (0-1)
        """
        try:
            if not self.validate_smiles(smiles1) or not self.validate_smiles(smiles2):
                return 0.0
            
            # Simple fingerprint-like similarity based on atom composition
            parsed1 = self.parse_smiles(smiles1)
            parsed2 = self.parse_smiles(smiles2)
            
            if "error" in parsed1 or "error" in parsed2:
                return 0.0
            
            atoms1 = set(parsed1["atom_counts"].keys())
            atoms2 = set(parsed2["atom_counts"].keys())
            
            if method.lower() == "tanimoto":
                intersection = len(atoms1.intersection(atoms2))
                union = len(atoms1.union(atoms2))
                return intersection / union if union > 0 else 0.0
            
            elif method.lower() == "dice":
                intersection = len(atoms1.intersection(atoms2))
                return 2 * intersection / (len(atoms1) + len(atoms2)) if (len(atoms1) + len(atoms2)) > 0 else 0.0
            
            elif method.lower() == "cosine":
                # Convert to vectors for cosine similarity
                all_atoms = atoms1.union(atoms2)
                vec1 = [parsed1["atom_counts"].get(atom, 0) for atom in all_atoms]
                vec2 = [parsed2["atom_counts"].get(atom, 0) for atom in all_atoms]
                
                dot_product = sum(a * b for a, b in zip(vec1, vec2))
                norm1 = sum(a * a for a in vec1) ** 0.5
                norm2 = sum(b * b for b in vec2) ** 0.5
                
                return dot_product / (norm1 * norm2) if norm1 * norm2 > 0 else 0.0
            
            else:
                # Default to Tanimoto
                return self.calculate_similarity(smiles1, smiles2, "Tanimoto")
            
        except Exception as e:
            logger.error(f"Similarity calculation error: {str(e)}")
            return 0.0
    
    def normalize_smiles(self, smiles: str) -> str:
        """
        Normalize SMILES string (basic cleanup)
        
        Args:
            smiles: Input SMILES string
            
        Returns:
            str: Normalized SMILES string
        """
        try:
            if not smiles:
                return ""
            
            # Remove extra whitespace
            normalized = smiles.strip()
            
            # Remove redundant parentheses (basic)
            normalized = re.sub(r'\(\)', '', normalized)
            
            return normalized
            
        except Exception as e:
            logger.error(f"SMILES normalization error: {str(e)}")
            return smiles
