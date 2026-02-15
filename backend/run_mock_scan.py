"""
Mock Scan Runner - Test StorageOptimizationAgent with sample data
"""
import json
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from services.groq_client import GroqClient
from agents.storage_agent import StorageOptimizationAgent


def main():
    # Load mock scan data
    scan_file = Path(__file__).parent.parent / "mock-data" / "aws" / "scan-sample.json"
    
    with open(scan_file, "r") as f:
        scan_data = json.load(f)
    
    print("=" * 60)
    print("CloudSpend AI - Storage Optimization Analysis")
    print("=" * 60)
    print(f"\nLoaded scan data from: {scan_file}")
    print(f"Account: {scan_data['accountId']}")
    print(f"Region: {scan_data['region']}")
    print(f"Total Monthly Cost: ${scan_data['costSummary']['totalMonthlyCost']}")
    print("\nAnalyzing storage resources...\n")
    
    # Initialize agent with Groq client
    llm_client = GroqClient()
    agent = StorageOptimizationAgent(llm_client)
    
    # Run analysis
    recommendations = agent.analyze(scan_data)
    
    # Print results
    print("=" * 60)
    print("OPTIMIZATION RECOMMENDATIONS")
    print("=" * 60)
    print(json.dumps(recommendations, indent=2))
    print("\n" + "=" * 60)
    
    if "totalPotentialSavings" in recommendations:
        print(f"Total Potential Savings: ${recommendations['totalPotentialSavings']:.2f}/month")
    print("=" * 60)


if __name__ == "__main__":
    main()
