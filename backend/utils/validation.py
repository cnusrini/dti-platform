import re
import json
from typing import Any, Dict, List, Optional, Union
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ValidationUtils:
    """Utility functions for input validation and data sanitization"""
    
    def __init__(self):
        # Validation patterns
        self.smiles_pattern = re.compile(r'^[A-Za-z0-9@+\-\[\]()=#\\/\\\\.:]+$')
        self.amino_acid_pattern = re.compile(r'^[ACDEFGHIKLMNPQRSTVWY\s]+$', re.IGNORECASE)
        self.float_pattern = re.compile(r'^-?\d+\.?\d*$')
        self.int_pattern = re.compile(r'^-?\d+$')
        
        # Valid atomic symbols for SMILES validation
        self.valid_atoms = {
            'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',
            'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca',
            'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
            'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr',
            'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn',
            'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba'
        }
        
        # Valid amino acid codes
        self.amino_acids = set('ACDEFGHIKLMNPQRSTVWY')
        
        # Common ADMET properties
        self.valid_admet_properties = {
            'absorption', 'distribution', 'metabolism', 'excretion', 'toxicity',
            'ld50', 'logp', 'solubility', 'bioavailability', 'clearance',
            'half_life', 'permeability', 'protein_binding'
        }
        
        # Valid similarity methods
        self.valid_similarity_methods = {'tanimoto', 'dice', 'cosine', 'euclidean', 'jaccard'}
        
        # Valid interaction types
        self.valid_interaction_types = {
            'synergistic', 'antagonistic', 'additive', 'unknown', 'competitive',
            'non-competitive', 'uncompetitive'
        }
        
        # Valid affinity types
        self.valid_affinity_types = {'ic50', 'kd', 'ki', 'ec50', 'ka'}
    
    def validate_smiles(self, smiles: str) -> bool:
        """
        Validate SMILES string format and structure
        
        Args:
            smiles: SMILES string to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            if not smiles or not isinstance(smiles, str):
                return False
            
            # Remove whitespace and check length
            smiles = smiles.strip()
            if len(smiles) == 0 or len(smiles) > 2000:  # Reasonable length limit
                return False
            
            # Basic pattern check
            if not self.smiles_pattern.match(smiles):
                return False
            
            # Check for balanced brackets
            if not self._validate_brackets(smiles):
                return False
            
            # Check for valid atomic symbols
            if not self._validate_atoms_in_smiles(smiles):
                return False
            
            # Check for basic SMILES rules
            return self._validate_smiles_structure(smiles)
            
        except Exception as e:
            logger.error(f"SMILES validation error: {str(e)}")
            return False
    
    def _validate_brackets(self, smiles: str) -> bool:
        """Validate bracket matching in SMILES"""
        stack = []
        bracket_pairs = {'(': ')', '[': ']'}
        
        for char in smiles:
            if char in bracket_pairs:
                stack.append(bracket_pairs[char])
            elif char in bracket_pairs.values():
                if not stack or stack.pop() != char:
                    return False
        
        return len(stack) == 0
    
    def _validate_atoms_in_smiles(self, smiles: str) -> bool:
        """Validate atomic symbols in SMILES"""
        # Extract atomic symbols (uppercase followed by optional lowercase)
        atom_matches = re.findall(r'[A-Z][a-z]?', smiles)
        
        for atom in atom_matches:
            if atom not in self.valid_atoms:
                return False
        
        return True
    
    def _validate_smiles_structure(self, smiles: str) -> bool:
        """Validate basic SMILES structural rules"""
        # Check for consecutive operators
        invalid_patterns = ['==', '##', '--', '++']
        for pattern in invalid_patterns:
            if pattern in smiles:
                return False
        
        # Check for proper ring closure
        ring_digits = re.findall(r'\d', smiles)
        if ring_digits:
            digit_counts = {}
            for digit in ring_digits:
                digit_counts[digit] = digit_counts.get(digit, 0) + 1
            
            # Each ring closure digit should appear exactly twice
            for count in digit_counts.values():
                if count != 2:
                    return False
        
        return True
    
    def validate_protein_sequence(self, sequence: str) -> bool:
        """
        Validate protein sequence format
        
        Args:
            sequence: Protein sequence to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            if not sequence or not isinstance(sequence, str):
                return False
            
            # Remove whitespace and convert to uppercase
            clean_sequence = ''.join(sequence.split()).upper()
            
            # Check length limits
            if len(clean_sequence) == 0 or len(clean_sequence) > 50000:  # Reasonable protein length
                return False
            
            # Check if all characters are valid amino acids
            return all(aa in self.amino_acids for aa in clean_sequence)
            
        except Exception as e:
            logger.error(f"Protein sequence validation error: {str(e)}")
            return False
    
    def validate_numerical_input(self, value: Any, min_val: Optional[float] = None, 
                                max_val: Optional[float] = None, 
                                allow_negative: bool = True) -> bool:
        """
        Validate numerical input
        
        Args:
            value: Value to validate
            min_val: Minimum allowed value
            max_val: Maximum allowed value
            allow_negative: Whether negative values are allowed
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            # Convert to float if string
            if isinstance(value, str):
                if not self.float_pattern.match(value.strip()):
                    return False
                value = float(value.strip())
            
            if not isinstance(value, (int, float)):
                return False
            
            # Check if number is valid (not NaN or infinity)
            if not (isinstance(value, (int, float)) and 
                   not (isinstance(value, float) and (value != value or abs(value) == float('inf')))):
                return False
            
            # Check negative values
            if not allow_negative and value < 0:
                return False
            
            # Check range
            if min_val is not None and value < min_val:
                return False
            
            if max_val is not None and value > max_val:
                return False
            
            return True
            
        except (ValueError, TypeError) as e:
            logger.error(f"Numerical validation error: {str(e)}")
            return False
    
    def validate_admet_properties(self, properties: List[str]) -> bool:
        """
        Validate ADMET property list
        
        Args:
            properties: List of ADMET properties to validate
            
        Returns:
            bool: True if all properties are valid, False otherwise
        """
        try:
            if not properties or not isinstance(properties, list):
                return False
            
            if len(properties) == 0 or len(properties) > 20:  # Reasonable limit
                return False
            
            # Check if all properties are valid
            normalized_props = [prop.lower().strip() for prop in properties]
            return all(prop in self.valid_admet_properties for prop in normalized_props)
            
        except Exception as e:
            logger.error(f"ADMET properties validation error: {str(e)}")
            return False
    
    def validate_similarity_method(self, method: str) -> bool:
        """
        Validate similarity calculation method
        
        Args:
            method: Similarity method to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            if not method or not isinstance(method, str):
                return False
            
            return method.lower().strip() in self.valid_similarity_methods
            
        except Exception as e:
            logger.error(f"Similarity method validation error: {str(e)}")
            return False
    
    def validate_interaction_type(self, interaction_type: str) -> bool:
        """
        Validate drug interaction type
        
        Args:
            interaction_type: Interaction type to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            if not interaction_type or not isinstance(interaction_type, str):
                return False
            
            return interaction_type.lower().strip() in self.valid_interaction_types
            
        except Exception as e:
            logger.error(f"Interaction type validation error: {str(e)}")
            return False
    
    def validate_affinity_type(self, affinity_type: str) -> bool:
        """
        Validate binding affinity type
        
        Args:
            affinity_type: Affinity type to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            if not affinity_type or not isinstance(affinity_type, str):
                return False
            
            return affinity_type.lower().strip() in self.valid_affinity_types
            
        except Exception as e:
            logger.error(f"Affinity type validation error: {str(e)}")
            return False
    
    def sanitize_input(self, input_text: str, max_length: int = 10000) -> str:
        """
        Sanitize input text to prevent injection attacks
        
        Args:
            input_text: Text to sanitize
            max_length: Maximum allowed length
            
        Returns:
            str: Sanitized text
        """
        try:
            if not input_text or not isinstance(input_text, str):
                return ""
            
            # Remove null bytes
            sanitized = input_text.replace('\x00', '')
            
            # Limit length
            if len(sanitized) > max_length:
                sanitized = sanitized[:max_length]
            
            # Remove potentially dangerous characters for file operations
            dangerous_chars = ['<', '>', '|', '&', ';', '`', '$']
            for char in dangerous_chars:
                sanitized = sanitized.replace(char, '')
            
            return sanitized.strip()
            
        except Exception as e:
            logger.error(f"Input sanitization error: {str(e)}")
            return ""
    
    def validate_file_upload(self, file_content: str, allowed_extensions: List[str], 
                           max_size_mb: float = 10.0) -> Dict[str, Any]:
        """
        Validate uploaded file content
        
        Args:
            file_content: Content of uploaded file
            allowed_extensions: List of allowed file extensions
            max_size_mb: Maximum file size in MB
            
        Returns:
            Dict: Validation result with status and details
        """
        try:
            result = {"valid": False, "error": None, "warnings": []}
            
            if not file_content:
                result["error"] = "Empty file content"
                return result
            
            # Check file size
            file_size_mb = len(file_content.encode('utf-8')) / (1024 * 1024)
            if file_size_mb > max_size_mb:
                result["error"] = f"File too large: {file_size_mb:.2f}MB > {max_size_mb}MB"
                return result
            
            # Check for binary content
            try:
                file_content.encode('utf-8')
            except UnicodeEncodeError:
                result["error"] = "File contains binary data"
                return result
            
            # Count lines
            lines = file_content.split('\n')
            if len(lines) > 10000:  # Reasonable limit
                result["warnings"].append(f"Large file with {len(lines)} lines")
            
            result["valid"] = True
            result["lines"] = len(lines)
            result["size_mb"] = file_size_mb
            
            return result
            
        except Exception as e:
            logger.error(f"File validation error: {str(e)}")
            return {"valid": False, "error": f"Validation failed: {str(e)}"}
    
    def validate_prediction_parameters(self, task: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate prediction parameters for specific tasks
        
        Args:
            task: Prediction task (DTI, DTA, etc.)
            parameters: Parameters to validate
            
        Returns:
            Dict: Validation result
        """
        try:
            result = {"valid": True, "errors": [], "warnings": []}
            
            if task.upper() == 'DTI':
                # Validate DTI parameters
                if 'drug_smiles' in parameters:
                    if not self.validate_smiles(parameters['drug_smiles']):
                        result["errors"].append("Invalid drug SMILES")
                        result["valid"] = False
                
                if 'target_sequence' in parameters:
                    if not self.validate_protein_sequence(parameters['target_sequence']):
                        result["errors"].append("Invalid protein sequence")
                        result["valid"] = False
            
            elif task.upper() == 'DTA':
                # Validate DTA parameters
                if 'drug_smiles' in parameters:
                    if not self.validate_smiles(parameters['drug_smiles']):
                        result["errors"].append("Invalid drug SMILES")
                        result["valid"] = False
                
                if 'target_sequence' in parameters:
                    if not self.validate_protein_sequence(parameters['target_sequence']):
                        result["errors"].append("Invalid protein sequence")
                        result["valid"] = False
                
                if 'affinity_type' in parameters:
                    if not self.validate_affinity_type(parameters['affinity_type']):
                        result["errors"].append("Invalid affinity type")
                        result["valid"] = False
            
            elif task.upper() == 'DDI':
                # Validate DDI parameters
                for drug_key in ['drug1_smiles', 'drug2_smiles']:
                    if drug_key in parameters:
                        if not self.validate_smiles(parameters[drug_key]):
                            result["errors"].append(f"Invalid {drug_key}")
                            result["valid"] = False
                
                if 'interaction_type' in parameters:
                    if not self.validate_interaction_type(parameters['interaction_type']):
                        result["errors"].append("Invalid interaction type")
                        result["valid"] = False
            
            elif task.upper() == 'ADMET':
                # Validate ADMET parameters
                if 'drug_smiles' in parameters:
                    if not self.validate_smiles(parameters['drug_smiles']):
                        result["errors"].append("Invalid drug SMILES")
                        result["valid"] = False
                
                if 'properties' in parameters:
                    if not self.validate_admet_properties(parameters['properties']):
                        result["errors"].append("Invalid ADMET properties")
                        result["valid"] = False
            
            elif task.upper() == 'SIMILARITY':
                # Validate similarity parameters
                if 'query_smiles' in parameters:
                    if not self.validate_smiles(parameters['query_smiles']):
                        result["errors"].append("Invalid query SMILES")
                        result["valid"] = False
                
                if 'method' in parameters:
                    if not self.validate_similarity_method(parameters['method']):
                        result["errors"].append("Invalid similarity method")
                        result["valid"] = False
                
                if 'threshold' in parameters:
                    if not self.validate_numerical_input(parameters['threshold'], 0.0, 1.0):
                        result["errors"].append("Invalid similarity threshold (must be 0-1)")
                        result["valid"] = False
                
                if 'max_results' in parameters:
                    if not self.validate_numerical_input(parameters['max_results'], 1, 1000, False):
                        result["errors"].append("Invalid max_results (must be 1-1000)")
                        result["valid"] = False
            
            return result
            
        except Exception as e:
            logger.error(f"Parameter validation error: {str(e)}")
            return {"valid": False, "errors": [f"Validation failed: {str(e)}"]}
    
    def create_validation_report(self, validations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a comprehensive validation report
        
        Args:
            validations: List of validation results
            
        Returns:
            Dict: Comprehensive validation report
        """
        try:
            report = {
                "overall_valid": True,
                "total_validations": len(validations),
                "passed_validations": 0,
                "failed_validations": 0,
                "warnings_count": 0,
                "errors": [],
                "warnings": [],
                "details": validations
            }
            
            for validation in validations:
                if validation.get("valid", False):
                    report["passed_validations"] += 1
                else:
                    report["failed_validations"] += 1
                    report["overall_valid"] = False
                
                # Collect errors and warnings
                if "errors" in validation:
                    report["errors"].extend(validation["errors"])
                elif "error" in validation and validation["error"]:
                    report["errors"].append(validation["error"])
                
                if "warnings" in validation:
                    report["warnings"].extend(validation["warnings"])
                    report["warnings_count"] += len(validation["warnings"])
            
            return report
            
        except Exception as e:
            logger.error(f"Validation report creation error: {str(e)}")
            return {
                "overall_valid": False,
                "error": f"Report generation failed: {str(e)}"
            }
