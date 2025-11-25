"""
Structured Outputs Pydantic Function Tool Example: Extract structured data from text using Pydantic models as function tool.
"""

import openai
import rich
from pydantic import BaseModel

from utils.openAIClient import OpenAIClient
from utils.print_utils import print_agent_messages, print_agent_response

agent = OpenAIClient()


panel_title = (f"Structured Outputs Pydantic Function Tool - (Agent: {agent.name.upper()} - Model: {agent.model.upper()})")

messages = [
    {"role": "system", "content": "You're a Github support bot. Use the tools to assist the developer."},
    {"role": "user", "content": "Extract the Jira number and issue type from this text: 'Fix the bug in PROJ-1234 asap'."},
]

class GetJira(BaseModel):
    jira_number: str
    issue_type: str

def main():

    print_agent_messages(messages, title=panel_title)

    agent_response = agent.chat_completion_create( # <----- Use chat_completion_create to use tools
        model=agent.model,
        temperature=0.7,
        messages=messages,
        tools=[openai.pydantic_function_tool(GetJira)] # <----- Define the tool using the Pydantic model
    )

    print_agent_response(agent_response)

    rich.print(agent_response.choices[0].message)

if __name__ == "__main__":
    main()