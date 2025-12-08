import json

import rich
from agent_framework._types import AgentRunResponse
from rich.console import Group
from rich.json import JSON
from rich.markdown import Markdown
from rich.panel import Panel


def display_panel(title: str, content, border_style: str):
    """Print content inside a styled panel."""
    rich.print(
        Panel(
            content,
            title=title,
            border_style=border_style,
            padding=(1, 2),
        )
    )


def print_agent_response(response: AgentRunResponse, title: str = "Agent Framework AI Response"):
    """Display Azure AI response in a formatted panel."""

    # Process the response to extract grouped tools and assistant messages
    grouped_tools, assistant = _processed_messages(response)
    
    # Display the grouped tools if any exist
    if grouped_tools:
        display_panel(
            title="Tool Calls and Results",
            content=JSON(json.dumps(grouped_tools, indent=2)),
            border_style="medium_orchid",
        )

    stats = {
        "prompt tokens": response.usage_details.input_token_count,
        "completion tokens": response.usage_details.output_token_count,
        "total tokens": response.usage_details.total_token_count,
    }
    print_message(response.text, stats, title=title)


def _processed_messages(response: AgentRunResponse):
    """Process messages from an agent response to extract tool calls and assistant content.
    
    Args:
        response: AgentRunResponse object containing messages to process
        
    Note:
        This function groups tool function calls with their corresponding results
        by call_id and extracts assistant text messages.
    """
    # rich.print("response")
    # rich.print(response.to_json())

    grouped_tools = {}
    assistant = []

    for message in response.messages:
        if message.role.value == "assistant":
            for content in message.contents:
                if content.type == "text":
                    assistant.append(
                        {
                            "text": content.text,
                            "author": message.author_name,
                        }
                    )
                elif content.type == "function_call":
                    call_id = content.call_id
                    if call_id not in grouped_tools:
                        grouped_tools[call_id] = {}
                    grouped_tools[call_id]["function_call"] = {
                        "name": content.name,
                        "arguments": content.arguments,
                    }
        elif message.role.value == "tool":
            for content in message.contents:
                if content.type == "function_result":
                    call_id = content.call_id
                    if call_id not in grouped_tools:
                        grouped_tools[call_id] = {}
                    grouped_tools[call_id]["function_result"] = {
                        "result": content.result,
                    }
    
    return grouped_tools, assistant

def print_message(
    message: str,
    stats: dict = None,
    title: str = "Agent Message",
    style: str = "bold green",
):
    """Display message and stats in a formatted panel."""
    if stats is None:
        stats = {}

    output = Markdown(message)
    try:
        # Try to parse as JSON to check if printable as JSON
        output = JSON.from_data(json.loads(message))
    except Exception:
        pass

    response_group = Group(output, JSON.from_data(stats))
    display_panel(title, response_group, style)
