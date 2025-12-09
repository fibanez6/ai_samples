"""
Chat Stream: Assistant chat with streaming response and emojis.
"""

import rich

from agents.openai.openai_client import OpenAIClient
from agents.openai.print_utils import print_request
from utils.agent_utils import wait_for_response

agent = OpenAIClient()
messages = [
    {"role": "system", "content": "You are an assistant that uses emojis."},
    {"role": "user", "content": "Please tell me a joke about computers."},
]
panel_title = (
    f"Chat Stream - (Agent: {agent.name.upper()} - Model: {agent.model.upper()})"
)


def main():

    print_request(messages, title=panel_title)

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
