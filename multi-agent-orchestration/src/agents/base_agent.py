"""
Base Agent class and common functionality for all agents.
"""

import asyncio
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


class BaseAgent(ABC):
    """Base class for all agents in the multi-agent system."""
    
    def __init__(
        self,
        name: str,
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ):
        self.name = name
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )
        self.conversation_history: List[Dict[str, Any]] = []
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the system prompt for this agent."""
        pass
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data and return results."""
        pass
    
    def add_to_history(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        """Add message to conversation history."""
        entry = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "agent": self.name
        }
        if metadata:
            entry["metadata"] = metadata
        self.conversation_history.append(entry)
    
    async def invoke_llm(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None
    ) -> str:
        """Invoke the LLM with messages."""
        chat_messages = []
        
        # Add system prompt
        if system_prompt or self.get_system_prompt():
            chat_messages.append(SystemMessage(content=system_prompt or self.get_system_prompt()))
        
        # Add conversation messages
        for msg in messages:
            if msg["role"] == "user":
                chat_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                chat_messages.append(AIMessage(content=msg["content"]))
        
        # Invoke LLM
        response = await self.llm.ainvoke(chat_messages)
        
        # Log conversation
        self.add_to_history("user", messages[-1]["content"] if messages else "")
        self.add_to_history("assistant", response.content)
        
        return response.content
    
    def get_capabilities(self) -> List[str]:
        """Return list of agent capabilities."""
        return [
            "natural_language_processing",
            "conversation_history_tracking",
            "llm_interaction"
        ]
    
    def get_status(self) -> Dict[str, Any]:
        """Return agent status information."""
        return {
            "name": self.name,
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "conversation_length": len(self.conversation_history),
            "capabilities": self.get_capabilities(),
            "last_activity": self.conversation_history[-1]["timestamp"] if self.conversation_history else None
        }
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []