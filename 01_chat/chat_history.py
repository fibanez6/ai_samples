"""
Chat History: Interactive math assistant chat with message history and rich UI.
"""
from rich.live import Live
from rich.spinner import Spinner

from utils.agentClient import AgentClient
from utils.print_utils import print_agent_messages, print_agent_response

agent = AgentClient()
messages = [
    {"role": "system", "content": "You are an math teacher assistant that help with math problems and uses emojis."}
]

panel_title = (f"Chat History - (Agent: {agent.name.upper()} - Model: {agent.model.upper()})")

def main():

    while True:
        question = input("\nYour math question: ")
        messages.append({"role": "user", "content": question})

        print_agent_messages(messages, title=panel_title)

        spinner = Spinner("dots", text="Waiting for the response...")
        with Live(spinner, refresh_per_second=10):
            response = agent.client.chat.completions.create(
                model=agent.model,
                temperature=0.5,
                messages=messages,
            )

        print_agent_response(response)
        messages.append({"role": "assistant", "content": response.choices[0].message.content})

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting chat...")
    except Exception:
        pass