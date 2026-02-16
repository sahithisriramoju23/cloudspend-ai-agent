"""
Compute Optimization Agent - Analyzes EC2 instances for cost optimization
"""
import json
from typing import Dict
from backend.agents.base_agent import BaseAgent
from backend.utils.llm_client import LLMClient


class ComputeOptimizationAgent(BaseAgent):
    """Agent for analyzing compute resources and generating optimization recommendations"""
    
    def __init__(self, llm_client: LLMClient):
        super().__init__("ComputeOptimizationAgent")
        self.llm_client = llm_client
    
    def analyze(self, scan_data: Dict) -> Dict:
        """
        Analyze AWS EC2 scan data and generate compute optimization recommendations
        
        Args:
            scan_data: AWS scan data dictionary
            
        Returns:
            Dict: Structured recommendations in JSON format
        """
        self.logger.info("Loading scan data for compute analysis")
        self.logger.debug(f"Account: {scan_data.get('accountId')}, Region: {scan_data.get('region')}")
        
        system_prompt = """You are a cloud compute optimization expert. Analyze EC2 instances and CloudWatch metrics to identify cost optimization opportunities.

CRITICAL: Respond ONLY with valid JSON. No explanations, no markdown, no code blocks. Just raw JSON.

Output format:
{
  "recommendations": [
    {
      "resourceType": "ec2",
      "resourceId": "instance-id",
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
        
        user_prompt = f"""Analyze this AWS infrastructure scan data and provide compute optimization recommendations:

{json.dumps(scan_data, indent=2)}

Focus on:
1. Underutilized EC2 instances (low CPU utilization < 20% average)
2. Stopped instances still incurring storage costs
3. Overprovisioned instance types (can be downsized)

For each recommendation provide:
- Clear issue description
- Evidence from metrics (CPU utilization, state, etc.)
- Estimated monthly savings
- Risk level of the change
- AWS CLI command for remediation
- Terraform code snippet for remediation

Return ONLY valid JSON with no additional text."""
        
        self.logger.info("Invoking LLM for compute optimization analysis")
        response = self.llm_client.invoke(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.3,
            max_tokens=4000
        )
        
        self.logger.info("Parsing LLM response")
        # Parse and validate JSON response
        try:
            # Clean response
            cleaned = response.strip()
            # Remove markdown if present
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
