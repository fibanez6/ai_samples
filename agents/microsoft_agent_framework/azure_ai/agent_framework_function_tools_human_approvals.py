# """
# Function tools and utilities for an Azure AI agent framework.
# """

import asyncio
from random import randint
from typing import Annotated

import rich
from agent_framework import ChatMessage, Role, ai_function
from agent_framework._types import AgentRunResponseUpdate, TextContent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from pydantic import Field

from agents.microsoft_agent_framework.azure_utils import print_request, print_response
from utils.agent_utils import await_for_response


@ai_function
def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    return f"The weather in {location} is {conditions[randint(0, 3)]} with a high of {randint(10, 30)}°C."

@ai_function(approval_mode="always_require")
def get_weather_detail(
    location: Annotated[str, Field(description="The city and state, e.g. San Francisco, CA")]
) -> str:
    """Get detailed weather information for a given location."""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    return f"The weather in {location} is {conditions[randint(0, 3)]} with a high of {randint(10, 30)}°C."

async def handle_approvals(query: str, agent) -> AgentRunResponseUpdate:
    """Handle function call approvals in a loop."""

    conversation_history = [ChatMessage(role=Role.USER, contents=[TextContent(text=query)])]
    max_iterations = 5
    processed_approvals = set()  # Track which approvals we've already processed

    for iteration in range(max_iterations):
        # Run the agent and wait for the response
        print_request(conversation_history, title=f"Agent Request Messages - Iteration {iteration + 1}")
        
        # Run the agent and wait for the response
        result = await await_for_response(agent.run(conversation_history))

        # Print the agent response
        print_response(result)
        
        if result is None:
            rich.print("⚠ Warning: Received None result from agent")
            break

        if not result.user_input_requests:
            rich.print("✓ No more approvals needed. Task completed.")
            return result

        # Add the assistant message with the approval request
        new_approvals = False
        for user_input_needed in result.user_input_requests:
            approval_id = user_input_needed.function_call.name

            rich.print(f"Processed Approvals: {processed_approvals}")
            
            # Check if we've already processed this approval
            if approval_id in processed_approvals:
                rich.print(f"⚠ Skipping duplicate approval request: {approval_id}")
                continue

            rich.print(f"\n⚠ Approval needed for: {user_input_needed.function_call.name}")
            rich.print(f"Arguments: {user_input_needed.function_call.arguments}")
            rich.print(f"Approval ID: {user_input_needed.id}")

            # Mark this approval as processed
            processed_approvals.add(approval_id)
            new_approvals = True

            # Add the assistant message with the approval request
            conversation_history.append(ChatMessage(role=Role.ASSISTANT, contents=[user_input_needed]))

            # Get user approval (in practice, this would be interactive)
            user_approval_input = ""
            while user_approval_input.lower() not in ["yes", "no"]:
                user_approval_input = input(f"Approve function call '{user_input_needed.function_call.name}'? (yes/no): ")
            user_approval = user_approval_input.lower() == "yes"
            # user_approval = True  # Replace with actual user input
            
            rich.print(f"{'✓' if user_approval else '✗'} Approval: {user_approval}")

            # Add the user's approval response
            conversation_history.append(
                ChatMessage(role=Role.USER, contents=[user_input_needed.create_response(user_approval)])
            )

        if not new_approvals:
            rich.print("⚠ No new approvals to process, breaking loop")
            break

    rich.print(f"⚠ Max iterations ({max_iterations}) reached.")
    return result


async def main() -> None:
    """Example of function tools with human approvals using the Microsoft Agent Framework Azure AI module."""

    # Create credential and client with proper cleanup
    async with AzureCliCredential() as credential:
        client = AzureAIAgentClient(async_credential=credential)
        
        # Create an agent
        agent = client.create_agent(
            name="WeatherAgent",
            instructions="You are a helpful assistant that can provide weather information.",
            tools=[get_weather, get_weather_detail],  # Tools defined at agent creation
        )

        # Handle approvals
        final_result = await handle_approvals("Get detailed weather for Seattle", agent)
        print_response(final_result)

        # Cleanup: close the agent client if it has a close method
        if hasattr(client, 'close'):
            await client.close()

if __name__ == "__main__":
    asyncio.run(main())
