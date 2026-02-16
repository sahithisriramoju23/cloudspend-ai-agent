"""
Schema Validator - Validates agent outputs against expected schemas
"""
from jsonschema import validate, ValidationError
from typing import Dict
from utils.logger import setup_logger

logger = setup_logger("SchemaValidator")

# Agent output schema
AGENT_OUTPUT_SCHEMA = {
    "type": "object",
    "required": ["recommendations", "totalPotentialSavings", "summary"],
    "properties": {
        "recommendations": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["resourceType", "resourceId", "currentCost", "issue", 
                           "recommendation", "estimatedSavings", "priority"],
                "properties": {
                    "resourceType": {"type": "string"},
                    "resourceId": {"type": "string"},
                    "currentCost": {"type": "number"},
                    "issue": {"type": "string"},
                    "evidence": {"type": "string"},
                    "recommendation": {"type": "string"},
                    "estimatedSavings": {"type": "number"},
                    "priority": {"type": "string", "enum": ["high", "medium", "low"]},
                    "risk": {"type": "string", "enum": ["low", "medium", "high"]},
                    "remediationCLI": {"type": "string"},
                    "remediationTerraform": {"type": "string"}
                }
            }
        },
        "totalPotentialSavings": {"type": "number"},
        "summary": {"type": "string"}
    }
}

# Report schema
REPORT_SCHEMA = {
    "type": "object",
    "required": ["executiveSummary", "totalEstimatedSavings", "top5Savings"],
    "properties": {
        "executiveSummary": {"type": "string"},
        "totalEstimatedSavings": {"type": "number"},
        "savingsBreakdown": {"type": "object"},
        "top5Savings": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["rank", "resourceType", "resourceId", "issue", 
                           "estimatedSavings", "priority"],
                "properties": {
                    "rank": {"type": "integer"},
                    "resourceType": {"type": "string"},
                    "resourceId": {"type": "string"},
                    "issue": {"type": "string"},
                    "estimatedSavings": {"type": "number"},
                    "priority": {"type": "string"}
                }
            }
        },
        "categorizedRecommendations": {"type": "object"},
        "quickWins": {"type": "string"},
        "riskAssessment": {"type": "string"}
    }
}


def validate_agent_output(output: Dict, agent_name: str) -> bool:
    """
    Validate agent output against schema
    
    Args:
        output: Agent output dictionary
        agent_name: Name of the agent for logging
        
    Returns:
        bool: True if valid, raises ValidationError if invalid
    """
    try:
        validate(instance=output, schema=AGENT_OUTPUT_SCHEMA)
        logger.info(f"{agent_name} output validated successfully")
        return True
    except ValidationError as e:
        logger.error(f"{agent_name} output validation failed: {e.message}")
        raise


def validate_report(report: Dict) -> bool:
    """
    Validate report output against schema
    
    Args:
        report: Report dictionary
        
    Returns:
        bool: True if valid, raises ValidationError if invalid
    """
    try:
        validate(instance=report, schema=REPORT_SCHEMA)
        logger.info("Report validated successfully")
        return True
    except ValidationError as e:
        logger.error(f"Report validation failed: {e.message}")
        raise
