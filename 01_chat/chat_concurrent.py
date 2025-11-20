"""
Chat Concurrent: Async assistant chat generating multiple sport descriptions concurrently.
"""
import asyncio

from rich.live import Live
from rich.spinner import Spinner

from utils.agentAsyncClient import AgentAsyncClient
from utils.print_utils import print_agent_messages, print_agent_response

agent = AgentAsyncClient() # <----- Use async agent client

async def generate_response(sport: str):
    messages = [
        {"role": "system", "content": "You are an assistant that makes meme references and uses emojis."},
        {"role": "user", "content": f"Generate a short description of {sport} as a sport"},
    ]

    panel_title = (f"Chat Concurrent - {sport} - (Agent: {agent.name.upper()} - Model: {agent.model.upper()})")

    print_agent_messages(messages, title=panel_title)

    spinner = Spinner("dots", text=f"Waiting for the response for {sport}...")
    with Live(spinner, refresh_per_second=10):
        response = await agent.client.chat.completions.create(
            model=agent.model,
            temperature=0.7,
            messages=messages,
        )

    panel_title = (f"Agent Response for sport: {sport}")
    print_agent_response(response, title=panel_title)

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
