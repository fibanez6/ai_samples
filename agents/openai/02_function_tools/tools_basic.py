"""
Basic example of using an agent with tools.
"""
import json

import rich

from agents.openai.openai_client import OpenAIClient
from agents.openai.print_utils import print_request, print_response
from utils.agent_utils import wait_for_response

# --- Define the tool (function) ---
tools = [
    {
        "type": "function",
        "function": {
            "name": "lookup_weather",
            "description": "Get the current weather for a location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },
    }
]


def lookup_weather(location: str, unit: str = "celsius"):
    """
    Get the current weather for a location.
    
    Args:
        location: The location to get weather for
        unit: Temperature unit, either 'celsius' or 'fahrenheit' (default: 'celsius')
    
    Returns:
        dict: Weather information containing location, temperature, unit, and description
    """
    # Dummy implementation
    return {
        "location": location,
        "temperature": 22,
        "unit": unit,
        "description": "clear sky",
    }


agent = OpenAIClient()
messages = [
    {"role": "system", "content": "You are a weather assistant that uses emojis."},
    {"role": "user", "content": "What's the weather like in Sydney right now?"},
]

panel_title = (
    f"Tools Basic - (Agent: {agent.name.upper()} - Model: {agent.model.upper()})"
)


def main():
    """ Run the agent with tools. """

    print_request(messages, title=panel_title)

    # Chat Completion
    agent_response = wait_for_response(agent.client.chat.completions.create(
        model=agent.model,
        temperature=0.7,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        parallel_tool_calls=False,
    ))

    print_response(agent_response)

    # Handle tool calls if any
    if agent_response.choices[0].message.tool_calls:
        tool_call = agent_response.choices[0].message.tool_calls[0]

        # Execute the tool based on the tool call
        if tool_call.function.name == "lookup_weather":
            args = json.loads(tool_call.function.arguments)
            weather_info = lookup_weather(**args)
            rich.print(f"[bold green]Weather Info:[/bold green] {weather_info}")
    else:
        rich.print(agent_response.choices[0].message.content)


if __name__ == "__main__":
    main()
