"""
Basic Agent Streaming example of using the Microsoft Agent Framework Azure AI module.
"""

import asyncio

from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from rich import print


async def main() -> None:
    """Example of non-streaming response (get the complete result at once)."""

    # Create an agent
    async with (
        AzureCliCredential() as credential,
        ChatAgent(
            AzureAIAgentClient(async_credential=credential),
            name="Joker",
            instructions="You are good at telling jokes.",
        ) as agent,
    ):

        # Run the agent and stream the response
        query = "Tell me a joke about a pirate."
        async for chunk in agent.run_stream(query):
            if chunk.text:
                print(chunk.text, end="", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
