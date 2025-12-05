""" """

import asyncio
import os

from agent_framework import ChatMessage, DataContent, Role, TextContent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

from utils.agent_utils import wait_for_response
from utils.print_utils import print_agent_response


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
        script_path = os.path.abspath(__file__)
        image_path = os.path.join(os.path.dirname(script_path), "../docs/images/Gfp-wisconsin-madison-the-nature-boardwalk.jpg")

        # Read the image file
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        if not image_bytes:
            raise ValueError(f"Image file at {image_path} is empty or could not be read.")

        # Create a message
        message = ChatMessage(
            role=Role.USER,
            contents=[
                TextContent(text="What do you see in this image?"),
                DataContent(
                    data=image_bytes,
                    media_type="image/jpeg"
                )
            ]
        )

        # Run the agent and wait for the response
        result = await wait_for_response(agent.run(message))

        # Print the response
        print_agent_response(result)


if __name__ == "__main__":
    asyncio.run(main())
