"""
Basic Chat Streaming example of using the Microsoft Agent Framework Azure AI module.
"""

import asyncio

from agent_framework import ChatMessage, Role, TextContent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential


async def main() -> None:
    """Example of chat streaming response (get the complete result at once)."""

    # Create an agent
    async with (
        AzureCliCredential() as credential,
        AzureAIAgentClient(async_credential=credential).create_agent(
            name="Joker",
            instructions="You are good at telling jokes.",
        ) as agent,
    ):
        # Create a message
        message = ChatMessage(
            role=Role.USER,
            contents=[TextContent(text="Tell me a joke about a pirate.")],
        )

        # Run the agent and stream the response
        async for chunk in agent.run_stream(message):
            if chunk.text:
                print(chunk.text, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
