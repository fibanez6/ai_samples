"""
Chat Stream: Assistant chat with streaming response and emojis.
"""
from rich import print
from rich.live import Live
from rich.spinner import Spinner

from utils.agentClient import AgentClient
from utils.print_utils import print_agent_messages

agent = AgentClient()
messages = [
    {"role": "system", "content": "You are an assistant that uses emojis."},
    {"role": "user", "content": "Please tell me a joke about computers."},
]
panel_title = (f"Chat Stream - (Agent: {agent.name.upper()} - Model: {agent.model.upper()})")

def main():

    print_agent_messages(messages, title=panel_title)

    spinner = Spinner("dots", text="Waiting for the response...")
    with Live(spinner, refresh_per_second=10):
        response = agent.client.chat.completions.create(
            model=agent.model,
            temperature=0.7,
            messages=messages,
            stream=True, # <----- Enable streaming response
        )
    
    print("")

    for event in response:
        if event.choices:
            content = event.choices[0].delta.content
            if content:
                print(content, end="", flush=True)

if __name__ == "__main__":
    main()