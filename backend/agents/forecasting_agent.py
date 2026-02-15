"""
Forecasting Agent - Predicts future cloud spending
"""
from .base_agent import BaseAgent

class ForecastingAgent(BaseAgent):
    def __init__(self):
        super().__init__("ForecastingAgent")
    
    async def execute(self, task: dict):
        # Generate spending forecasts
        pass
