"""
Google Gemini LLM Client Implementation
"""
import os
import google.generativeai as genai
from services.llm_client import LLMClient


class GeminiClient(LLMClient):
    """Google Gemini implementation of LLMClient"""
    
    def __init__(self, model: str = "gemini-2.5-flash"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
    
    def invoke(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        
        response = self.model.generate_content(
            full_prompt,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_tokens
            }
        )
        return response.text
