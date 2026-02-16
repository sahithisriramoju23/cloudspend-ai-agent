"""
Report Agent - Aggregates and summarizes outputs from all optimization agents
"""
import json
from typing import Dict, List
from agents.base_agent import BaseAgent
from services.llm_client import LLMClient


class ReportAgent(BaseAgent):
    """Agent for aggregating and summarizing optimization recommendations"""
    
    def __init__(self, llm_client: LLMClient):
        super().__init__("ReportAgent")
        self.llm_client = llm_client
    
    def analyze(self, agent_outputs: List[Dict]) -> Dict:
        """
        Aggregate outputs from multiple agents and generate executive report
        
        Args:
            agent_outputs: List of outputs from other agents
            
        Returns:
            Dict: Executive report with summary and categorized recommendations
        """
        self.logger.info(f"Aggregating outputs from {len(agent_outputs)} agents")
        
        system_prompt = """You are a cloud cost optimization executive advisor. Analyze the outputs from multiple optimization agents and create a comprehensive executive report.

CRITICAL: Respond ONLY with valid JSON. No explanations, no markdown, no code blocks. Just raw JSON.

Output format:
{
  "executiveSummary": "2-3 sentence high-level summary for executives",
  "totalEstimatedSavings": 0.00,
  "savingsBreakdown": {
    "compute": 0.00,
    "storage": 0.00,
    "network": 0.00
  },
  "top5Savings": [
    {
      "rank": 1,
      "resourceType": "type",
      "resourceId": "id",
      "issue": "brief issue",
      "estimatedSavings": 0.00,
      "priority": "high|medium|low"
    }
  ],
  "categorizedRecommendations": {
    "highPriority": [],
    "mediumPriority": [],
    "lowPriority": []
  },
  "quickWins": "List of easy, low-risk changes that can be implemented immediately",
  "riskAssessment": "Overall risk assessment of implementing all recommendations"
}"""
        
        user_prompt = f"""Analyze these optimization agent outputs and create an executive report:

{json.dumps(agent_outputs, indent=2)}

Create a comprehensive report that includes:
1. Executive summary (2-3 sentences for C-level)
2. Total estimated monthly savings across all categories
3. Savings breakdown by category (compute, storage, network)
4. Top 5 highest-impact savings opportunities ranked by estimated savings
5. Categorized recommendations by priority (high, medium, low)
6. Quick wins - easy, low-risk changes
7. Overall risk assessment

Return ONLY valid JSON with no additional text."""
        
        self.logger.info("Invoking LLM for report generation")
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
            
            report = json.loads(cleaned)
            self.logger.info(f"Successfully generated executive report")
            self.logger.info(f"Total estimated savings: ${report.get('totalEstimatedSavings', 0):.2f}")
            return report
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON parse error at position {e.pos}: {e.msg}")
            self.logger.error(f"Response preview: {response[:500]}...")
            raise ValueError(f"LLM did not return valid JSON. Error: {e.msg} at position {e.pos}")
