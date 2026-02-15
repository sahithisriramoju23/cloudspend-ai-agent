"""
Storage Optimization Agent - Analyzes storage resources and generates recommendations
"""
import json
from typing import Dict
from backend.utils.llm_client import LLMClient


class StorageOptimizationAgent:
    """Agent for analyzing storage resources and generating optimization recommendations"""
    
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
    
    def analyze(self, scan_data: Dict) -> Dict:
        """
        Analyze AWS scan data and generate storage optimization recommendations
        
        Args:
            scan_data: AWS scan data dictionary
            
        Returns:
            Dict: Structured recommendations in JSON format
        """
        system_prompt = """You are a cloud storage optimization expert. Analyze the provided AWS scan data and generate cost optimization recommendations.

CRITICAL: Respond ONLY with valid JSON. No explanations, no markdown, no code blocks. Just raw JSON.

Output format:
{
  "recommendations": [
    {
      "resourceType": "ebs|s3|rds",
      "resourceId": "resource identifier",
      "currentCost": 0.00,
      "issue": "description of inefficiency",
      "recommendation": "specific action to take",
      "estimatedSavings": 0.00,
      "priority": "high|medium|low"
    }
  ],
  "totalPotentialSavings": 0.00,
  "summary": "brief summary of findings"
}"""
        
        user_prompt = f"""Analyze this AWS infrastructure scan data and provide storage optimization recommendations:

{json.dumps(scan_data, indent=2)}

Focus on:
- EBS volumes: underutilized, oversized, or wrong type
- S3 buckets: storage class optimization opportunities
- RDS storage: oversized or inefficient configurations

Return ONLY valid JSON with no additional text."""
        
        response = self.llm_client.invoke(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.3,
            max_tokens=2000
        )
        
        # Parse and validate JSON response
        try:
            recommendations = json.loads(response.strip())
            return recommendations
        except json.JSONDecodeError:
            # Attempt to extract JSON if wrapped in markdown
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
                return json.loads(json_str)
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
                return json.loads(json_str)
            raise ValueError(f"LLM did not return valid JSON: {response}")
