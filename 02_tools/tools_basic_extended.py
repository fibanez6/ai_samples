"""
Tools Basic Extended: Assistant chat using a tool (function) to lookup weather information with emoji responses.
"""
import json
from rich import print
from rich.live import Live
from rich.spinner import Spinner

from utils.agentClient import AgentClient
from utils.print_utils import print_agent_messages, print_agent_response

# --- Define the tool (function) ---
tools=[
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
                "required": ["location"]
            },
        },
    }
]

def lookup_weather(location: str, unit: str = "celsius"):
    # Dummy implementation
    return {
        "location": location,
        "temperature": 22,
        "unit": unit,
        "description": "clear sky"
    }

agent = AgentClient()
messages = [
    {"role": "system", "content": "You are a weather assistant that uses emojis."},
    {"role": "user", "content": "What's the weather like in Sydney right now?"},
]

panel_title = (f"Tools Basic Extended - (Agent: {agent.name.upper()} - Model: {agent.model.upper()})")

def main():
    print_agent_messages(messages, title=panel_title)

    agent_response = agent.chat_completion_create(
        model=agent.model,
        temperature=0.7,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        parallel_tool_calls=False,
    )

    print_agent_response(agent_response)

    # Handle tool calls if any
    if agent_response.choices[0].message.tool_calls:
        tool_call = agent_response.choices[0].message.tool_calls[0]

        # Execute the tool based on the tool call
        if tool_call.function.name == "lookup_weather":
            
            # Append the assistant's message with the tool call to the messages
            messages.append(agent_response.choices[0].message)

            args = json.loads(tool_call.function.arguments)
            weather_info = lookup_weather(**args)

            # Append the tool's response to the messages
            messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": str(weather_info)})

            # Get a final response from the agent after tool execution
            final_response = agent.chat_completion_create(
                model=agent.model,
                temperature=0.7,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                parallel_tool_calls=False,
            )
            print_agent_response(final_response)
    else:
        print(agent_response.choices[0].message.content)

if __name__ == "__main__":
    main()