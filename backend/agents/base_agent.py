"""
Base Agent for PharmQAgentAI
Provides foundation for all AI agents using Google Gemini
"""

import os
import google.generativeai as genai
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Base class for all PharmQAgentAI agents"""
    
    def __init__(self, name: str, model_name: str = "gemini-1.5-flash"):
        self.name = name
        self.model_name = model_name
        self._configure_genai()
        self.model = genai.GenerativeModel(model_name)
        self.conversation_history = []
        
    def _configure_genai(self):
        """Configure Google Generative AI"""
        api_key = os.getenv('GOOGLE_AI_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_AI_API_KEY environment variable not set")
        genai.configure(api_key=api_key)
        
    def add_to_history(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": self._get_timestamp()
        })
        
    def _get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
        
    async def generate_response(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Generate response using Gemini"""
        try:
            # Build full prompt with context
            full_prompt = self._build_prompt(prompt, context)
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            
            # Add to history
            self.add_to_history("user", prompt)
            self.add_to_history("assistant", response.text)
            
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return f"Error processing request: {str(e)}"
            
    def _build_prompt(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Build enhanced prompt with context and agent personality"""
        base_prompt = f"""You are {self.name}, an AI agent specialized in pharmaceutical research and drug discovery.

Agent Context: {self.get_agent_context()}

Current Task: {prompt}
"""
        
        if context:
            base_prompt += f"\nAdditional Context: {context}\n"
            
        if self.conversation_history:
            base_prompt += "\nRecent Conversation History:\n"
            for msg in self.conversation_history[-3:]:  # Last 3 messages
                base_prompt += f"{msg['role']}: {msg['content']}\n"
                
        return base_prompt
        
    @abstractmethod
    def get_agent_context(self) -> str:
        """Return agent-specific context and expertise"""
        pass
        
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        
    def get_capabilities(self) -> List[str]:
        """Return list of agent capabilities"""
        return [
            "Natural language processing",
            "Scientific literature analysis", 
            "Drug discovery insights",
            "Context-aware responses"
        ]