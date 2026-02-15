"""
Data Models for CloudSpend AI
"""
from pydantic import BaseModel
from datetime import datetime

class CostRecord(BaseModel):
    id: str
    provider: str
    service: str
    cost: float
    timestamp: datetime
