"""
Chat Stream: Assistant chat with streaming response and emojis.
"""

import rich

from agents.openAIClient import OpenAIClient
from utils.agent_utils import wait_for_response
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

    agent_response = wait_for_response(agent.client.chat.completions.create(
        model=agent.model,
        temperature=0.7,
        messages=messages,
        stream=True,  # <----- Enable streaming response
    ))

    rich.print("\n")

    for event in agent_response:
        if event.choices:
            content = event.choices[0].delta.content
            if content:
                rich.print(content, end="", flush=True)


if __name__ == "__main__":
    main()
