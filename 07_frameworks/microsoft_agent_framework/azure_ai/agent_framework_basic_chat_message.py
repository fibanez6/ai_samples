"""
Basic Chat example of using the Microsoft Agent Framework Azure AI module.

A `ChatMessage` represents a single message within a conversational interaction. It primarily serves as a data container, holding the content and context of an utterance, rather than encapsulating behavior.

Key attributes of a `ChatMessage` include:
- `role`: Specifies the sender of the message (e.g., `user`, `assistant`, `system`, `tool`).
- `content`: Holds the primary payload of the message, which can be text or a structured object.
- Optional `metadata`: Contains additional contextual information like timestamps, tool call details, or function results.

It can be thought of as: 'An object that stores what someone said.'
"""

import asyncio

from agent_framework import ChatMessage, Role, TextContent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

from utils.agent_utils import wait_for_response
from utils.azure_utils import print_agent_response


async def main() -> None:
    """Example of non-streaming response (get the complete result at once)."""

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

        # Run the agent and wait for the response
        result = await wait_for_response(agent.run(message))

        # Print the response
        print_agent_response(result)


if __name__ == "__main__":
    asyncio.run(main())
