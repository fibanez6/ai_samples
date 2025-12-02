"""
Basic example of using the Microsoft Agent Framework Azure AI module.
"""

import asyncio
import os

import rich
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv

# Load environment variables
# load_dotenv(override=True)

async def main() -> None:
    """Example of non-streaming response (get the complete result at once)."""
    async with (
        AzureCliCredential() as credential,
        ChatAgent(
            AzureAIAgentClient(async_credential=credential),
            instructions="You are good at telling jokes.",
        ) as agent,
    ):
        result = await agent.run("Tell me a joke about a pirate.")
        rich.print(result)


if __name__ == "__main__":
    asyncio.run(main())
