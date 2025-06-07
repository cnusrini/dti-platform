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
        import google.generativeai as genai
        from .drug_discovery_assistant import DrugDiscoveryAssistant
        from .research_orchestrator import ResearchOrchestrator
        from .google_agent_builder import GoogleAgentBuilder
        from .enhanced_adk_system import EnhancedADKSystem
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
                self.drug_discovery_assistant = DrugDiscoveryAssistant()
                self.research_orchestrator = ResearchOrchestrator()
                self.google_agent_builder = GoogleAgentBuilder()
                self.enhanced_adk_system = EnhancedADKSystem()
                logger.info("AI agents initialized successfully with Enhanced Google AI integration")
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
            result = await self.drug_discovery_assistant.process_drug_query(query, compound_data)
            return result
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
            # Get compound analysis from assistant
            analysis_result = await self.drug_discovery_assistant.analyze_compound_properties(
                smiles, prediction_results
            )
            
            return analysis_result
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
            # Use Enhanced ADK system for advanced orchestration
            if hasattr(self, 'enhanced_adk_system') and self.enhanced_adk_system.is_available():
                result = await self.enhanced_adk_system.orchestrate_multi_agent_analysis(
                    compound_data, prediction_results
                )
                return result
            elif hasattr(self, 'google_agent_builder'):
                result = await self.google_agent_builder.orchestrate_multi_agent_research(
                    compound_data, prediction_results
                )
                return result
            else:
                # Fallback to standard orchestrator
                result = await self.research_orchestrator.orchestrate_research(
                    compound_data, prediction_results
                )
                return result
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
            explanation = await self.drug_discovery_assistant.explain_prediction_results(
                prediction_type, results
            )
            return explanation
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
            return {
                "enabled": True,
                "agents": {
                    "drug_discovery_assistant": {
                        "name": self.drug_discovery_assistant.name,
                        "capabilities": self.drug_discovery_assistant.get_capabilities()
                    },
                    "research_orchestrator": {
                        "available_agents": list(self.research_orchestrator.agents.keys())
                    }
                }
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