"""
Network Optimization Agent - Analyzes network resources for cost optimization
"""
import json
from typing import Dict
from backend.agents.base_agent import BaseAgent
from backend.utils.llm_client import LLMClient


class NetworkOptimizationAgent(BaseAgent):
    """Agent for analyzing network resources and generating optimization recommendations"""
    
    def __init__(self, llm_client: LLMClient):
        super().__init__("NetworkOptimizationAgent")
        self.llm_client = llm_client
    
    def analyze(self, scan_data: Dict) -> Dict:
        """
        Analyze AWS network scan data and generate optimization recommendations
        
        Args:
            scan_data: AWS scan data dictionary
            
        Returns:
            Dict: Structured recommendations in JSON format
        """
        self.logger.info("Loading scan data for network analysis")
        self.logger.debug(f"Account: {scan_data.get('accountId')}, Region: {scan_data.get('region')}")
        
        system_prompt = """You are a cloud network optimization expert. Analyze NAT gateways, Elastic IPs, and load balancers to identify cost optimization opportunities.

CRITICAL: Respond ONLY with valid JSON. No explanations, no markdown, no code blocks. Just raw JSON.

Output format:
{
  "recommendations": [
    {
      "resourceType": "nat-gateway|elastic-ip|load-balancer",
      "resourceId": "resource identifier",
      "currentCost": 0.00,
      "issue": "description of the problem",
      "evidence": "specific metrics or data supporting the issue",
      "recommendation": "specific action to take",
      "estimatedSavings": 0.00,
      "priority": "high|medium|low",
      "risk": "low|medium|high - risk level of implementing change",
      "remediationCLI": "AWS CLI command to fix the issue",
      "remediationTerraform": "Terraform code snippet to fix the issue"
    }
  ],
  "totalPotentialSavings": 0.00,
  "summary": "brief summary of findings"
}"""
        
        user_prompt = f"""Analyze this AWS infrastructure scan data and provide network optimization recommendations:

{json.dumps(scan_data, indent=2)}

Focus on:
1. NAT Gateways - expensive resource ($0.045/hour + data processing), check if necessary or can use alternatives
2. Unused Elastic IPs - charged when not associated with running instances
3. Idle Load Balancers - no traffic or targets, still incurring hourly charges

For each recommendation provide:
- Clear issue description
- Evidence from metrics (state, associations, traffic data)
- Estimated monthly savings
- Risk level of the change
- AWS CLI command for remediation
- Terraform code snippet for remediation

Return ONLY valid JSON with no additional text."""
        
        self.logger.info("Invoking LLM for network optimization analysis")
        response = self.llm_client.invoke(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.3,
            max_tokens=4000
        )
        
        self.logger.info("Parsing LLM response")
        try:
            cleaned = response.strip()
            if "```json" in cleaned:
                cleaned = cleaned.split("```json")[1].split("```")[0].strip()
            elif "```" in cleaned:
                cleaned = cleaned.split("```")[1].split("```")[0].strip()
            
            recommendations = json.loads(cleaned)
            self.logger.info(f"Successfully parsed recommendations: {len(recommendations.get('recommendations', []))} items")
            self.logger.info(f"Returning recommendations with potential savings: ${recommendations.get('totalPotentialSavings', 0):.2f}")
            return recommendations
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON parse error at position {e.pos}: {e.msg}")
            self.logger.error(f"Response preview: {response[:500]}...")
            raise ValueError(f"LLM did not return valid JSON. Error: {e.msg} at position {e.pos}")
