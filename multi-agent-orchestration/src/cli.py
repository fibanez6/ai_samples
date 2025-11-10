#!/usr/bin/env python3
"""
Command Line Interface for Multi-Agent Orchestration System.
"""

import asyncio
import json
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.json import JSON
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from src.config.settings import (create_default_config_file, get_config,
                                 load_config_from_file)
from src.orchestrator.langgraph_orchestrator import MultiAgentOrchestrator
from src.utils.workflow_utils import ResultsFormatter, WorkflowValidator

app = typer.Typer(help="Multi-Agent Orchestration System CLI")
console = Console()

@app.command()
def execute(
    query: str = typer.Argument(..., help="Research query to execute"),
    urls: Optional[List[str]] = typer.Option(None, "--url", "-u", help="URLs to research"),
    search_terms: Optional[List[str]] = typer.Option(None, "--search", "-s", help="Search terms"),
    max_sources: int = typer.Option(5, "--max-sources", "-m", help="Maximum sources to research"),
    analysis_type: str = typer.Option("comprehensive", "--analysis", "-a", 
                                     help="Analysis type (comprehensive, executive, technical, comparative, critical)"),
    output_file: Optional[str] = typer.Option(None, "--output", "-o", help="Output file for results"),
    config_file: Optional[str] = typer.Option(None, "--config", "-c", help="Configuration file"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
):
    """Execute a multi-agent orchestration workflow."""
    
    async def run_execution():
        try:
            # Load configuration
            if config_file:
                config = load_config_from_file(config_file)
                console.print(f"📄 Loaded configuration from: {config_file}")
            else:
                config = get_config()
            
            # Validate configuration
            validation = config.validate_config()
            if validation["errors"]:
                console.print("❌ Configuration errors:", style="red")
                for error in validation["errors"]:
                    console.print(f"  • {error}", style="red")
                return
            
            if verbose and validation["warnings"]:
                console.print("⚠️ Configuration warnings:", style="yellow")
                for warning in validation["warnings"]:
                    console.print(f"  • {warning}", style="yellow")
            
            # Prepare user input
            user_input = {
                "max_sources": max_sources,
                "analysis_type": analysis_type
            }
            
            if urls:
                user_input["urls"] = list(urls)
            
            if search_terms:
                user_input["search_terms"] = list(search_terms)
            
            # Validate inputs
            query_validation = WorkflowValidator.validate_query(query)
            if not query_validation["valid"]:
                console.print("❌ Query validation failed:", style="red")
                for issue in query_validation["issues"]:
                    console.print(f"  • {issue}", style="red")
                return
            
            input_validation = WorkflowValidator.validate_user_input(user_input)
            if not input_validation["valid"]:
                console.print("❌ Input validation failed:", style="red")
                for issue in input_validation["issues"]:
                    console.print(f"  • {issue}", style="red")
                return
            
            # Display execution info
            console.print("\n🎭 Multi-Agent Orchestration", style="bold blue")
            console.print(Panel(f"[bold]Query:[/bold] {query}", border_style="blue"))
            
            if verbose:
                info_table = Table(show_header=False)
                info_table.add_row("URLs", str(len(urls)) if urls else "0")
                info_table.add_row("Search Terms", str(len(search_terms)) if search_terms else "0")
                info_table.add_row("Max Sources", str(max_sources))
                info_table.add_row("Analysis Type", analysis_type)
                console.print(info_table)
            
            # Initialize orchestrator
            orchestrator = MultiAgentOrchestrator(mcp_base_url=config.mcp_server.base_url)
            
            # Execute with progress indicator
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Executing multi-agent workflow...", total=None)
                
                results = await orchestrator.execute(query, user_input)
                
                progress.update(task, description="✅ Workflow completed!")
            
            # Display results
            console.print("\n" + "="*80)
            console.print("RESULTS", style="bold green", justify="center")
            console.print("="*80)
            
            # Format results for display
            if verbose:
                # Detailed display
                formatted_results = ResultsFormatter.format_for_display(results)
                console.print(formatted_results)
            else:
                # Summary display
                summary = ResultsFormatter.format_summary(results)
                console.print(summary)
                
                # Key insights
                insights = results.get("key_insights", [])
                if insights:
                    console.print(f"\n💡 Key Insights ({len(insights)}):", style="bold")
                    for i, insight in enumerate(insights[:3], 1):  # Show top 3
                        insight_text = insight if isinstance(insight, str) else insight.get('insight', str(insight))
                        console.print(f"{i}. {insight_text[:100]}...")
                
                # Recommendations
                recommendations = results.get("strategic_recommendations", [])
                if recommendations:
                    console.print(f"\n📋 Strategic Recommendations ({len(recommendations)}):", style="bold")
                    for i, rec in enumerate(recommendations[:3], 1):  # Show top 3
                        console.print(f"{i}. {rec[:100]}...")
            
            # Save to file if requested
            if output_file:
                output_path = Path(output_file)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_path, 'w') as f:
                    json.dump(results, f, indent=2)
                
                console.print(f"\n💾 Results saved to: {output_file}", style="green")
            
            return results
            
        except Exception as e:
            console.print(f"❌ Execution failed: {str(e)}", style="red")
            if verbose:
                import traceback
                console.print(traceback.format_exc())
            return None
    
    return asyncio.run(run_execution())

