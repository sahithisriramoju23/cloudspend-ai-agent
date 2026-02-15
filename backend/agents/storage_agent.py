"""
Storage Optimization Agent - Analyzes storage resources and generates recommendations
"""
import json
from typing import Dict
from services.llm_client import LLMClient
from utils.logger import setup_logger


class StorageOptimizationAgent:
    """Agent for analyzing storage resources and generating optimization recommendations"""
    
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        self.logger = setup_logger("StorageOptimizationAgent")
    
    def analyze(self, scan_data: Dict) -> Dict:
        """
        Analyze AWS scan data and generate storage optimization recommendations
        
        Args:
            scan_data: AWS scan data dictionary
            
        Returns:
            Dict: Structured recommendations in JSON format
        """
        self.logger.info("Loading scan data for analysis")
        self.logger.debug(f"Account: {scan_data.get('accountId')}, Region: {scan_data.get('region')}")
        
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
        
        self.logger.info("Invoking LLM for storage optimization analysis")
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
