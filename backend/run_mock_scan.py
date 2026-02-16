"""
Mock Scan Runner - Test StorageOptimizationAgent with sample data
"""
import json
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from services.gemini_client import GeminiClient
from agents.orchestrator_agent import OrchestratorAgent


def main():
    # Load mock scan data
    scan_file = Path(__file__).parent.parent / "mock-data" / "aws" / "scan-sample.json"
    
    with open(scan_file, "r") as f:
        scan_data = json.load(f)
    
    print("=" * 60)
    print("CloudSpend AI - Multi-Agent Cost Optimization Analysis")
    print("=" * 60)
    print(f"\nLoaded scan data from: {scan_file}")
    print(f"Account: {scan_data['accountId']}")
    print(f"Region: {scan_data['region']}")
    print(f"Total Monthly Cost: ${scan_data['costSummary']['totalMonthlyCost']}")
    print("\nRunning multi-agent analysis...\n")
    
    # Initialize orchestrator with Gemini client
    llm_client = GeminiClient()
    orchestrator = OrchestratorAgent(llm_client)
    
    # Run orchestrated analysis
    result = orchestrator.analyze(scan_data)
    
    # Save output to file
    output_dir = Path(__file__).parent.parent / "docs" / "sample-output"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "report.json"
    
    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    print(f"\nScan ID: {result['scanId']}")
    print(f"Timestamp: {result['timestamp']}")
    print(f"\nOutput saved to: {output_file}")
    
    # Print executive summary
    if "report" in result and "executiveSummary" in result["report"]:
        print("\n" + "=" * 60)
        print("EXECUTIVE SUMMARY")
        print("=" * 60)
        print(f"\n{result['report']['executiveSummary']}")
        
        if "totalEstimatedSavings" in result["report"]:
            print(f"\nTotal Potential Savings: ${result['report']['totalEstimatedSavings']:.2f}/month")
        
        if "top5Savings" in result["report"]:
            print("\n" + "=" * 60)
            print("TOP 5 SAVINGS OPPORTUNITIES")
            print("=" * 60)
            for item in result["report"]["top5Savings"]:
                print(f"\n{item['rank']}. {item['resourceType']} - {item['resourceId']}")
                print(f"   Issue: {item['issue']}")
                print(f"   Savings: ${item['estimatedSavings']:.2f}/month")
                print(f"   Priority: {item['priority']}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
