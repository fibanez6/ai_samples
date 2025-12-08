"""
Chat Parallel: Async assistant chat generating multiple sport descriptions concurrently.
"""

import asyncio

from agents.openAIClient import AsyncOpenAIClient
from utils.agent_utils import await_for_response
from utils.print_utils import print_agent_messages, print_agent_response

agent = AsyncOpenAIClient()  # <----- Use async agent client


async def generate_response(sport: str):
    messages = [
        {
            "role": "system",
            "content": "You are an assistant that makes meme references and uses emojis.",
        },
        {
            "role": "user",
            "content": f"Generate a short description of {sport} as a sport",
        },
    ]

    panel_title = f"Chat Async - {sport} - (Agent: {agent.name.upper()} - Model: {agent.model.upper()})"

    print_agent_messages(messages, title=panel_title)

    agent_response = await await_for_response(
        agent.client.chat.completions.create(
            model=agent.model,
            temperature=0.7,
            messages=messages,
        ),
        spinner_text=f"Waiting for the response for {sport}..."
    )

    panel_title = f"Agent Response for sport: {sport}"
    print_agent_response(agent_response, title=panel_title)


async def main():
    try:
        await asyncio.gather(
            generate_response("Football"),
            generate_response("Soccer"),
            generate_response("Tennis"),
        )
    finally:
        await agent.client.close()


if __name__ == "__main__":
    asyncio.run(main())
