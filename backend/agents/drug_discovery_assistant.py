"""
Intelligent Drug Discovery Assistant Agent
Handles natural language queries and conversational analysis for drug discovery
"""

from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)

class DrugDiscoveryAssistant(BaseAgent):
    """AI assistant for drug discovery research and analysis"""
    
    def __init__(self):
        super().__init__(
            name="Drug Discovery Assistant",
            model_name="gemini-1.5-flash"
        )
        self.expertise_areas = [
            "Drug-target interactions",
            "ADMET properties",
            "Molecular similarity",
            "Pharmacokinetics",
            "Safety assessment",
            "Therapeutic applications"
        ]
        
    def get_agent_context(self) -> str:
        """Return agent-specific context"""
        return """I am an expert AI assistant specializing in pharmaceutical research and drug discovery. 
        I help researchers analyze molecular compounds, predict drug properties, interpret experimental results, 
        and provide insights into therapeutic applications. I combine scientific knowledge with AI prediction 
        results to offer comprehensive drug discovery guidance."""
        
    async def process_drug_query(self, query: str, compound_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Process natural language drug discovery queries"""
        context = {
            "query_type": "drug_discovery",
            "compound_data": compound_data,
            "expertise_areas": self.expertise_areas
        }
        
        enhanced_prompt = f"""
        As a drug discovery expert, analyze this research query and provide comprehensive insights:
        
        Query: {query}
        
        Please provide:
        1. Direct answer to the query
        2. Scientific rationale and mechanisms
        3. Relevant considerations for drug development
        4. Potential risks or limitations
        5. Recommended next steps for research
        
        Focus on actionable insights that advance drug discovery research.
        """
        
        response = await self.generate_response(enhanced_prompt, context)
        
        return {
            "response": response,
            "query": query,
            "agent": self.name,
            "expertise_applied": self.expertise_areas,
            "timestamp": self._get_timestamp()
        }
        
    async def analyze_compound_properties(self, smiles: str, prediction_results: Dict) -> Dict[str, Any]:
        """Analyze compound properties and provide clinical insights"""
        context = {
            "analysis_type": "compound_analysis",
            "smiles": smiles,
            "prediction_results": prediction_results
        }
        
        enhanced_prompt = f"""
        Analyze this molecular compound and its predicted properties:
        
        SMILES: {smiles}
        Prediction Results: {prediction_results}
        
        Provide comprehensive analysis including:
        1. Molecular characteristics and drug-like properties
        2. Clinical interpretation of ADMET results
        3. Safety profile assessment
        4. Therapeutic potential and applications
        5. Development challenges and opportunities
        6. Comparison with known drugs in similar classes
        
        Present findings in clear, actionable language for pharmaceutical researchers.
        """
        
        response = await self.generate_response(enhanced_prompt, context)
        
        return {
            "analysis": response,
            "compound": smiles,
            "predictions_analyzed": list(prediction_results.keys()) if prediction_results else [],
            "agent": self.name,
            "timestamp": self._get_timestamp()
        }
        
    async def suggest_research_directions(self, current_findings: Dict) -> Dict[str, Any]:
        """Suggest new research directions based on current findings"""
        context = {
            "task_type": "research_planning",
            "current_findings": current_findings
        }
        
        enhanced_prompt = f"""
        Based on these research findings, suggest promising research directions:
        
        Current Findings: {current_findings}
        
        Provide strategic recommendations:
        1. Most promising research avenues to pursue
        2. Key experiments and studies to conduct
        3. Potential collaborations or partnerships
        4. Technology platforms that could accelerate progress
        5. Timeline and milestone suggestions
        6. Resource requirements and priorities
        
        Focus on high-impact opportunities that could advance drug development.
        """
        
        response = await self.generate_response(enhanced_prompt, context)
        
        return {
            "research_directions": response,
            "based_on_findings": current_findings,
            "agent": self.name,
            "timestamp": self._get_timestamp()
        }
        
    async def explain_prediction_results(self, prediction_type: str, results: Dict) -> str:
        """Generate plain-language explanations of prediction results"""
        context = {
            "explanation_type": "prediction_interpretation",
            "prediction_type": prediction_type,
            "results": results
        }
        
        enhanced_prompt = f"""
        Explain these {prediction_type} prediction results in clear, accessible language:
        
        Results: {results}
        
        Provide explanation covering:
        1. What these results mean in practical terms
        2. Clinical significance and implications
        3. How these values compare to typical drug standards
        4. What researchers should focus on next
        5. Any limitations or caveats to consider
        
        Use plain language that non-experts can understand while maintaining scientific accuracy.
        """
        
        response = await self.generate_response(enhanced_prompt, context)
        return response
        
    def get_capabilities(self) -> List[str]:
        """Return assistant capabilities"""
        return [
            "Natural language drug discovery queries",
            "Compound property analysis and interpretation", 
            "Clinical context generation for ADMET results",
            "Research direction recommendations",
            "Plain-language explanation of complex results",
            "Therapeutic application suggestions",
            "Safety and efficacy assessment",
            "Literature context and scientific rationale"
        ]