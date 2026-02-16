"""
Orchestrator Agent - Coordinates execution of all optimization agents
"""
import uuid
from typing import Dict
from datetime import datetime
from agents.base_agent import BaseAgent
from agents.storage_agent import StorageOptimizationAgent
from agents.compute_agent import ComputeOptimizationAgent
from agents.network_agent import NetworkOptimizationAgent
from agents.report_agent import ReportAgent
from utils.llm_client import LLMClient
from utils.schema_validator import validate_agent_output, validate_report


class OrchestratorAgent(BaseAgent):
    """Orchestrates execution of all optimization agents"""
    
    def __init__(self, llm_client: LLMClient):
        super().__init__("OrchestratorAgent")
        self.llm_client = llm_client
        
        # Initialize all agents
        self.storage_agent = StorageOptimizationAgent(llm_client)
        self.compute_agent = ComputeOptimizationAgent(llm_client)
        self.network_agent = NetworkOptimizationAgent(llm_client)
        self.report_agent = ReportAgent(llm_client)
    
    def analyze(self, scan_data: Dict) -> Dict:
        """
        Run all optimization agents and generate comprehensive report
        
        Args:
            scan_data: AWS scan data dictionary
            
        Returns:
            Dict: Orchestrated results with scanId, report, and agent outputs
        """
        scan_id = str(uuid.uuid4())
        self.logger.info(f"Starting orchestrated analysis - Scan ID: {scan_id}")
        
        agent_outputs = {}
        
        # Run storage optimization
        self.logger.info("Running Storage Optimization Agent")
        try:
            agent_outputs["storage"] = self.storage_agent.analyze(scan_data)
            validate_agent_output(agent_outputs["storage"], "StorageOptimizationAgent")
        except Exception as e:
            self.logger.error(f"Storage agent failed: {str(e)}")
            agent_outputs["storage"] = {"error": str(e), "recommendations": [], "totalPotentialSavings": 0.0, "summary": ""}
        
        # Run compute optimization
        self.logger.info("Running Compute Optimization Agent")
        try:
            agent_outputs["compute"] = self.compute_agent.analyze(scan_data)
            validate_agent_output(agent_outputs["compute"], "ComputeOptimizationAgent")
        except Exception as e:
            self.logger.error(f"Compute agent failed: {str(e)}")
            agent_outputs["compute"] = {"error": str(e), "recommendations": [], "totalPotentialSavings": 0.0, "summary": ""}
        
        # Run network optimization
        self.logger.info("Running Network Optimization Agent")
        try:
            agent_outputs["network"] = self.network_agent.analyze(scan_data)
            validate_agent_output(agent_outputs["network"], "NetworkOptimizationAgent")
        except Exception as e:
            self.logger.error(f"Network agent failed: {str(e)}")
            agent_outputs["network"] = {"error": str(e), "recommendations": [], "totalPotentialSavings": 0.0, "summary": ""}
        
        # Generate executive report
        self.logger.info("Generating Executive Report")
        try:
            report = self.report_agent.analyze(list(agent_outputs.values()))
            validate_report(report)
        except Exception as e:
            self.logger.error(f"Report agent failed: {str(e)}")
            report = {"error": str(e), "executiveSummary": "Report generation failed", "totalEstimatedSavings": 0.0, "top5Savings": []}
        
        result = {
            "scanId": scan_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "accountId": scan_data.get("accountId"),
            "region": scan_data.get("region"),
            "report": report,
            "agentOutputs": agent_outputs
        }
        
        self.logger.info(f"Orchestration complete - Scan ID: {scan_id}")
        return result
