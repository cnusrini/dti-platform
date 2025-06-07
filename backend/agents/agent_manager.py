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