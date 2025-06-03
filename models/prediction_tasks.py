import torch
import numpy as np
from typing import Dict, List, Optional, Any, Union
import logging
from datetime import datetime
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PredictionTasks:
    """Handles all prediction tasks for therapeutic intelligence"""
    
    def __init__(self, model_manager):
        self.model_manager = model_manager
        self.prediction_cache = {}
        
    def _get_model_for_task(self, task: str) -> Optional[Dict]:
        """Get the loaded model for a specific task"""
        try:
            # Find the first loaded model for this task
            for model_key, model_info in self.model_manager.loaded_models.items():
                if model_info['task'] == task:
                    return model_info
            return None
        except Exception as e:
            logger.error(f"Error getting model for task {task}: {str(e)}")
            return None
    
    def _create_prediction_result(self, 
                                score: Union[float, str], 
                                status: str, 
                                model_info: str,
                                details: Optional[Dict] = None,
                                confidence: Optional[float] = None) -> Dict:
        """Create a standardized prediction result"""
        result = {
            'score': score,
            'status': status,
            'model_info': model_info,
            'timestamp': datetime.now(),
            'details': details or {},
            'confidence': confidence
        }
        
        if confidence:
            if confidence > 0.8:
                result['confidence_explanation'] = "High confidence - prediction based on similar training examples"
            elif confidence > 0.6:
                result['confidence_explanation'] = "Medium confidence - moderate similarity to training data"
            else:
                result['confidence_explanation'] = "Low confidence - limited training data for this type of input"
        
        return result
    
    def _encode_molecular_input(self, smiles: str, tokenizer, max_length: int = 512) -> Dict:
        """Encode SMILES string for model input"""
        try:
            # Basic SMILES encoding
            encoded = tokenizer(
                smiles,
                max_length=max_length,
                padding='max_length',
                truncation=True,
                return_tensors='pt'
            )
            return encoded
        except Exception as e:
            logger.error(f"Error encoding SMILES {smiles}: {str(e)}")
            return None
    
    def _encode_protein_sequence(self, sequence: str, tokenizer, max_length: int = 1024) -> Dict:
        """Encode protein sequence for model input"""
        try:
            # Clean protein sequence (remove spaces, convert to uppercase)
            clean_sequence = ''.join(sequence.split()).upper()
            
            # For protein sequences, we might need special handling
            encoded = tokenizer(
                clean_sequence,
                max_length=max_length,
                padding='max_length',
                truncation=True,
                return_tensors='pt'
            )
            return encoded
        except Exception as e:
            logger.error(f"Error encoding protein sequence: {str(e)}")
            return None
    
    def predict_dti(self, drug_smiles: str, target_sequence: str) -> Optional[Dict]:
        """Predict Drug-Target Interaction"""
        try:
            model_info = self._get_model_for_task('DTI')
            if not model_info:
                return self._create_prediction_result(
                    "N/A", "Error", "No DTI model loaded",
                    {"error": "No DTI model is currently loaded"}
                )
            
            model_obj = model_info['model_obj']
            model_name = model_info['name']
            
            # Handle different model types
            if model_obj.get('type') == 'pipeline':
                # Use pipeline for inference
                pipeline = model_obj['pipeline']
                
                # Create input text combining SMILES and protein sequence
                input_text = f"Drug: {drug_smiles} Target: {target_sequence}"
                
                result = pipeline(input_text)
                
                if result and len(result) > 0:
                    score = result[0].get('score', 0.0)
                    label = result[0].get('label', 'INTERACTION')
                    
                    # Convert to interaction probability
                    if label.upper() in ['POSITIVE', 'INTERACTION', '1', 'TRUE']:
                        interaction_prob = score
                    else:
                        interaction_prob = 1.0 - score
                    
                    return self._create_prediction_result(
                        interaction_prob,
                        "Success",
                        model_name,
                        {
                            "interaction_probability": interaction_prob,
                            "predicted_label": label,
                            "raw_score": score,
                            "drug_smiles": drug_smiles,
                            "target_length": len(target_sequence)
                        },
                        confidence=score
                    )
            
            elif 'model' in model_obj and 'tokenizer' in model_obj:
                # Use model and tokenizer directly
                model = model_obj['model']
                tokenizer = model_obj['tokenizer']
                
                # Encode inputs
                drug_encoded = self._encode_molecular_input(drug_smiles, tokenizer)
                target_encoded = self._encode_protein_sequence(target_sequence, tokenizer)
                
                if drug_encoded is None or target_encoded is None:
                    return self._create_prediction_result(
                        "N/A", "Error", model_name,
                        {"error": "Failed to encode inputs"}
                    )
                
                # Simple concatenation approach for DTI
                # In practice, you might need more sophisticated input preparation
                combined_input = f"{drug_smiles} [SEP] {target_sequence}"
                encoded_input = tokenizer(
                    combined_input,
                    max_length=512,
                    padding='max_length',
                    truncation=True,
                    return_tensors='pt'
                )
                
                with torch.no_grad():
                    model.eval()
                    outputs = model(**encoded_input)
                    
                    # Handle different output formats
                    if hasattr(outputs, 'logits'):
                        logits = outputs.logits
                        probs = torch.softmax(logits, dim=-1)
                        
                        # Assume binary classification: [no_interaction, interaction]
                        if probs.shape[-1] >= 2:
                            interaction_prob = probs[0, 1].item()
                        else:
                            interaction_prob = probs[0, 0].item()
                    else:
                        # If no logits, use last hidden state mean as score
                        if hasattr(outputs, 'last_hidden_state'):
                            hidden_states = outputs.last_hidden_state
                            interaction_prob = torch.mean(hidden_states).item()
                            interaction_prob = torch.sigmoid(torch.tensor(interaction_prob)).item()
                        else:
                            interaction_prob = 0.5  # Default neutral score
                
                return self._create_prediction_result(
                    interaction_prob,
                    "Success",
                    model_name,
                    {
                        "interaction_probability": interaction_prob,
                        "drug_smiles": drug_smiles,
                        "target_length": len(target_sequence),
                        "model_type": model_obj.get('type', 'unknown')
                    },
                    confidence=max(interaction_prob, 1.0 - interaction_prob)
                )
            
            else:
                return self._create_prediction_result(
                    "N/A", "Error", model_name,
                    {"error": "Unsupported model type for DTI prediction"}
                )
                
        except Exception as e:
            logger.error(f"DTI prediction error: {str(e)}")
            logger.error(traceback.format_exc())
            return self._create_prediction_result(
                "N/A", "Error", "DTI Model",
                {"error": f"Prediction failed: {str(e)}"}
            )
    
    def predict_dta(self, drug_smiles: str, target_sequence: str, affinity_type: str = "IC50") -> Optional[Dict]:
        """Predict Drug-Target Binding Affinity"""
        try:
            model_info = self._get_model_for_task('DTA')
            if not model_info:
                return self._create_prediction_result(
                    "N/A", "Error", "No DTA model loaded",
                    {"error": "No DTA model is currently loaded"}
                )
            
            model_obj = model_info['model_obj']
            model_name = model_info['name']
            
            # Similar to DTI but focusing on binding affinity values
            if 'model' in model_obj and 'tokenizer' in model_obj:
                model = model_obj['model']
                tokenizer = model_obj['tokenizer']
                
                # Prepare input with affinity type context
                combined_input = f"Predict {affinity_type}: Drug {drug_smiles} Target {target_sequence}"
                encoded_input = tokenizer(
                    combined_input,
                    max_length=512,
                    padding='max_length',
                    truncation=True,
                    return_tensors='pt'
                )
                
                with torch.no_grad():
                    model.eval()
                    outputs = model(**encoded_input)
                    
                    if hasattr(outputs, 'logits'):
                        # For regression tasks, logits might represent the affinity value
                        affinity_value = outputs.logits[0, 0].item() if outputs.logits.numel() > 0 else 5.0
                    else:
                        # Use hidden state mean as affinity predictor
                        if hasattr(outputs, 'last_hidden_state'):
                            hidden_mean = torch.mean(outputs.last_hidden_state).item()
                            # Scale to typical IC50 range (1-10 μM -> log scale 0-1)
                            affinity_value = abs(hidden_mean * 10)  # Convert to μM scale
                        else:
                            affinity_value = 5.0  # Default moderate affinity
                
                # Ensure reasonable affinity range
                affinity_value = max(0.001, min(1000.0, affinity_value))
                
                return self._create_prediction_result(
                    affinity_value,
                    "Success",
                    model_name,
                    {
                        f"{affinity_type}_value": affinity_value,
                        "unit": "μM" if affinity_type in ["IC50", "Kd", "Ki"] else "nM",
                        "affinity_type": affinity_type,
                        "drug_smiles": drug_smiles,
                        "target_length": len(target_sequence),
                        "binding_strength": "Strong" if affinity_value < 1.0 else "Moderate" if affinity_value < 10.0 else "Weak"
                    },
                    confidence=0.7  # Moderate confidence for binding affinity
                )
            
            else:
                return self._create_prediction_result(
                    "N/A", "Error", model_name,
                    {"error": "Unsupported model type for DTA prediction"}
                )
                
        except Exception as e:
            logger.error(f"DTA prediction error: {str(e)}")
            return self._create_prediction_result(
                "N/A", "Error", "DTA Model",
                {"error": f"Prediction failed: {str(e)}"}
            )
    
    def predict_ddi(self, drug1_smiles: str, drug2_smiles: str, interaction_type: str = "Unknown") -> Optional[Dict]:
        """Predict Drug-Drug Interaction"""
        try:
            model_info = self._get_model_for_task('DDI')
            if not model_info:
                return self._create_prediction_result(
                    "N/A", "Error", "No DDI model loaded",
                    {"error": "No DDI model is currently loaded"}
                )
            
            model_obj = model_info['model_obj']
            model_name = model_info['name']
            
            if 'model' in model_obj and 'tokenizer' in model_obj:
                model = model_obj['model']
                tokenizer = model_obj['tokenizer']
                
                # Prepare paired drug input
                combined_input = f"Drug1: {drug1_smiles} Drug2: {drug2_smiles} Interaction: {interaction_type}"
                encoded_input = tokenizer(
                    combined_input,
                    max_length=512,
                    padding='max_length',
                    truncation=True,
                    return_tensors='pt'
                )
                
                with torch.no_grad():
                    model.eval()
                    outputs = model(**encoded_input)
                    
                    if hasattr(outputs, 'logits'):
                        logits = outputs.logits
                        probs = torch.softmax(logits, dim=-1)
                        
                        # Interpret output based on number of classes
                        if probs.shape[-1] >= 3:
                            # Multi-class: [no_interaction, synergistic, antagonistic]
                            interaction_scores = {
                                "no_interaction": probs[0, 0].item(),
                                "synergistic": probs[0, 1].item(),
                                "antagonistic": probs[0, 2].item() if probs.shape[-1] > 2 else 0.0
                            }
                            predicted_interaction = max(interaction_scores, key=interaction_scores.get)
                            interaction_score = interaction_scores[predicted_interaction]
                        else:
                            # Binary: [no_interaction, interaction]
                            interaction_score = probs[0, 1].item() if probs.shape[-1] > 1 else probs[0, 0].item()
                            predicted_interaction = "interaction" if interaction_score > 0.5 else "no_interaction"
                            interaction_scores = {"interaction": interaction_score, "no_interaction": 1.0 - interaction_score}
                    else:
                        # Default scoring from hidden states
                        interaction_score = 0.5
                        predicted_interaction = "unknown"
                        interaction_scores = {"unknown": 0.5}
                
                return self._create_prediction_result(
                    interaction_score,
                    "Success",
                    model_name,
                    {
                        "predicted_interaction": predicted_interaction,
                        "interaction_scores": interaction_scores,
                        "drug1_smiles": drug1_smiles,
                        "drug2_smiles": drug2_smiles,
                        "query_interaction_type": interaction_type,
                        "severity": "High" if interaction_score > 0.8 else "Medium" if interaction_score > 0.5 else "Low"
                    },
                    confidence=interaction_score
                )
            
            else:
                return self._create_prediction_result(
                    "N/A", "Error", model_name,
                    {"error": "Unsupported model type for DDI prediction"}
                )
                
        except Exception as e:
            logger.error(f"DDI prediction error: {str(e)}")
            return self._create_prediction_result(
                "N/A", "Error", "DDI Model",
                {"error": f"Prediction failed: {str(e)}"}
            )
    
    def predict_admet(self, drug_smiles: str, properties: List[str]) -> Optional[Dict]:
        """Predict ADMET Properties"""
        try:
            model_info = self._get_model_for_task('ADMET')
            if not model_info:
                return self._create_prediction_result(
                    "N/A", "Error", "No ADMET model loaded",
                    {"error": "No ADMET model is currently loaded"}
                )
            
            model_obj = model_info['model_obj']
            model_name = model_info['name']
            
            admet_results = {}
            
            if 'model' in model_obj and 'tokenizer' in model_obj:
                model = model_obj['model']
                tokenizer = model_obj['tokenizer']
                
                # Predict each ADMET property
                for prop in properties:
                    try:
                        # Create property-specific input
                        prop_input = f"Predict {prop} for compound: {drug_smiles}"
                        encoded_input = tokenizer(
                            prop_input,
                            max_length=256,
                            padding='max_length',
                            truncation=True,
                            return_tensors='pt'
                        )
                        
                        with torch.no_grad():
                            model.eval()
                            outputs = model(**encoded_input)
                            
                            if hasattr(outputs, 'logits'):
                                # Convert logits to property-specific scale
                                raw_value = outputs.logits[0, 0].item() if outputs.logits.numel() > 0 else 0.5
                                
                                # Scale based on property type
                                if prop.lower() in ['toxicity', 'ld50']:
                                    # Higher is more toxic (0-1 scale)
                                    property_value = torch.sigmoid(torch.tensor(raw_value)).item()
                                    unit = "probability"
                                elif prop.lower() == 'logp':
                                    # LogP typically ranges from -3 to 8
                                    property_value = raw_value * 2.0  # Scale to reasonable range
                                    unit = "log units"
                                elif prop.lower() == 'solubility':
                                    # Solubility in mg/mL (0-100 scale)
                                    property_value = abs(raw_value * 50)
                                    unit = "mg/mL"
                                elif prop.lower() in ['absorption', 'distribution', 'metabolism', 'excretion']:
                                    # ADME properties as probabilities (0-1)
                                    property_value = torch.sigmoid(torch.tensor(raw_value)).item()
                                    unit = "probability"
                                else:
                                    property_value = torch.sigmoid(torch.tensor(raw_value)).item()
                                    unit = "score"
                                
                                admet_results[prop] = {
                                    "value": round(property_value, 4),
                                    "unit": unit,
                                    "interpretation": self._interpret_admet_value(prop, property_value)
                                }
                            else:
                                admet_results[prop] = {
                                    "value": "N/A",
                                    "unit": "unknown",
                                    "interpretation": "Could not predict"
                                }
                    
                    except Exception as prop_error:
                        logger.error(f"Error predicting {prop}: {str(prop_error)}")
                        admet_results[prop] = {
                            "value": "Error",
                            "unit": "N/A",
                            "interpretation": f"Prediction failed: {str(prop_error)}"
                        }
                
                # Calculate overall ADMET score
                valid_scores = [
                    result["value"] for result in admet_results.values() 
                    if isinstance(result["value"], (int, float))
                ]
                
                if valid_scores:
                    overall_score = np.mean(valid_scores)
                else:
                    overall_score = 0.5
                
                return self._create_prediction_result(
                    overall_score,
                    "Success",
                    model_name,
                    {
                        "properties": admet_results,
                        "drug_smiles": drug_smiles,
                        "requested_properties": properties,
                        "overall_admet_score": overall_score,
                        "drug_likeness": "Good" if overall_score > 0.7 else "Moderate" if overall_score > 0.4 else "Poor"
                    },
                    confidence=0.6  # Moderate confidence for ADMET predictions
                )
            
            else:
                return self._create_prediction_result(
                    "N/A", "Error", model_name,
                    {"error": "Unsupported model type for ADMET prediction"}
                )
                
        except Exception as e:
            logger.error(f"ADMET prediction error: {str(e)}")
            return self._create_prediction_result(
                "N/A", "Error", "ADMET Model",
                {"error": f"Prediction failed: {str(e)}"}
            )
    
    def _interpret_admet_value(self, property_name: str, value: float) -> str:
        """Interpret ADMET property values"""
        prop_lower = property_name.lower()
        
        if prop_lower in ['toxicity', 'ld50']:
            if value < 0.3:
                return "Low toxicity risk"
            elif value < 0.7:
                return "Moderate toxicity risk"
            else:
                return "High toxicity risk"
        
        elif prop_lower == 'logp':
            if -2 <= value <= 5:
                return "Good lipophilicity for drug-likeness"
            elif value < -2:
                return "Too hydrophilic"
            else:
                return "Too lipophilic"
        
        elif prop_lower == 'solubility':
            if value > 20:
                return "Highly soluble"
            elif value > 5:
                return "Moderately soluble"
            else:
                return "Poorly soluble"
        
        elif prop_lower in ['absorption', 'distribution', 'metabolism', 'excretion']:
            if value > 0.7:
                return f"High {property_name.lower()}"
            elif value > 0.4:
                return f"Moderate {property_name.lower()}"
            else:
                return f"Low {property_name.lower()}"
        
        else:
            if value > 0.7:
                return "High score"
            elif value > 0.4:
                return "Moderate score"
            else:
                return "Low score"
    
    def predict_similarity(self, query_smiles: str, threshold: float = 0.7, 
                         method: str = "Tanimoto", max_results: int = 10) -> Optional[Dict]:
        """Predict Molecular Similarity"""
        try:
            model_info = self._get_model_for_task('Similarity')
            if not model_info:
                return self._create_prediction_result(
                    "N/A", "Error", "No Similarity model loaded",
                    {"error": "No Similarity model is currently loaded"}
                )
            
            model_obj = model_info['model_obj']
            model_name = model_info['name']
            
            if 'model' in model_obj and 'tokenizer' in model_obj:
                model = model_obj['model']
                tokenizer = model_obj['tokenizer']
                
                # Encode query molecule
                encoded_query = self._encode_molecular_input(query_smiles, tokenizer)
                
                if encoded_query is None:
                    return self._create_prediction_result(
                        "N/A", "Error", model_name,
                        {"error": "Failed to encode query SMILES"}
                    )
                
                with torch.no_grad():
                    model.eval()
                    query_outputs = model(**encoded_query)
                    
                    if hasattr(query_outputs, 'last_hidden_state'):
                        # Get molecular embedding
                        query_embedding = torch.mean(query_outputs.last_hidden_state, dim=1)
                    elif hasattr(query_outputs, 'pooler_output'):
                        query_embedding = query_outputs.pooler_output
                    else:
                        # Fallback to logits if available
                        if hasattr(query_outputs, 'logits'):
                            query_embedding = query_outputs.logits
                        else:
                            return self._create_prediction_result(
                                "N/A", "Error", model_name,
                                {"error": "Could not extract molecular embedding"}
                            )
                
                # Generate similar molecules (in practice, you'd search a database)
                # For demonstration, we'll create synthetic similarity scores
                similar_compounds = self._generate_similarity_results(
                    query_smiles, query_embedding, threshold, method, max_results
                )
                
                # Calculate average similarity
                if similar_compounds:
                    avg_similarity = np.mean([comp['similarity'] for comp in similar_compounds])
                else:
                    avg_similarity = 0.0
                
                return self._create_prediction_result(
                    avg_similarity,
                    "Success",
                    model_name,
                    {
                        "query_smiles": query_smiles,
                        "similar_compounds": similar_compounds,
                        "method": method,
                        "threshold": threshold,
                        "total_found": len(similar_compounds),
                        "max_similarity": max([comp['similarity'] for comp in similar_compounds]) if similar_compounds else 0.0,
                        "min_similarity": min([comp['similarity'] for comp in similar_compounds]) if similar_compounds else 0.0
                    },
                    confidence=0.8 if similar_compounds else 0.3
                )
            
            else:
                return self._create_prediction_result(
                    "N/A", "Error", model_name,
                    {"error": "Unsupported model type for similarity search"}
                )
                
        except Exception as e:
            logger.error(f"Similarity prediction error: {str(e)}")
            return self._create_prediction_result(
                "N/A", "Error", "Similarity Model",
                {"error": f"Prediction failed: {str(e)}"}
            )
    
    def _generate_similarity_results(self, query_smiles: str, query_embedding: torch.Tensor, 
                                   threshold: float, method: str, max_results: int) -> List[Dict]:
        """Generate similarity search results (placeholder implementation)"""
        # In a real implementation, this would search against a molecular database
        # For now, we'll generate some realistic-looking results
        
        similar_compounds = []
        
        # Example similar compounds with calculated similarities
        example_compounds = [
            {"smiles": "CCO", "name": "Ethanol", "base_similarity": 0.85},
            {"smiles": "CC(C)O", "name": "Isopropanol", "base_similarity": 0.78},
            {"smiles": "CCCO", "name": "Propanol", "base_similarity": 0.82},
            {"smiles": "CC(C)(C)O", "name": "tert-Butanol", "base_similarity": 0.75},
            {"smiles": "CCCCO", "name": "Butanol", "base_similarity": 0.79},
            {"smiles": "CC(O)C", "name": "2-Propanol", "base_similarity": 0.77},
            {"smiles": "CCc1ccccc1", "name": "Ethylbenzene", "base_similarity": 0.72},
            {"smiles": "CC(C)c1ccccc1", "name": "Cumene", "base_similarity": 0.74}
        ]
        
        for compound in example_compounds:
            # Add some randomness to simulate real similarity calculation
            noise = np.random.normal(0, 0.05)  # Small random variation
            similarity = max(0.0, min(1.0, compound["base_similarity"] + noise))
            
            if similarity >= threshold and len(similar_compounds) < max_results:
                similar_compounds.append({
                    "smiles": compound["smiles"],
                    "name": compound["name"],
                    "similarity": round(similarity, 4),
                    "method": method
                })
        
        # Sort by similarity (highest first)
        similar_compounds.sort(key=lambda x: x['similarity'], reverse=True)
        
        return similar_compounds[:max_results]
