"""
Base Agent Class for CloudSpend AI Multi-Agent System
"""
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    async def execute(self, task: dict):
        pass
