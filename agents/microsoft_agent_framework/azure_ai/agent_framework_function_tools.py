"""
Function tools and utilities for an Azure AI agent framework.
"""

import asyncio
from datetime import datetime, timezone
from random import randint
from typing import Annotated

import rich
from agent_framework import ChatMessage, Role, TextContent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from pydantic import Field

from agents.microsoft_agent_framework.azure_utils import print_request, print_response
from utils.agent_utils import await_for_response


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

async def tools_on_agent_level() -> None:
    """Example showing tools defined when creating the agent."""

    rich.print("-" * 80)
    rich.print("tools_on_agent_level")
    rich.print("-" * 80)

    # Create credential and client with proper cleanup
    async with AzureCliCredential() as credential:
        client = AzureAIAgentClient(async_credential=credential)
        
        # Create an agent
        agent = client.create_agent(
            name="WeatherAgent",
            instructions="You are a helpful assistant that can provide weather and time information.",
            tools=[get_weather, get_time],  # Tools defined at agent creation
        )

        # First query - agent uses weather tool
        query1 = ChatMessage(
            role=Role.USER,
            contents=[TextContent(text="What's the weather like in New York?")],
        )
        print_request(query1)
        result = await await_for_response(agent.run(query1))
        print_response(result)

        # Second query - agent uses time tool
        query2 = ChatMessage(
            role=Role.USER,
            contents=[TextContent(text="What's the time?")],
        )
        print_request(query2)
        result = await await_for_response(agent.run(query2))
        print_response(result)
        
        # Cleanup: close the agent client if it has a close method
        if hasattr(client, 'close'):
            await client.close()

async def tools_on_run_level() -> None:
    """Example showing tools passed to the run method."""

    rich.print("-" * 80)
    rich.print("tools_on_run_level")
    rich.print("-" * 80)

    # Create credential and client with proper cleanup
    async with AzureCliCredential() as credential:
        client = AzureAIAgentClient(async_credential=credential)
        
        # Create an agent
        agent = client.create_agent(
            name="WeatherAgent",
            instructions="You are a helpful assistant that can provide weather and time information.",
        )

        # First query - agent uses weather tool
        query1 = ChatMessage(
            role=Role.USER,
            contents=[TextContent(text="What's the weather like in New York?")],
        )
        print_request(query1)
        result = await await_for_response(agent.run(query1, tools=[get_weather]))
        print_response(result)

        # Second query - agent uses time tool
        query2 = ChatMessage(
            role=Role.USER,
            contents=[TextContent(text="What's the time?")],
        )
        print_request(query2)
        result = await await_for_response(agent.run(query2, tools=[get_time]))
        print_response(result)
        
        # Cleanup: close the agent client if it has a close method
        if hasattr(client, 'close'):
            await client.close()

async def mixed_tools_example() -> None:
    """Example showing both agent-level tools and run-method tools."""

    rich.print("-" * 80)
    rich.print("mixed_tools_example")
    rich.print("-" * 80)

    # Create credential and client with proper cleanup
    async with AzureCliCredential() as credential:
        client = AzureAIAgentClient(async_credential=credential)
        
        # Create an agent
        agent = client.create_agent(
            name="WeatherAgent",
            instructions="You are a helpful assistant that can provide weather and time information.",
            tools=[get_weather],  # Tools defined at agent creation
        )

        # First query - agent uses weather tool
        query1 = ChatMessage(
            role=Role.USER,
            contents=[TextContent(text="What's the weather like in New York?")],
        )
        print_request(query1)
        result = await await_for_response(agent.run(query1))
        print_response(result)

        # Second query - agent uses time tool
        query2 = ChatMessage(
            role=Role.USER,
            contents=[TextContent(text="What's the time?")],
        )
        print_request(query2)
        result = await await_for_response(agent.run(query2, tools=[get_time]))
        print_response(result)
        
        # Cleanup: close the agent client if it has a close method
        if hasattr(client, 'close'):
            await client.close()

async def main() -> None:
    """Example showing tools defined when creating the agent."""
    await tools_on_agent_level()
    await tools_on_run_level()
    await mixed_tools_example()


if __name__ == "__main__":
    asyncio.run(main())
