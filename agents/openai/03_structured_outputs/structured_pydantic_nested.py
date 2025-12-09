"""
Structured Outputs Pydantic Nested: Extract structured data from text using nested Pydantic models.
"""

import rich
from pydantic import BaseModel

from agents.openai.openai_client import OpenAIClient
from agents.openai.print_utils import print_request, print_response
from utils.agent_utils import wait_for_response

agent = OpenAIClient()


panel_title = f"Structured Outputs Pydantic Nested - (Agent: {agent.name.upper()} - Model: {agent.model.upper()})"

messages = [
    {"role": "system", "content": "Extract the event information."},
    {
        "role": "user",
        "content": "Alice the designer and Bob the architect are going to a science event on Tuesday.",
    },
]


class Participant(BaseModel):
    name: str
    job_title: str


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[Participant]


def main():

    print_request(messages, title=panel_title)

    agent_response = wait_for_response(agent.client.chat.completions.parse(
        model=agent.model,
        temperature=0.7,
        messages=messages,
        response_format=CalendarEvent,  # <----- Use the Pydantic model here
    ))

    print_response(agent_response)

    rich.print(agent_response.choices[0].message)


if __name__ == "__main__":
    main()
