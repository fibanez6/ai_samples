"""
Chat Basic: Simple assistant chat with movie references and emojis.
"""

from agents.openAIClient import OpenAIClient
from utils.agent_utils import wait_for_response
from utils.print_utils import print_agent_messages, print_agent_response

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

    print_agent_messages(messages, title=panel_title)

    agent_response = wait_for_response(agent.client.chat.completions.create(
        model=agent.model,
        temperature=0.7,
        messages=messages,
    ))

    print_agent_response(agent_response)


if __name__ == "__main__":
    main()
