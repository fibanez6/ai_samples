"""
Chat History: Interactive math assistant chat with message history and rich UI.
"""
from utils.openAIClient import OpenAIClient
from utils.print_utils import print_agent_messages, print_agent_response

agent = OpenAIClient()
messages = [
    {"role": "system", "content": "You are an math teacher assistant that help with math problems and uses emojis."}
]

panel_title = (f"Chat History - (Agent: {agent.name.upper()} - Model: {agent.model.upper()})")

def main():

    while True:
        question = input("\nYour math question: ")
        messages.append({"role": "user", "content": question})

        print_agent_messages(messages, title=panel_title)

        agent_response = agent.chat_completion_create(
            model=agent.model,
            temperature=0.5,
            messages=messages,
        )

        print_agent_response(agent_response)
        messages.append({"role": "assistant", "content": agent_response.choices[0].message.content})

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting chat...")
    except Exception:
        pass