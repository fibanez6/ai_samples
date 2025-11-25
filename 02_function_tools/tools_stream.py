"""
Basic example of using an agent with tools + streaming.
Compatible with standard ChatCompletionChunk API.
"""

import json

from rich import print

from utils.openAIClient import OpenAIClient
from utils.print_utils import print_agent_messages, print_agent_response

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
    return {
        "location": location,
        "temperature": 22,
        "unit": unit,
        "description": "clear sky ☀️",
    }


agent = OpenAIClient()
messages = [
    {"role": "system", "content": "You are a weather bot using emojis."},
    {"role": "user", "content": "What's the weather in Tokyo?"}
]
panel_title = f"Tools Stream - (Agent: {agent.name.upper()} - Model: {agent.model.upper()})"
available_functions = {
    "lookup_weather": lookup_weather
}

# -----------------------------------------------------------------------------
def stream_with_tools(messages):

    print_agent_messages(messages, title=panel_title)

    stream = agent.chat_completion_create(
        model=agent.model,
        temperature=0.7,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        stream=True,
    )

    print("[yellow]\n--- Streaming initial assistant reply ---[/yellow]\n")

    # --- Only 1 tool call normally; but we support multiple ---
    current_call_id = None
    current_call_name = None
    args_buffer = ""
    content_buffer = ""

    for event in stream:
        if not event.choices:
            continue

        delta = event.choices[0].delta

        # --- 1. TEXT STREAM (normal tokens) ---
        if delta.content:
            content_buffer += delta.content

        # --- 2. TOOL CALL STREAM ---   
        if delta.tool_calls:
            tc = delta.tool_calls[0]  # only one per chunk
            func = tc.function

            # If it's the first chunk → capture ID + name
            if tc.id is not None:
                current_call_id = tc.id
                current_call_name = func.name

            # Accumulate argument fragments
            if func.arguments:
                args_buffer += func.arguments

        # --- END OF TOOL CALL ---
        if event.choices[0].finish_reason == "tool_calls":
            break

    # Build object exactly like your ToolCall type wrapper
    print("\n\n--- Tool call captured ---\n")
    print(f"[green]Tool call message: id={current_call_id}, name={current_call_name}, arguments={args_buffer}[/green]")

    return {
        "content": content_buffer,
        "tool_call": {
            "id": current_call_id,
            "name": current_call_name,
            "arguments": args_buffer
        }
    }

# -----------------------------------------------------------------------------
def main():
    # Step 1 — Stream first reply and detect tool calls
    response = stream_with_tools(messages)

    tool_call = response["tool_call"]
    if not tool_call["name"]:
        print("[red]No tool calls detected.[/red]")
        return
    
    # Step 2 - Append ASSISTANT TOOL CALL MESSAGE (no intermediate assistant content!)
    messages.append({
        "role": "assistant",
        "tool_calls": [
            {
                "id": tool_call["id"],
                "type": "function",
                "function": {
                    "name": tool_call["name"],
                    "arguments": tool_call["arguments"],
                }
            }
        ],
        "content": None
    })

    # Step 3 — Execute tool calls
    call_args = json.loads(tool_call["arguments"])
    func = available_functions[tool_call["name"]]
    result = func(**call_args)

    messages.append({
        "role": "tool",
        "tool_call_id": tool_call["id"],
        "content": json.dumps(result),
    })

    # Step 4 — Final assistant reply
    print("\n--- Final assistant reply ---\n")

    print_agent_messages(messages, title=panel_title)

    followup = agent.chat_completion_create(
        model=agent.model,
        temperature=0.7,
        messages=messages,
        tools=tools,
    )

    print_agent_response(followup)



# -----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
