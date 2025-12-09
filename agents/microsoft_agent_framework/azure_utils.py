import json
from typing import Any

import rich
from agent_framework import Role
from agent_framework._types import AgentRunResponse, AgentRunResponseUpdate, ChatMessage
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

# ==========================
# Process request
# ==========================

def _process_request(message: ChatMessage | str) -> dict:
    rich.print("message")
    rich.print(message.to_json() if isinstance(message, ChatMessage) else message)

    processed_messages = {}
    if isinstance(message, ChatMessage):
        # Initialize the role key as a dictionary
        processed_messages[message.role.value] = {}
        for content in message.contents:
            if content.type == "text":
                processed_messages[message.role.value]["text"] = content.text
            elif content.type == "function_call":
                 processed_messages[message.role.value]["function_call"] = {
                        "call_id": content.call_id,
                        "name": content.name,
                        "arguments": content.arguments,
                    }
            elif content.type == "function_result":
                 processed_messages[message.role.value]["function_result"] = {
                        "call_id": content.call_id,
                        "result": content.result,
                    }
            elif content.type == "function_approval_request":
                 processed_messages[message.role.value]["approval_request"] = {
                    "function_call": {
                        "call_id": content.function_call.call_id,
                        "name": content.function_call.name,
                        "arguments": content.function_call.arguments,
                    }
                }
            elif content.type == "function_approval_response":
                processed_messages[message.role.value]["approval_response"] = {
                    "approved": content.approved,
                    "function_call": {
                        "call_id": content.function_call.call_id,
                        "name": content.function_call.name,
                        "arguments": content.function_call.arguments,
                    }
                }
            elif hasattr(content, content.type):
                processed_messages[message.role.value][content.type] = getattr(content, content.type)
            
    else:
        processed_messages[Role.USER.value] = message
    return processed_messages

def print_request(
    message: ChatMessage | list[Any] | str,
    title: str = "Agent Request Messages" ):
    """Display agent messages in a formatted panel."""
    # Process the message to extract grouped tools and assistant messages
    messages_to_process = message if isinstance(message, list) else [message]
    processed_messages = [_process_request(msg) for msg in messages_to_process]

    display_panel(title, JSON.from_data(processed_messages), "bold blue")

# ==========================
# Process response
# ==========================

def _process_response(response: AgentRunResponse):
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

    messages = response.messages if response else []

    for message in messages:
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
                elif content.type == "function_approval_request":
                    id = content.id
                    if id not in grouped_tools:
                        grouped_tools[id] = {}
                    grouped_tools[id]["function_approval_request"] = {
                        "name": content.function_call.name,
                        "arguments": content.function_call.arguments,
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
    
    return {
        "assistant": assistant,
        "grouped_tools": grouped_tools
    }


def print_response(response: AgentRunResponse | AgentRunResponseUpdate, title: str = "Agent Framework AI Response"):
    """Display Azure AI response in a formatted panel."""
    rich.print("response")
    rich.print(type(response))

    if not response:
        rich.print("No response")
        return

    # Process the response to extract grouped tools and assistant messages
    processed_messages = _process_response(response)
    
    # Display the grouped tools if any exist
    if processed_messages["grouped_tools"]:
        display_panel(
            title="Tool Calls",
            content=JSON(json.dumps(processed_messages, indent=2)),
            border_style="medium_orchid",
        )

    stats = {}
    if response.usage_details:
        stats = {
            "prompt tokens": response.usage_details.input_token_count,
            "completion tokens": response.usage_details.output_token_count,
            "total tokens": response.usage_details.total_token_count,
        }
    
    if response.text:
        print_message(response.text, stats, title=title)

def print_message(
    message: str,
    stats: dict = None,
    title: str = "Agent Message",
    style: str = "bold green"):
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