@app.command()
def health():
    """Check system health."""
    
    async def check_health():
        try:
            console.print("🏥 Checking system health...", style="blue")
            
            orchestrator = MultiAgentOrchestrator()
            health_status = await orchestrator.health_check()
            
            # Create health status table
            table = Table(title="System Health Status")
            table.add_column("Component", style="cyan")
            table.add_column("Status", style="green")
            table.add_column("Details")
            
            # Orchestrator status
            table.add_row("Orchestrator", health_status.get('orchestrator', 'unknown'), "")
            
            # MCP Server status
            mcp_status = health_status.get('mcp_server', {})
            if isinstance(mcp_status, dict):
                mcp_health = mcp_status.get('status', 'healthy')
            else:
                mcp_health = str(mcp_status)
            table.add_row("MCP Server", mcp_health, "")
            
            # Agents status
            agents = health_status.get('agents', {})
            for agent_name, agent_status in agents.items():
                name = agent_status.get('name', agent_name)
                conversations = agent_status.get('conversation_length', 0)
                table.add_row(f"Agent: {name}", "healthy", f"{conversations} conversations")
            
            # Execution history
            history_count = health_status.get('execution_history_count', 0)
            table.add_row("Execution History", "available", f"{history_count} entries")
            
            console.print(table)
            
            return health_status
            
        except Exception as e:
            console.print(f"❌ Health check failed: {str(e)}", style="red")
            return None
    
    return asyncio.run(check_health())

@app.command()
def config(
    create: bool = typer.Option(False, "--create", help="Create default configuration file"),
    file: Optional[str] = typer.Option(None, "--file", "-f", help="Configuration file path"),
    validate: bool = typer.Option(False, "--validate", help="Validate configuration"),
    show: bool = typer.Option(False, "--show", help="Show current configuration")
):
    """Configuration management."""
    
    if create:
        config_path = file or "config.json"
        create_default_config_file(config_path)
        console.print(f"✅ Created default configuration: {config_path}", style="green")
        return
    
    if file:
        try:
            config = load_config_from_file(file)
            console.print(f"✅ Loaded configuration from: {file}", style="green")
        except Exception as e:
            console.print(f"❌ Failed to load configuration: {str(e)}", style="red")
            return
    else:
        config = get_config()
    
    if validate:
        validation = config.validate_config()
        
        if validation["errors"]:
            console.print("❌ Configuration errors:", style="red")
            for error in validation["errors"]:
                console.print(f"  • {error}", style="red")
        else:
            console.print("✅ Configuration is valid", style="green")
        
        if validation["warnings"]:
            console.print("⚠️ Configuration warnings:", style="yellow")
            for warning in validation["warnings"]:
                console.print(f"  • {warning}", style="yellow")
    
    if show:
        config_dict = config.dict()
        # Hide sensitive information
        if 'openai' in config_dict and 'api_key' in config_dict['openai']:
            config_dict['openai']['api_key'] = '***HIDDEN***'
        
        console.print("📋 Current Configuration:", style="bold")
        console.print(JSON.from_data(config_dict))

@app.command()
def start_mcp_server(
    host: str = typer.Option("0.0.0.0", "--host", help="Host to bind the server"),
    port: int = typer.Option(8000, "--port", help="Port to bind the server"),
):
    """Start the MCP server using UV."""
    import subprocess
    import sys
    from pathlib import Path
    
    try:
        console.print(f"🚀 Starting MCP server with UV on {host}:{port}", style="blue")
        
        # Get the path to the MCP server module
        server_module = "src.mcp_server.server:app"
        
        # Build UV command
        uv_cmd = [
            "uv", "run", "uvicorn", server_module,
            "--host", host,
            "--port", str(port),
            "--reload",  # Enable auto-reload for development
        ]
        
        console.print(f"📝 Running: {' '.join(uv_cmd)}", style="dim")
        
        # Run the command
        subprocess.run(uv_cmd, check=True)
        
    except subprocess.CalledProcessError as e:
        console.print(f"❌ Failed to start MCP server with UV: {str(e)}", style="red")
        console.print("💡 Make sure UV is installed and you're in the project directory", style="yellow")
    except FileNotFoundError:
        console.print("❌ UV not found. Please install UV first:", style="red")
        console.print("curl -LsSf https://astral.sh/uv/install.sh | sh", style="blue")
    except Exception as e:
        console.print(f"❌ Failed to start MCP server: {str(e)}", style="red")

@app.command()
def examples():
    """Run example workflows."""
    
    async def run_examples():
        try:
            console.print("🎭 Running example workflows...", style="blue")
            
            from src.examples.usage_examples import basic_example
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Running basic example...", total=None)
                
                results = await basic_example()
                
                progress.update(task, description="✅ Example completed!")
            
            if results:
                console.print("✅ Example workflow completed successfully", style="green")
                summary = ResultsFormatter.format_summary(results)
                console.print(summary)
            else:
                console.print("❌ Example workflow failed", style="red")
            
        except Exception as e:
            console.print(f"❌ Examples failed: {str(e)}", style="red")
    
    return asyncio.run(run_examples())

if __name__ == "__main__":
    app()