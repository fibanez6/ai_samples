"""
Example of chat with image URI.
"""

import asyncio

from agent_framework import ChatMessage, Role, TextContent, UriContent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

from utils.agent_utils import wait_for_response
from utils.azure_utils import print_agent_response


async def main() -> None:
    """Example of chat with image URI."""

    # Create an agent
    async with (
        AzureCliCredential() as credential,
        AzureAIAgentClient(async_credential=credential).create_agent(
            name="Image Analyzer",
            instructions="What do you see in this image?",
        ) as agent,
    ):

        # Create a message
        message = ChatMessage(
            role=Role.USER,
            contents=[
                TextContent(text="What do you see in this image?"),
                UriContent(
                    uri="https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_92x30dp.png",
                    media_type="image/png",
                ),
            ],
        )

        # Run the agent and wait for the response
        result = await wait_for_response(agent.run(message))

        # Print the response
        print_agent_response(result)


if __name__ == "__main__":
    asyncio.run(main())
