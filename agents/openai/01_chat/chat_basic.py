"""
Chat Basic: Simple assistant chat with movie references and emojis.
"""

from agents.openai.openai_client import OpenAIClient
from agents.openai.print_utils import print_request, print_response
from utils.agent_utils import wait_for_response

agent = OpenAIClient()
messages = [
    {
        "role": "system",
        "content": "You are an assistant that makes movie references and uses emojis.",
    },
    {"role": "user", "content": "What happens today in Melbourne?"},
]

panel_title = (
    f"Chat Basic - (Agent: {agent.name.upper()} - Model: {agent.model.upper()})"
)


def main():
    """Main function to run the chat basic example."""

    print_request(messages, title=panel_title)

    agent_response = wait_for_response(agent.client.chat.completions.create(
        model=agent.model,
        temperature=0.7,
        messages=messages,
    ))

    print_response(agent_response)


if __name__ == "__main__":
    main()
