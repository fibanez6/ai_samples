"""
Run an agent that uses the MCP client to interact with the Github MCP server.

reference: https://github.com/Azure-Samples/python-mcp-demo/tree/main
"""

import asyncio
import logging
import os
from datetime import datetime

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from rich import print

# Load environment variables
load_dotenv(override=True)

# MCP server URL
MCP_SERVER_URL = "https://api.githubcopilot.com/mcp/"
base_model = ChatOpenAI(
    model=os.getenv("GITHUB_MODEL", "gpt-4o"),
    base_url=os.getenv("GITHUB_API_URL", "https://models.github.ai/inference"),
    api_key=SecretStr(os.environ["GITHUB_TOKEN"]),
)


async def run_agent() -> None:
    """
    Run an agent that uses the MCP client to interact with the Github MCP server.
    """

    # Initialize MCP client
    mcp_client = MultiServerMCPClient({
        "github": {
            "url": "https://api.githubcopilot.com/mcp/",
            "transport": "streamable_http",
            "headers": {"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"},
        }
    })

    # Get tools
    all_tools = await mcp_client.get_tools()
    print(f"[dim]Total tools available: {len(all_tools)}[/dim]\n")

    # Filter to ONLY read operations
    safe_tool_names = ['search_repositories', 'search_code']
    filtered_tools = [t for t in all_tools if t.name in safe_tool_names]

    # Show filtered tools
    print("[bold cyan]Filtered Tools (read-only):[/bold cyan]")
    for tool in filtered_tools:
        print(f"  ✓ {tool.name}")
    
    # Show what was filtered out
    blocked_tools = [t for t in all_tools if 'create' in t.name or 'update' in t.name or 'fork' in t.name]
    if blocked_tools:
        print(f"\n[dim]Blocked tools ({len(blocked_tools)}): " + ", ".join([t.name for t in blocked_tools[:5]]) + "...[/dim]")


    # Create agent with filtered tools
    agent = create_agent(
        model=base_model,
        tools=filtered_tools,
        system_prompt="You help users research GitHub repositories. Search and analyze information."
    )

    # Prepare query
    query = "Find popular Python MCP server repositories"
    print(f"[bold]Query:[/bold] {query}\n")
    
    # Invoke agent
    try:
        response = await agent.ainvoke(
            {
                "messages": [
                    HumanMessage(content=query),
                ]
            }
        )
        print(f"[bold green]Result:[/bold green]\n{response['messages'][-1].content}\n")
    except Exception as e:
        print(f"[bold red]Error:[/bold red] {str(e)}\n")


if __name__ == "__main__":
    asyncio.run(run_agent())
