"""
Chat Basic: Simple assistant chat with movie references and emojis.
"""
from rich.live import Live
from rich.spinner import Spinner

from utils.agentClient import AgentClient
from utils.print_utils import print_agent_messages, print_agent_response

agent = AgentClient()
messages = [
    {"role": "system", "content": "You are an assistant that makes movie references and uses emojis."},
    {"role": "user", "content": "What happens today in Melbourne?"},
]

panel_title = (f"Chat Basic - (Agent: {agent.name.upper()} - Model: {agent.model.upper()})")

def main():

    print_agent_messages(messages, title=panel_title)

    spinner = Spinner("dots", text="Waiting for the response...")
    with Live(spinner, refresh_per_second=10):
        response = agent.client.chat.completions.create(
            model=agent.model,
            temperature=0.7,
            messages=messages,
        )

    print_agent_response(response)

if __name__ == "__main__":
    main()