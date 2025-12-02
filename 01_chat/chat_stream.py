"""
Chat Stream: Assistant chat with streaming response and emojis.
"""

from rich import print

from agents.openAIClient import OpenAIClient
from utils.print_utils import print_agent_messages

agent = OpenAIClient()
messages = [
    {"role": "system", "content": "You are an assistant that uses emojis."},
    {"role": "user", "content": "Please tell me a joke about computers."},
]
panel_title = (
    f"Chat Stream - (Agent: {agent.name.upper()} - Model: {agent.model.upper()})"
)


def main():

    print_agent_messages(messages, title=panel_title)

    agent_response = agent.chat_completion_create(
        model=agent.model,
        temperature=0.7,
        messages=messages,
        stream=True,  # <----- Enable streaming response
    )

    print("\n")

    for event in agent_response:
        if event.choices:
            content = event.choices[0].delta.content
            if content:
                print(content, end="", flush=True)


if __name__ == "__main__":
    main()
