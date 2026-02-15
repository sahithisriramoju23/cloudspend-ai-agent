"""
LLM Client Interface for CloudSpend AI
"""
from abc import ABC, abstractmethod
from typing import Optional


class LLMClient(ABC):
    """Abstract base class for LLM client implementations"""
    
    @abstractmethod
    def invoke(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """
        Invoke the LLM with given prompts and parameters
        
        Args:
            system_prompt: System instruction for the LLM
            user_prompt: User query or input
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in response
            
        Returns:
            str: LLM response text
        """
        pass
