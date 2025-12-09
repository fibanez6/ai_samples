""" """

import json
from concurrent.futures import ThreadPoolExecutor

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
    },
    {
        "type": "function",
        "function": {
            "name": "lookup_location",
            "description": "Return latitude/longitude and country for a given city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name to look up."}
                },
                "required": ["city"],
            },
        },
    },
]


def lookup_weather(location: str, unit: str = "celsius"):
    # Dummy implementation
    return {
        "location": location,
        "temperature": 22,
        "unit": unit,
        "description": "clear sky",
    }


def lookup_location(city: str):
    """Dummy geocoding tool."""
    database = {
        "sydney": {"lat": -33.8688, "lng": 151.2093, "country": "Australia"},
        "tokyo": {"lat": 35.6762, "lng": 139.6503, "country": "Japan"},
        "new york": {"lat": 40.7128, "lng": -74.0060, "country": "USA"},
    }

    key = city.lower().strip()
    if key in database:
        return database[key]
    else:
        return {"error": f"City '{city}' not found in database."}


agent = OpenAIClient()
messages = [
    {"role": "system", "content": "You are a weather assistant that uses emojis."},
    {"role": "user", "content": "What's the weather and location in Sydney?"},
]

panel_title = f"Tools Multiple Parallel - (Agent: {agent.name.upper()} - Model: {agent.model.upper()})"

# Map function names to actual functions
available_functions = {
    "lookup_weather": lookup_weather,
    "lookup_location": lookup_location,
}


def main():
    """ Run the agent with tools. """

    print_request(messages, title=panel_title)

    agent_response = wait_for_response(agent.client.chat.completions.create(
        model=agent.model,
        temperature=0.7,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        # parallel_tool_calls=False, <----- Disable sequential tool calls
    ))

    print_response(agent_response)

    # Handle tool calls if any
    if agent_response.choices[0].message.tool_calls:
        tool_call = agent_response.choices[0].message.tool_calls

        # Append the assistant's message with the tool call to the messages
        messages.append(agent_response.choices[0].message)

        # Execute tool calls in parallel
        with ThreadPoolExecutor() as executor:
            futures = []

            # Loop through each tool call
            for call in tool_call:
                # Get the function name and arguments
                function_name = call.function.name
                args = json.loads(call.function.arguments)

                rich.print(f"Tool request: {function_name}({args})")

                # Submit the function to be executed in parallel
                if function_name in available_functions:
                    func = available_functions[function_name]
                    future = executor.submit(func, **args)

                    # Store the future along with tool call and function name
                    futures.append((call, function_name, future))
                else:
                    rich.print(f"[red]Function '{function_name}' not found.[/red]")

            # Add each tool result to the conversation
            for tool_call, function_name, future in futures:
                result = future.result()
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result),
                    }
                )

        rich.print("\n[bold green]Tool results added to the conversation.[/bold green]\n")

        # Get final response from the model with all tool results
        final_response = wait_for_response(agent.client.chat.completions.create(
            model=agent.model,
            temperature=0.7,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        ))

        # Display the final response
        print_response(final_response)
    else:
        rich.print(agent_response.choices[0].message.content)


if __name__ == "__main__":
    main()
