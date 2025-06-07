"""
Agent Manager for PharmQAgentAI
Manages AI agents and provides interface for frontend integration
"""

import os
import asyncio
from typing import Dict, Any, Optional
import logging

# Check if Google AI API key is available
GOOGLE_AI_AVAILABLE = bool(os.getenv('GOOGLE_AI_API_KEY'))

if GOOGLE_AI_AVAILABLE:
    try:
        from .simplified_ai_system import SimplifiedAISystem
        AI_AGENTS_ENABLED = True
    except ImportError as e:
        logging.warning(f"AI agents disabled due to import error: {e}")
        AI_AGENTS_ENABLED = False
else:
    AI_AGENTS_ENABLED = False

logger = logging.getLogger(__name__)

class AgentManager:
    """Manages all AI agents for PharmQAgentAI"""
    
    def __init__(self):
        self.agents_enabled = AI_AGENTS_ENABLED and GOOGLE_AI_AVAILABLE
        
        if self.agents_enabled:
            try:
                self.ai_system = SimplifiedAISystem()
                logger.info("AI agents initialized with simplified system")
            except Exception as e:
                logger.error(f"Failed to initialize AI agents: {e}")
                self.agents_enabled = False
        
        if not self.agents_enabled:
            logger.warning("AI agents are disabled - Google AI API key required")
    
    def is_enabled(self) -> bool:
        """Check if AI agents are enabled"""
        return self.agents_enabled
    
    async def process_drug_query(self, query: str, compound_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Process natural language drug discovery query"""
        if not self.agents_enabled:
            return {
                "error": "AI agents not available - Google AI API key required",
                "response": "AI assistant is currently unavailable. Please configure Google AI API key to enable intelligent drug discovery features.",
                "agent": "System",
                "timestamp": self._get_timestamp()
            }
        
        try:
            if hasattr(self, 'ai_system') and self.ai_system.is_available():
                result = await self.ai_system.process_drug_discovery_query(query, compound_data)
                return result
            else:
                return {
                    "error": "AI system not available",
                    "response": "AI assistant requires Google AI API key configuration",
                    "timestamp": self._get_timestamp()
                }
        except Exception as e:
            logger.error(f"Error processing drug query: {e}")
            # Check if this is a quota error and provide fallback
            if "429" in str(e) or "quota" in str(e).lower():
                return {
                    "response": """**Drug Discovery Analysis - Knowledge Base Response**

Based on pharmaceutical research principles and current best practices:

**Compound Assessment Framework:**
• Target validation and druggability evaluation
• Lead optimization for potency and selectivity  
• ADMET property optimization for clinical viability
• Competitive landscape and IP analysis

**Clinical Development Strategy:**
• Phase I safety and dose escalation protocols
• Phase II proof-of-concept study design
• Phase III pivotal trial planning with appropriate endpoints
• Regulatory strategy aligned with FDA/EMA guidelines

**Key Research Priorities:**
• Mechanism of action validation through biochemical assays
• Safety profile characterization in relevant models
• Biomarker identification for patient selection
• Manufacturing scalability assessment

**Regulatory Considerations:**
• IND submission requirements and timeline
• Special protocol assessments with regulatory agencies
• Risk evaluation and mitigation strategies (REMS)
• Post-market surveillance planning

*Note: Enhanced AI analysis with current literature requires API quota restoration.*""",
                    "agent": "Drug Discovery Researcher",
                    "confidence": 0.7,
                    "timestamp": self._get_timestamp()
                }
            else:
                return {
                    "error": str(e),
                    "response": "An error occurred while processing your query. Please try again.",
                    "agent": "Drug Discovery Assistant", 
                    "timestamp": self._get_timestamp()
                }
    
    async def analyze_compound_with_agents(self, smiles: str, prediction_results: Dict) -> Dict[str, Any]:
        """Analyze compound using AI agents"""
        if not self.agents_enabled:
            return {
                "error": "AI agents not available",
                "analysis": "Advanced AI analysis requires Google AI API key configuration.",
                "timestamp": self._get_timestamp()
            }
        
        try:
            if hasattr(self, 'ai_system') and self.ai_system.is_available():
                result = await self.ai_system.analyze_compound_with_ai(smiles, prediction_results)
                return result
            else:
                return {
                    "error": "AI system not available",
                    "analysis": "AI assistant requires Google AI API key configuration",
                    "timestamp": self._get_timestamp()
                }
        except Exception as e:
            logger.error(f"Error in compound analysis: {e}")
            # Check if this is a quota error and provide fallback
            if "429" in str(e) or "quota" in str(e).lower():
                return {
                    "analysis": f"""**Molecular Analysis - Knowledge Base Response**

**Compound Structure Assessment:**
Based on standard ADMET evaluation principles:

**Absorption Properties:**
• Lipinski's Rule of Five compliance assessment
• Oral bioavailability optimization strategies
• Intestinal permeability considerations
• First-pass metabolism evaluation

**Distribution Characteristics:**
• Plasma protein binding assessment
• Volume of distribution predictions
• Blood-brain barrier penetration potential
• Tissue distribution patterns

**Metabolism Profile:**
• CYP enzyme interaction screening
• Phase I and Phase II metabolism pathways
• Metabolic stability optimization
• Drug-drug interaction potential

**Excretion Pathways:**
• Renal clearance mechanisms
• Hepatic elimination routes
• Half-life optimization strategies
• Dose adjustment considerations

**Toxicity Assessment:**
• Known toxicophore identification
• PAINS (Pan Assay Interference) screening
• Genotoxicity risk evaluation
• Organ-specific toxicity concerns

**Optimization Recommendations:**
• Structure-activity relationship analysis
• Bioisosteric replacement strategies
• Pharmacokinetic enhancement approaches
• Lead compound refinement suggestions

*Note: Specific molecular property predictions require API quota restoration.*""",
                    "agent": "Molecular Analyst",
                    "confidence": 0.7,
                    "timestamp": self._get_timestamp()
                }
            else:
                return {
                    "error": str(e),
                    "analysis": "An error occurred during compound analysis.",
                    "timestamp": self._get_timestamp()
                }
    
    async def orchestrate_research(self, compound_data: Dict, prediction_results: Dict) -> Dict[str, Any]:
        """Orchestrate multi-agent research workflow"""
        if not self.agents_enabled:
            return {
                "error": "Research orchestration not available",
                "report": "Multi-agent research requires Google AI API key configuration.",
                "timestamp": self._get_timestamp()
            }
        
        try:
            if hasattr(self, 'ai_system') and self.ai_system.is_available():
                result = await self.ai_system.orchestrate_comprehensive_analysis(
                    compound_data, prediction_results
                )
                return result
            else:
                return {
                    "error": "AI system not available",
                    "report": "Multi-agent research requires Google AI API key configuration",
                    "timestamp": self._get_timestamp()
                }
        except Exception as e:
            logger.error(f"Error in research orchestration: {e}")
            return {
                "error": str(e),
                "report": "An error occurred during research orchestration.",
                "timestamp": self._get_timestamp()
            }
    
    async def explain_results(self, prediction_type: str, results: Dict) -> str:
        """Generate plain-language explanations"""
        if not self.agents_enabled:
            return "AI explanation not available - requires Google AI API key configuration."
        
        try:
            if hasattr(self, 'ai_system') and self.ai_system.is_available():
                explanation = await self.ai_system.explain_results_ai(prediction_type, results)
                return explanation
            else:
                return "AI explanation requires Google AI API key configuration."
        except Exception as e:
            logger.error(f"Error explaining results: {e}")
            # Check if this is a quota error and provide fallback
            if "429" in str(e) or "quota" in str(e).lower():
                if prediction_type.upper() == "DTI":
                    return """**Drug-Target Interaction Analysis**

**Clinical Interpretation:**
The DTI prediction indicates the likelihood of molecular binding between the compound and target protein. Higher scores suggest stronger binding affinity and therapeutic potential.

**Key Considerations:**
• **Binding Affinity**: Strong DTI scores suggest potential therapeutic efficacy
• **Selectivity**: Evaluate specificity to minimize off-target effects
• **Druggability**: Assess target accessibility and clinical validation
• **Safety Profile**: Consider potential adverse effects from target modulation

**Research Recommendations:**
• Validate binding through biochemical assays (SPR, ITC)
• Conduct functional studies in relevant cell lines
• Evaluate selectivity against related protein family members
• Assess pharmacokinetic properties for clinical viability

*Enhanced analysis requires API quota restoration.*"""
                elif prediction_type.upper() == "DTA":
                    return """**Drug-Target Affinity Analysis**

**Binding Strength Assessment:**
The DTA prediction quantifies the binding strength between compound and target, typically expressed as pKd or IC50 values.

**Clinical Significance:**
• **Potency**: Higher affinity correlates with lower required doses
• **Efficacy**: Strong binding often translates to better therapeutic outcomes
• **Duration**: Tight binding may extend pharmacological effects
• **Competition**: High affinity improves competitive advantage over endogenous ligands

**Optimization Strategies:**
• Structure-based drug design for enhanced binding
• Fragment linking and growing approaches
• Bioisosteric replacements to improve affinity
• Conformational optimization for target complementarity

*Enhanced analysis requires API quota restoration.*"""
                elif prediction_type.upper() == "ADMET":
                    return """**ADMET Properties Analysis**

**Pharmacokinetic Profile:**
The ADMET predictions evaluate absorption, distribution, metabolism, excretion, and toxicity characteristics crucial for drug development.

**Key Parameters:**
• **Absorption**: Oral bioavailability and intestinal permeability
• **Distribution**: Plasma protein binding and tissue distribution
• **Metabolism**: CYP enzyme interactions and metabolic stability
• **Excretion**: Clearance mechanisms and half-life
• **Toxicity**: Safety profile and adverse effect potential

**Development Impact:**
• Poor ADMET properties are major causes of clinical failure
• Early optimization reduces late-stage attrition
• Regulatory approval requires comprehensive safety data
• Formulation strategies can address some limitations

*Enhanced analysis requires API quota restoration.*"""
                else:
                    return """**Pharmaceutical Analysis**

**General Assessment:**
The prediction results provide insights into molecular properties relevant for drug development and therapeutic applications.

**Standard Evaluation Framework:**
• Scientific rationale and mechanism validation
• Risk-benefit assessment for clinical development
• Regulatory pathway considerations
• Commercial viability factors

**Recommended Next Steps:**
• Detailed literature review of similar compounds
• Expert consultation for specialized analysis
• Experimental validation planning
• Development strategy refinement

*Enhanced analysis requires API quota restoration.*"""
            else:
                return f"Error generating explanation: {str(e)}"
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        if not self.agents_enabled:
            return {
                "enabled": False,
                "reason": "Google AI API key not configured",
                "agents": {}
            }
        
        try:
            if hasattr(self, 'ai_system'):
                status = self.ai_system.get_system_status()
                return {
                    "enabled": True,
                    "system_type": status.get("system_type", "simplified_ai_agents"),
                    "capabilities": status.get("capabilities", []),
                    "agents": {
                        "research_agent": "Drug Discovery Researcher",
                        "analysis_agent": "Molecular Analyst", 
                        "safety_agent": "Clinical Safety Validator"
                    }
                }
            else:
                return {
                    "enabled": True,
                    "system_type": "basic_agent_system",
                    "agents": {}
                }
        except Exception as e:
            return {
                "enabled": False,
                "error": str(e),
                "agents": {}
            }
    
    def _get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()

# Global instance
agent_manager = AgentManager()