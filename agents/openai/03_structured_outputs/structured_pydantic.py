"""
Structured Outputs Pydantic: Extract structured data from text using Pydantic models.
"""

import rich
from pydantic import BaseModel

from agents.openai.openai_client import OpenAIClient
from agents.openai.print_utils import print_request, print_response
from utils.agent_utils import wait_for_response

agent = OpenAIClient()
panel_title = f"Structured Outputs Pydantic - (Agent: {agent.name.upper()} - Model: {agent.model.upper()})"

text_to_parse = (
    "Information: Mr Bob Fronz, 29 year old, bob.f@example.com, born on 1994-04-15."
)
messages = [
    {
        "role": "system",
        "content": "You are an assistant that helps with structured data. Extract name, age, and email from the text and return as JSON.",
    },
    {
        "role": "user",
        "content": f"Extract name, age and email from this text: {text_to_parse}",
    },
]


class PersonInfo(BaseModel):
    name: str
    age: int
    email: str


def main():

    print_request(messages, title=panel_title)

    agent_response = wait_for_response(agent.client.chat.completions.parse(
        model=agent.model,
        temperature=0.7,
        messages=messages,
        response_format=PersonInfo,  # <----- Use the Pydantic model here
    ))

    print_response(agent_response)

    message = agent_response.choices[0].message
    if message.refusal:
        rich.print(message.refusal)
    else:
        event = message.parsed
        rich.print(event)


if __name__ == "__main__":
    main()
