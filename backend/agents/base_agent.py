"""
Base Agent Class for CloudSpend AI Multi-Agent System
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from utils.logger import setup_logger


@dataclass
class Recommendation:
    """Standardized recommendation structure"""
    resourceType: str
    resourceId: str
    currentCost: float
    issue: str
    recommendation: str
    estimatedSavings: float
    priority: str  # high, medium, low
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class AgentOutput:
    """Standardized agent output structure"""
    agentName: str
    recommendations: List[Dict]
    totalPotentialSavings: float
    summary: str
    metadata: Dict[str, Any] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)


class BaseAgent(ABC):
    """Abstract base class for all CloudSpend AI agents"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = setup_logger(name)
    
    @abstractmethod
    def analyze(self, scan_data: Dict) -> Dict:
        """
        Analyze scan data and generate recommendations
        
        Args:
            scan_data: Cloud infrastructure scan data
            
        Returns:
            Dict: Structured recommendations
        """
        pass
    
    def run(self, scan_data: Dict) -> AgentOutput:
        """
        Standardized run method for all agents
        
        Args:
            scan_data: Cloud infrastructure scan data
            
        Returns:
            AgentOutput: Standardized output structure
        """
        self.logger.info(f"Starting {self.name} analysis")
        
        try:
            result = self.analyze(scan_data)
            
            output = AgentOutput(
                agentName=self.name,
                recommendations=result.get("recommendations", []),
                totalPotentialSavings=result.get("totalPotentialSavings", 0.0),
                summary=result.get("summary", ""),
                metadata=result.get("metadata", {})
            )
            
            self.logger.info(f"{self.name} completed successfully")
            return output
            
        except Exception as e:
            self.logger.error(f"{self.name} failed: {str(e)}")
            raise
