"""
Example usage of the Multi-Agent Orchestration system.
This example demonstrates how to use the system for research, analysis, and action planning.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.config.settings import create_default_config_file, get_config
from src.orchestrator.langgraph_orchestrator import MultiAgentOrchestrator
from src.utils.workflow_utils import ResultsFormatter, WorkflowValidator


async def basic_example():
    """Basic example of multi-agent orchestration."""
    print("🚀 Multi-Agent Orchestration - Basic Example")
    print("=" * 50)
    
    # Initialize orchestrator
    orchestrator = MultiAgentOrchestrator()
    
    # Define the research query
    query = "What are the latest trends in AI and machine learning for 2024?"
    
    # Optional: Define additional parameters
    user_input = {
        "urls": [
            "https://arxiv.org/list/cs.AI/recent",
            "https://www.nature.com/subjects/machine-learning"
        ],
        "search_terms": ["AI trends 2024", "machine learning developments"],
        "max_sources": 3,
        "analysis_type": "comprehensive",
        "objectives": [
            "Identify key AI trends for 2024",
            "Understand market implications",
            "Provide actionable insights"
        ]
    }
    
    # Validate inputs
    query_validation = WorkflowValidator.validate_query(query)
    input_validation = WorkflowValidator.validate_user_input(user_input)
    
    if not query_validation["valid"]:
        print(f"❌ Query validation failed: {query_validation['issues']}")
        return
    
    if not input_validation["valid"]:
        print(f"❌ Input validation failed: {input_validation['issues']}")
        return
    
    print(f"✅ Inputs validated successfully")
    print(f"📝 Query: {query}")
    print(f"🔗 URLs to research: {len(user_input['urls'])}")
    print(f"🔍 Search terms: {len(user_input['search_terms'])}")
    
    try:
        # Execute the multi-agent workflow
        print("\n🎭 Starting multi-agent orchestration...")
        results = await orchestrator.execute(query, user_input)
        
        # Validate results
        output_validation = WorkflowValidator.validate_workflow_output(results)
        if not output_validation["valid"]:
            print(f"⚠️ Output validation issues: {output_validation['issues']}")
        
        # Format and display results
        print("\n" + "=" * 80)
        print("RESULTS")
        print("=" * 80)
        
        formatted_results = ResultsFormatter.format_for_display(results)
        print(formatted_results)
        
        # Display summary
        print("\n" + ResultsFormatter.format_summary(results))
        
        return results
        
    except Exception as e:
        print(f"❌ Orchestration failed: {str(e)}")
        return None

async def advanced_example():
    """Advanced example with custom configuration and error handling."""
    print("\n🚀 Multi-Agent Orchestration - Advanced Example")
    print("=" * 50)
    
    # Load configuration
    config = get_config()
    
    # Check configuration
    validation_results = config.validate_config()
    if validation_results["errors"]:
        print(f"❌ Configuration errors: {validation_results['errors']}")
        return
    
    if validation_results["warnings"]:
        print(f"⚠️ Configuration warnings: {validation_results['warnings']}")
    
    # Initialize orchestrator with custom settings
    orchestrator = MultiAgentOrchestrator(
        mcp_base_url=config.mcp_server.base_url
    )
    
    # Complex research query
    query = """
    Analyze the competitive landscape for AI-powered customer service solutions.
    Focus on market leaders, emerging technologies, and strategic recommendations
    for a mid-size company looking to implement AI customer service.
    """
    
    user_input = {
        "urls": [
            "https://www.gartner.com/en/information-technology",
            "https://www.forrester.com/",
        ],
        "search_terms": [
            "AI customer service solutions",
            "conversational AI market",
            "chatbot competitive analysis"
        ],
        "max_sources": 5,
        "analysis_type": "competitive",
        "focus_areas": [
            "Market positioning",
            "Technology capabilities",
            "Pricing strategies",
            "Integration complexity"
        ],
        "objectives": [
            "Identify top 5 AI customer service solutions",
            "Compare features and pricing",
            "Assess implementation complexity",
            "Provide vendor recommendations"
        ],
        "constraints": {
            "budget": "Mid-market budget constraints",
            "timeline": "6-month implementation timeline",
            "technical_resources": "Limited technical team"
        }
    }
    
    try:
        print(f"📊 Advanced orchestration starting...")
        print(f"🎯 Focus areas: {', '.join(user_input['focus_areas'])}")
        print(f"📋 Objectives: {len(user_input['objectives'])}")
        
        # Execute with timeout
        from src.utils.workflow_utils import run_with_timeout
        
        results = await run_with_timeout(
            orchestrator.execute(query, user_input),
            timeout_seconds=600,  # 10 minutes timeout
            timeout_message="Advanced orchestration timed out"
        )
        
        # Save results to file
        import json
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"results_advanced_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"💾 Results saved to: {results_file}")
        
        # Display formatted results
        formatted_results = ResultsFormatter.format_for_display(results)
        print(formatted_results)
        
        return results
        
    except TimeoutError as e:
        print(f"⏰ {str(e)}")
        return None
    except Exception as e:
        print(f"❌ Advanced orchestration failed: {str(e)}")
        return None

async def health_check_example():
    """Example of system health checking."""
    print("\n🏥 System Health Check Example")
    print("=" * 50)
    
    orchestrator = MultiAgentOrchestrator()
    
    try:
        health_status = await orchestrator.health_check()
        
        print("🔍 Health Check Results:")
        print(f"  Orchestrator: {health_status['orchestrator']}")
        print(f"  MCP Server: {health_status.get('mcp_server', {}).get('status', 'unknown')}")
        print(f"  Execution History: {health_status['execution_history_count']} entries")
        
        # Agent status
        agents_status = health_status.get('agents', {})
        for agent_name, status in agents_status.items():
            print(f"  {agent_name}: {status.get('name', 'Unknown')} - {status.get('conversation_length', 0)} conversations")
        
        return health_status
        
    except Exception as e:
        print(f"❌ Health check failed: {str(e)}")
        return None

async def batch_processing_example():
    """Example of processing multiple queries in batch."""
    print("\n📦 Batch Processing Example")
    print("=" * 50)
    
    orchestrator = MultiAgentOrchestrator()
    
    # Define multiple queries
    queries = [
        {
            "query": "What are the benefits of remote work for companies?",
            "user_input": {
                "search_terms": ["remote work benefits", "distributed teams"],
                "max_sources": 2,
                "analysis_type": "executive"
            }
        },
        {
            "query": "How to implement cybersecurity best practices for small businesses?",
            "user_input": {
                "search_terms": ["small business cybersecurity", "security best practices"],
                "max_sources": 2,
                "analysis_type": "technical"
            }
        }
    ]
    
    results = []
    for i, query_data in enumerate(queries, 1):
        print(f"\n🔄 Processing query {i}/{len(queries)}")
        print(f"📝 Query: {query_data['query'][:50]}...")
        
        try:
            result = await orchestrator.execute(
                query_data["query"],
                query_data["user_input"]
            )
            results.append({
                "query": query_data["query"],
                "result": result,
                "status": "success"
            })
            print(f"✅ Query {i} completed successfully")
            
        except Exception as e:
            results.append({
                "query": query_data["query"],
                "error": str(e),
                "status": "failed"
            })
            print(f"❌ Query {i} failed: {str(e)}")
    
    # Summary
    successful = len([r for r in results if r["status"] == "success"])
    print(f"\n📊 Batch Processing Complete:")
    print(f"  Total queries: {len(queries)}")
    print(f"  Successful: {successful}")
    print(f"  Failed: {len(queries) - successful}")
    
    return results

async def main():
    """Main function to run all examples."""
    print("🎭 Multi-Agent Orchestration System Examples")
    print("=" * 60)
    
    # Check if configuration exists
    if not os.path.exists('.env'):
        print("⚠️ No .env file found. Creating example configuration...")
        create_default_config_file("config.json")
        print("📝 Created config.json - please review and update with your settings")
        print("📝 Copy .env.example to .env and add your OpenAI API key")
        return
    
    # Run examples
    examples = [
        ("Basic Example", basic_example),
        ("Health Check", health_check_example),
        ("Advanced Example", advanced_example),
        ("Batch Processing", batch_processing_example),
    ]
    
    for example_name, example_func in examples:
        print(f"\n{'='*20} {example_name} {'='*20}")
        try:
            await example_func()
            print(f"✅ {example_name} completed")
        except Exception as e:
            print(f"❌ {example_name} failed: {str(e)}")
        
        # Pause between examples
        print("\n⏸️ Press Enter to continue to next example...")
        input()

if __name__ == "__main__":
    asyncio.run(main())