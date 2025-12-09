#!/usr/bin/env python3
"""
Quick start script for Multi-Agent Orchestration System.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.append(str(Path(__file__).parent / "src"))

try:
    from src.config.settings import create_default_config_file, get_config
    from src.orchestrator.langgraph_orchestrator import MultiAgentOrchestrator
    from src.utils.workflow_utils import ResultsFormatter
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you've installed the dependencies with: uv sync")
    sys.exit(1)

async def quick_demo():
    """Run a quick demonstration of the system."""
    print("🎭 Multi-Agent Orchestration System - Quick Demo")
    print("=" * 60)
    
    # Check for OpenAI API key
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OpenAI API key not found!")
        print("Please set your OPENAI_API_KEY environment variable or create a .env file")
        print("Copy .env.example to .env and add your API key")
        return
    
    # Simple demo query
    query = "What are the key benefits of remote work for modern companies?"
    
    print(f"📝 Demo Query: {query}")
    print("🚀 Starting orchestration...")
    
    try:
        # Initialize orchestrator
        orchestrator = MultiAgentOrchestrator()
        
        # Execute with simple parameters
        user_input = {
            "search_terms": ["remote work benefits", "distributed teams"],
            "max_sources": 2,  # Keep it simple for demo
            "analysis_type": "executive"
        }
        
        results = await orchestrator.execute(query, user_input)
        
        # Display results
        print("\n" + "="*60)
        print("DEMO RESULTS")
        print("="*60)
        
        summary = ResultsFormatter.format_summary(results)
        print(summary)
        
        # Show key insights
        insights = results.get("key_insights", [])
        if insights:
            print(f"\n💡 Key Insights:")
            for i, insight in enumerate(insights[:3], 1):
                insight_text = insight if isinstance(insight, str) else insight.get('insight', str(insight))
                print(f"{i}. {insight_text[:150]}...")
        
        # Show recommendations
        recommendations = results.get("strategic_recommendations", [])
        if recommendations:
            print(f"\n📋 Recommendations:")
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"{i}. {rec[:150]}...")
        
        print(f"\n✅ Demo completed successfully!")
        print(f"📊 Generated {len(insights)} insights and {len(recommendations)} recommendations")
        
        # Show next steps with UV commands
        print(f"\n🚀 Next Steps - Try these UV commands:")
        print(f"  uv run uvicorn src.mcp_server.server:app --reload  # Start MCP server")
        print(f"  uv run python -m src.cli execute 'Your query here'  # Run custom queries")
        print(f"  uv run python -m src.cli examples  # Run more examples")
        print(f"  uv run python -m src.cli health    # Check system health")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        print("This might be due to:")
        print("- Invalid OpenAI API key")
        print("- Network connectivity issues")
        print("- Missing MCP server (try starting it separately)")
        print("\n🔧 Troubleshooting:")
        print("  uv run python -m src.cli health  # Check system status")
        print("  uv run uvicorn src.mcp_server.server:app --reload  # Start MCP server")

def main():
    """Main entry point."""
    print("🚀 Multi-Agent Orchestration System")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    
    # Check if we're in the right directory
    if not (Path.cwd() / "src").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Create default config if it doesn't exist
    if not Path("config.json").exists():
        print("📝 Creating default configuration...")
        create_default_config_file()
    
    # Run the demo
    try:
        asyncio.run(quick_demo())
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()