"""
Example of using the Microsoft Agent Framework Azure AI module.
"""

import asyncio

import rich
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from pydantic import BaseModel

from agents.microsoft_agent_framework.azure_utils import print_request, print_response
from utils.agent_utils import await_for_response


class PersonInfo(BaseModel):
    """Information about a person."""
    name: str | None = None
    age: int | None = None
    occupation: str | None = None


async def main() -> None:
    """Example of structured output using the Microsoft Agent Framework Azure AI module."""

    # Create an agent
    agent = ChatAgent(
        chat_client=AzureAIAgentClient(async_credential=AzureCliCredential()),
        name="HelpfulAssistant",
        instructions="You are a helpful assistant that extracts person information from text.",
    )

    # Create a message
    message = "Please provide information about John Smith, who is a 35-year-old software engineer."

    # Run the agent and wait for the response
    print_request(message)
    result = await await_for_response(agent.run(message, response_format=PersonInfo))

    # Print the response
    if result.value:
        print_response(result)
    else:
        rich.print("No structured data found in response")

if __name__ == "__main__":
    asyncio.run(main())
