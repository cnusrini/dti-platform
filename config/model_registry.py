"""
Model Registry for PharmQAgentAI
Central registry of available models and their configurations
"""

MODEL_REGISTRY = {
    "DTI": {
        "DeepDTI": {
            "type": "transformer",
            "description": "Deep learning model for drug-target interaction prediction",
            "input_format": ["drug_smiles", "target_sequence"],
            "output_format": "interaction_score",
            "status": "available"
        },
        "GraphDTI": {
            "type": "graph",
            "description": "Graph neural network for DTI prediction",
            "input_format": ["drug_smiles", "target_sequence"],
            "output_format": "interaction_score",
            "status": "available"
        }
    },
    "DTA": {
        "DeepDTA": {
            "type": "transformer",
            "description": "Deep learning model for drug-target affinity prediction",
            "input_format": ["drug_smiles", "target_sequence"],
            "output_format": "affinity_value",
            "status": "available"
        },
        "AttentionDTA": {
            "type": "attention",
            "description": "Attention-based model for DTA prediction",
            "input_format": ["drug_smiles", "target_sequence"],
            "output_format": "affinity_value",
            "status": "available"
        }
    },
    "DDI": {
        "DrugBAN": {
            "type": "transformer",
            "description": "BiAttention network for drug-drug interaction prediction",
            "input_format": ["drug1_smiles", "drug2_smiles"],
            "output_format": "interaction_risk",
            "status": "available"
        },
        "MHCADDI": {
            "type": "multihead",
            "description": "Multi-head cross attention for DDI prediction",
            "input_format": ["drug1_smiles", "drug2_smiles"],
            "output_format": "interaction_risk",
            "status": "available"
        }
    },
    "ADMET": {
        "ADMETlab": {
            "type": "ensemble",
            "description": "Ensemble model for ADMET property prediction",
            "input_format": ["drug_smiles"],
            "output_format": "admet_properties",
            "status": "available"
        },
        "ChemProp": {
            "type": "graph",
            "description": "Graph convolutional network for molecular property prediction",
            "input_format": ["drug_smiles"],
            "output_format": "admet_properties",
            "status": "available"
        }
    },
    "Similarity": {
        "MolBERT": {
            "type": "transformer",
            "description": "Molecular BERT for similarity search",
            "input_format": ["query_smiles"],
            "output_format": "similar_molecules",
            "status": "available"
        },
        "ChemBERTa": {
            "type": "transformer",
            "description": "Chemical BERT for molecular similarity",
            "input_format": ["query_smiles"],
            "output_format": "similar_molecules",
            "status": "available"
        }
    }
}