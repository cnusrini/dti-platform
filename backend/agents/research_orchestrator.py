"""
Multi-Agent Research Orchestration System
Coordinates multiple AI agents for comprehensive drug discovery research
"""

from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
import logging
import asyncio

logger = logging.getLogger(__name__)

class ResearchAgent(BaseAgent):
    """Agent for scientific literature research and data gathering"""
    
    def __init__(self):
        super().__init__(
            name="Research Agent",
            model_name="gemini-pro"
        )
        
    def get_agent_context(self) -> str:
        return """I am a research specialist focused on scientific literature analysis, 
        data gathering, and evidence synthesis for pharmaceutical research. I help identify 
        relevant studies, extract key findings, and synthesize research insights."""
        
    async def research_compound(self, compound_info: Dict) -> Dict[str, Any]:
        """Research scientific literature about a compound"""
        context = {
            "task": "literature_research",
            "compound": compound_info
        }
        
        prompt = f"""
        Conduct comprehensive research analysis for this compound:
        {compound_info}
        
        Provide detailed insights on:
        1. Known biological activities and mechanisms
        2. Previous clinical studies and outcomes  
        3. Safety profile and adverse effects
        4. Therapeutic applications and indications
        5. Patent landscape and intellectual property
        6. Competitive compounds and alternatives
        
        Synthesize findings into actionable research intelligence.
        """
        
        response = await self.generate_response(prompt, context)
        
        return {
            "research_findings": response,
            "compound_analyzed": compound_info,
            "agent": self.name,
            "timestamp": self._get_timestamp()
        }

class AnalysisAgent(BaseAgent):
    """Agent for molecular data processing and insight generation"""
    
    def __init__(self):
        super().__init__(
            name="Analysis Agent", 
            model_name="gemini-pro"
        )
        
    def get_agent_context(self) -> str:
        return """I specialize in molecular data analysis, prediction interpretation, 
        and scientific insight generation. I process complex pharmaceutical data and 
        extract meaningful patterns for drug discovery applications."""
        
    async def analyze_predictions(self, prediction_data: Dict) -> Dict[str, Any]:
        """Analyze prediction results and generate insights"""
        context = {
            "task": "prediction_analysis",
            "data": prediction_data
        }
        
        prompt = f"""
        Analyze these drug discovery prediction results:
        {prediction_data}
        
        Generate comprehensive analysis including:
        1. Key molecular insights and drug-like properties
        2. Strengths and limitations identified
        3. Risk assessment and safety considerations
        4. Optimization opportunities
        5. Clinical development implications
        6. Recommended validation studies
        
        Provide actionable insights for research teams.
        """
        
        response = await self.generate_response(prompt, context)
        
        return {
            "analysis_results": response,
            "predictions_processed": prediction_data,
            "agent": self.name,
            "timestamp": self._get_timestamp()
        }

class ValidationAgent(BaseAgent):
    """Agent for cross-referencing and validation against known databases"""
    
    def __init__(self):
        super().__init__(
            name="Validation Agent",
            model_name="gemini-pro"
        )
        
    def get_agent_context(self) -> str:
        return """I am responsible for validation and quality control in drug discovery. 
        I cross-reference predictions with known databases, validate molecular structures, 
        and ensure scientific accuracy of research findings."""
        
    async def validate_compound(self, compound_data: Dict) -> Dict[str, Any]:
        """Validate compound data against known standards"""
        context = {
            "task": "compound_validation",
            "compound": compound_data
        }
        
        prompt = f"""
        Validate this compound data against pharmaceutical standards:
        {compound_data}
        
        Perform validation checking:
        1. Molecular structure validity and drug-likeness
        2. ADMET profile consistency with known drugs
        3. Safety flags and contraindications
        4. Regulatory compliance considerations
        5. Quality control recommendations
        6. Data integrity assessment
        
        Provide validation report with confidence scores.
        """
        
        response = await self.generate_response(prompt, context)
        
        return {
            "validation_report": response,
            "compound_validated": compound_data,
            "agent": self.name,
            "timestamp": self._get_timestamp()
        }

class ReportingAgent(BaseAgent):
    """Agent for compiling comprehensive research reports"""
    
    def __init__(self):
        super().__init__(
            name="Reporting Agent",
            model_name="gemini-pro"
        )
        
    def get_agent_context(self) -> str:
        return """I specialize in scientific report generation and documentation. 
        I compile research findings from multiple agents into comprehensive, 
        publication-ready reports for pharmaceutical research teams."""
        
    async def compile_research_report(self, agent_findings: Dict) -> Dict[str, Any]:
        """Compile findings from multiple agents into comprehensive report"""
        context = {
            "task": "report_compilation",
            "findings": agent_findings
        }
        
        prompt = f"""
        Compile comprehensive research report from these agent findings:
        {agent_findings}
        
        Generate structured report with:
        1. Executive Summary
        2. Key Findings and Insights
        3. Research Methodology and Data Sources
        4. Risk Assessment and Safety Profile
        5. Recommendations and Next Steps
        6. Technical Appendix
        
        Format as professional pharmaceutical research document.
        """
        
        response = await self.generate_response(prompt, context)
        
        return {
            "research_report": response,
            "compiled_from": list(agent_findings.keys()),
            "agent": self.name,
            "timestamp": self._get_timestamp()
        }

class ResearchOrchestrator:
    """Orchestrates multiple agents for comprehensive drug discovery research"""
    
    def __init__(self):
        self.research_agent = ResearchAgent()
        self.analysis_agent = AnalysisAgent()
        self.validation_agent = ValidationAgent()
        self.reporting_agent = ReportingAgent()
        
        self.agents = {
            "research": self.research_agent,
            "analysis": self.analysis_agent,
            "validation": self.validation_agent,
            "reporting": self.reporting_agent
        }
        
    async def orchestrate_research(self, compound_data: Dict, prediction_results: Dict) -> Dict[str, Any]:
        """Orchestrate multi-agent research workflow"""
        logger.info("Starting multi-agent research orchestration")
        
        # Step 1: Parallel research and analysis
        research_task = self.research_agent.research_compound(compound_data)
        analysis_task = self.analysis_agent.analyze_predictions(prediction_results)
        
        research_results, analysis_results = await asyncio.gather(
            research_task, analysis_task, return_exceptions=True
        )
        
        # Step 2: Validation
        validation_data = {
            "compound": compound_data,
            "predictions": prediction_results,
            "research": research_results if not isinstance(research_results, Exception) else None,
            "analysis": analysis_results if not isinstance(analysis_results, Exception) else None
        }
        
        validation_results = await self.validation_agent.validate_compound(validation_data)
        
        # Step 3: Compile comprehensive report
        all_findings = {
            "research": research_results if not isinstance(research_results, Exception) else {"error": str(research_results)},
            "analysis": analysis_results if not isinstance(analysis_results, Exception) else {"error": str(analysis_results)},
            "validation": validation_results
        }
        
        final_report = await self.reporting_agent.compile_research_report(all_findings)
        
        return {
            "orchestration_complete": True,
            "individual_findings": all_findings,
            "comprehensive_report": final_report,
            "agents_involved": list(self.agents.keys()),
            "timestamp": self._get_current_timestamp()
        }
        
    async def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        status = {}
        for name, agent in self.agents.items():
            status[name] = {
                "name": agent.name,
                "capabilities": agent.get_capabilities(),
                "conversation_length": len(agent.conversation_history)
            }
        return status
        
    def _get_current_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
        
    def clear_all_histories(self):
        """Clear conversation history for all agents"""
        for agent in self.agents.values():
            agent.clear_history()