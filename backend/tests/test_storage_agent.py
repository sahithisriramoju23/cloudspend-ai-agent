"""
Tests for StorageOptimizationAgent
"""
import pytest
import json
from pathlib import Path
from unittest.mock import Mock
from backend.agents.storage_agent import StorageOptimizationAgent


@pytest.fixture
def mock_llm_client():
    """Mock LLM client that returns valid JSON"""
    client = Mock()
    client.invoke.return_value = json.dumps({
        "recommendations": [
            {
                "resourceType": "ebs",
                "resourceId": "vol-123",
                "currentCost": 10.0,
                "issue": "Underutilized volume",
                "recommendation": "Reduce size",
                "estimatedSavings": 5.0,
                "priority": "medium"
            }
        ],
        "totalPotentialSavings": 5.0,
        "summary": "Test summary"
    })
    return client


@pytest.fixture
def sample_scan_data():
    """Load sample scan data"""
    scan_file = Path(__file__).parent.parent.parent / "mock-data" / "aws" / "scan-sample.json"
    with open(scan_file, "r") as f:
        return json.load(f)


def test_storage_agent_returns_recommendations(mock_llm_client, sample_scan_data):
    """Test that agent returns recommendations array"""
    agent = StorageOptimizationAgent(mock_llm_client)
    result = agent.analyze(sample_scan_data)
    
    assert "recommendations" in result
    assert isinstance(result["recommendations"], list)
    assert len(result["recommendations"]) > 0


def test_storage_agent_returns_required_keys(mock_llm_client, sample_scan_data):
    """Test that result contains all required keys"""
    agent = StorageOptimizationAgent(mock_llm_client)
    result = agent.analyze(sample_scan_data)
    
    assert "recommendations" in result
    assert "totalPotentialSavings" in result
    assert "summary" in result


def test_recommendation_structure(mock_llm_client, sample_scan_data):
    """Test that each recommendation has required fields"""
    agent = StorageOptimizationAgent(mock_llm_client)
    result = agent.analyze(sample_scan_data)
    
    for rec in result["recommendations"]:
        assert "resourceType" in rec
        assert "resourceId" in rec
        assert "currentCost" in rec
        assert "issue" in rec
        assert "recommendation" in rec
        assert "estimatedSavings" in rec
        assert "priority" in rec


def test_llm_client_invoked(mock_llm_client, sample_scan_data):
    """Test that LLM client is invoked with correct parameters"""
    agent = StorageOptimizationAgent(mock_llm_client)
    agent.analyze(sample_scan_data)
    
    mock_llm_client.invoke.assert_called_once()
    call_args = mock_llm_client.invoke.call_args
    
    assert "system_prompt" in call_args.kwargs
    assert "user_prompt" in call_args.kwargs
    assert call_args.kwargs["temperature"] == 0.3
    assert call_args.kwargs["max_tokens"] == 2000
