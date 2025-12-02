"""
Run an agent that uses the MCP client to interact with the MCP server.

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

# Load environment variables
load_dotenv(override=True)

# MCP server URL
MCP_SERVER_URL = "http://localhost:8000/sse"
base_model = ChatOpenAI(
    model=os.getenv("GITHUB_MODEL", "gpt-4o"),
    base_url=os.getenv("GITHUB_API_URL", "https://models.github.ai/inference"),
    api_key=SecretStr(os.environ["GITHUB_TOKEN"]),
)


async def run_agent() -> None:
    """
    Run an agent that uses the MCP client to interact with the MCP server.
    """

    # Initialize MCP client
    client = MultiServerMCPClient(
        {
            "expenses": {
                "url": MCP_SERVER_URL,
                "transport": "sse",
            }
        }
    )

    # Get tools and create agent
    tools = await client.get_tools()
    agent = create_agent(base_model, tools)

    # Prepare query with context
    today = datetime.now().strftime("%Y-%m-%d")
    user_query = "yesterday I bought a laptop for $1200 using my visa."

    # Invoke agent
    response = await agent.ainvoke(
        {
            "messages": [
                SystemMessage(content=f"Today's date is {today}."),
                HumanMessage(content=user_query),
            ]
        }
    )

    # Display result
    final_response = response["messages"][-1].content
    print(final_response)


if __name__ == "__main__":
    asyncio.run(run_agent())
