"""
Structured Outputs Basic: Extract structured data from text using JSON Schema.
"""
from utils.openAIClient import OpenAIClient
from utils.print_utils import print_agent_messages, print_agent_response

agent = OpenAIClient()
panel_title = (f"Structured Outputs Basic - (Agent: {agent.name.upper()} - Model: {agent.model.upper()})")
json_schema = {
    "name": "PersonInfo",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
            "email": {"type": "string", "format": "email"}
        },
        "required": ["name", "age", "email"],
        "additionalProperties": False
    }
}
text_to_parse = "Información: Bob Fronz, 29 year old, bob.f@example.com."
messages = [
    {"role": "system", "content": "You are an assistant that helps with structured data. Extract name, age, and email from the text and return as JSON."},
    {"role": "user", "content": f"Extract name, age and email from this text: {text_to_parse}"},
]


def main():

    print_agent_messages(messages, title=panel_title)

    agent_response = agent.chat_completion_create(
        model=agent.model,
        temperature=0.7,
        messages=messages,
        response_format={
            "type": "json_schema",
            "json_schema": json_schema
        }
    )

    print_agent_response(agent_response)

if __name__ == "__main__":
    main()