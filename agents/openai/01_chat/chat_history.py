"""
Chat History: Interactive math assistant chat with message history and rich UI.
"""

from agents.openai.openai_client import OpenAIClient
from agents.openai.print_utils import print_request, print_response
from utils.agent_utils import wait_for_response

agent = OpenAIClient()
messages = [
    {
        "role": "system",
        "content": "You are an math teacher assistant that help with math problems and uses emojis.",
    }
]

panel_title = (
    f"Chat History - (Agent: {agent.name.upper()} - Model: {agent.model.upper()})"
)


def main():
    """ Run the agent with chat history. """

    while True:
        question = input("\nYour math question: ")
        messages.append({"role": "user", "content": question})

        print_request(messages, title=panel_title)

        agent_response = wait_for_response(agent.client.chat.completions.create(
            model=agent.model,
            temperature=0.5,
            messages=messages,
        ))

        print_response(agent_response)
        messages.append(
            {"role": "assistant", "content": agent_response.choices[0].message.content}
        )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting chat...")
    except Exception:
        pass
