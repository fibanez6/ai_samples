"""
Function tools and utilities for an Azure AI agent framework.
"""

import asyncio
from datetime import datetime, timezone
from random import randint
from typing import Annotated

from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from pydantic import Field

from utils.agent_utils import await_for_response
from utils.azure_utils import print_agent_response


def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    return f"The weather in {location} is {conditions[randint(0, 3)]} with a high of {randint(10, 30)}°C."


def get_time() -> str:
    """Get the current UTC time."""
    current_time = datetime.now(timezone.utc)
    return f"The current UTC time is {current_time.strftime('%Y-%m-%d %H:%M:%S')}."


def lookup_location(query: str):
    """Lookup the latitude and longitude of a location."""
    mock_db = {
        "Sydney": {"lat": -33.8568, "lon": 151.2153},
        "New York": {"lat": 40.7128, "lon": -74.0060},
    }
    return mock_db.get(query, {"lat": 0, "lon": 0})


async def tools_on_agent_level() -> None:
    """Example showing tools defined when creating the agent."""

    # Create an agent
    agent = ChatAgent(
        chat_client=AzureAIAgentClient(async_credential=AzureCliCredential()),
        instructions="You are a helpful assistant that can provide weather and time information.",
        tools=[get_weather, get_time],  # Tools defined at agent creation
    )

    # First query - agent uses weather tool
    query1 = "What's the weather like in New York?"
    result = await await_for_response(agent.run(query1))

    print_agent_response(result)

    # Second query - agent uses time tool
    # query2 = "What's the time?"
    # result = await await_for_response(agent.run(query2))
    # print_agent_response(result)


async def main() -> None:
    """Example showing tools defined when creating the agent."""
    await tools_on_agent_level()


if __name__ == "__main__":
    asyncio.run(main())
