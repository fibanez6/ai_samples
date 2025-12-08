"""
Basic Agent example of using the Microsoft Agent Framework Azure AI module.

A `ChatAgent` is a core component within the agent framework, designed to manage and drive conversational interactions.
It acts as the "brain" of the agent, encapsulating behavior rather than just text.

Key responsibilities include:
- Receiving and processing incoming messages.
- Orchestrating calls to external tools or functions.
- Applying reasoning or predefined policies to determine the next action.
- Generating appropriate responses.
- Producing the subsequent `ChatMessage` within the conversation flow.
"""

import asyncio

from agent_framework import ChatAgent
from agent_framework._types import AgentRunResponse
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

from utils.agent_utils import await_for_response
from utils.azure_utils import print_agent_response


async def main() -> None:
    """Example of streaming response (get the complete result at once)."""

    # Create an agent
    async with (
        AzureCliCredential() as credential,
        ChatAgent(
            AzureAIAgentClient(async_credential=credential),
            name="Joker",
            instructions="You are good at telling jokes.",
        ) as agent,
    ):

        # Run the agent and wait for the response
        result: AgentRunResponse = await await_for_response(
            agent.run("Tell me a joke about a pirate.")
        )

        # Print the response
        print_agent_response(result)


if __name__ == "__main__":
    asyncio.run(main())
