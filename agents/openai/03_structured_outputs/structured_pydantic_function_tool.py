"""
Structured Outputs Pydantic Function Tool Example: Extract structured data from text using Pydantic models as function tool.
"""

import openai
import rich
from pydantic import BaseModel

from agents.openai.openai_client import OpenAIClient
from agents.openai.print_utils import print_request, print_response
from utils.agent_utils import wait_for_response

agent = OpenAIClient()

panel_title = f"Structured Outputs Pydantic Function Tool - (Agent: {agent.name.upper()} - Model: {agent.model.upper()})"

messages = [
    {
        "role": "system",
        "content": "You're a Github support bot. Use the tools to assist the developer.",
    },
    {
        "role": "user",
        "content": "Extract the Jira number and issue type from this text: 'Fix the bug in PROJ-1234 asap'.",
    },
]


class GetJira(BaseModel):
    jira_number: str
    issue_type: str


def main():

    print_request(messages, title=panel_title)

    agent_response = (
        wait_for_response(agent.client.chat.completions.create(  # <----- Use chat completion create to use tools
            model=agent.model,
            temperature=0.7,
            messages=messages,
            tools=[
                openai.pydantic_function_tool(GetJira)
            ],  # <----- Define the tool using the Pydantic model
        ))
    )

    print_response(agent_response)

    rich.print(agent_response.choices[0].message)


if __name__ == "__main__":
    main()
