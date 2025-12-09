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

from agents.microsoft_agent_framework.azure_utils import print_request, print_response
from utils.agent_utils import await_for_response


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
        # Define the message
        message = "Tell me a joke about a pirate."

        # Run the agent and wait for the response
        print_request(message)
        result: AgentRunResponse = await await_for_response(agent.run(message))

        # Print the response
        print_response(result)


if __name__ == "__main__":
    asyncio.run(main())
