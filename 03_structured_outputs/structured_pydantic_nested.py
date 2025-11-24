"""
Structured Outputs Pydantic Nested: Extract structured data from text using nested Pydantic models.
"""

from pydantic import BaseModel
import rich
from utils.agentClient import AgentClient
from utils.print_utils import print_agent_messages, print_agent_response

agent = AgentClient()


panel_title = (f"Structured Outputs Pydantic Nested - (Agent: {agent.name.upper()} - Model: {agent.model.upper()})")

messages = [
    {"role": "system", "content": "Extract the event information."},
    {"role": "user", "content": "Alice the designer and Bob the architect are going to a science event on Tuesday."},
]

class Participant(BaseModel):
    name: str
    job_title: str


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[Participant]

def main():

    print_agent_messages(messages, title=panel_title)

    agent_response = agent.chat_completion_parse(
        model=agent.model,
        temperature=0.7,
        messages=messages,
        response_format=CalendarEvent # <----- Use the Pydantic model here
    )

    print_agent_response(agent_response)

    rich.print(agent_response.choices[0].message)

if __name__ == "__main__":
    main()