"""
Structured Outputs Pydantic: Extract structured data from text using Pydantic models.
"""

from pydantic import BaseModel
import rich
from utils.agentClient import AgentClient
from utils.print_utils import print_agent_messages, print_agent_response

agent = AgentClient()
panel_title = (f"Structured Outputs Pydantic - (Agent: {agent.name.upper()} - Model: {agent.model.upper()})")

text_to_parse = "Information: Mr Bob Fronz, 29 year old, bob.f@example.com, born on 1994-04-15."
messages = [
    {"role": "system", "content": "You are an assistant that helps with structured data. Extract name, age, and email from the text and return as JSON."},
    {"role": "user", "content": f"Extract name, age and email from this text: {text_to_parse}"},
]

class PersonInfo(BaseModel):
    name: str
    age: int
    email: str

def main():

    print_agent_messages(messages, title=panel_title)

    agent_response = agent.chat_completion_parse(
        model=agent.model,
        temperature=0.7,
        messages=messages,
        response_format=PersonInfo # <----- Use the Pydantic model here
    )

    print_agent_response(agent_response)

    message = agent_response.choices[0].message
    if message.refusal:
        rich.print(message.refusal)
    else:
        event = message.parsed
        rich.print(event)

if __name__ == "__main__":
    main()