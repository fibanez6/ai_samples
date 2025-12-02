import json

from rich import print
from rich.console import Group
from rich.json import JSON
from rich.markdown import Markdown
from rich.panel import Panel
from agent_framework._types import AgentRunResponse

def display_panel(title: str, content, border_style: str):
    """Print content inside a styled panel."""
    print(
        Panel(
            content,
            title=title,
            border_style=border_style,
            padding=(1, 2),
        )
    )

def print_agent_messages(messages: list, title: str = "Agent Messages"):
    """Display agent messages in a formatted panel."""
    display_panel(
        title,
        JSON.from_data(messages),
        "bold blue"
    )


def print_agent_response(response, title: str = "Agent Response"):
    """Display agent response in a formatted panel."""

    if isinstance(response, AgentRunResponse): 
        # Azure AI response
        _print_azure_response(response, title=title)
    else: 
        # OpenAI response
        _print_openai_response(response, title=title)


def _print_openai_response(response, title: str = "OpenAI Response"):
    """Display OpenAI response in a formatted panel."""
    message = response.choices[0].message
    usage = response.usage
    stats = {
        "prompt tokens": usage.prompt_tokens,
        "completion tokens": usage.completion_tokens,
        "total tokens": usage.total_tokens
    }

    if getattr(message, "refusal", False):
        print_message(message.refusal, stats, title="Agent Refusal", style="bold red")
    elif getattr(message, "tool_calls", None):
        print_message_tools(message, stats, title=title)
    elif getattr(message, "parsed", None):
        parse = message.parsed.model_dump_json(indent=2)
        print_message(parse, stats, title=title)
    else:
        print_message(message.content, stats, title=title)

def _print_azure_response(response, title: str = "Agent Framework AI Response"):
    """Display Azure AI response in a formatted panel."""
    stats = {}
    print_message(response.text, stats, title=title)

def print_message_tools(message, stats: dict, title: str = "Agent Tool Message"):
    """Display tool call messages in a formatted panel."""

    tool_responses = "\n\n".join(
        f"**Tool Id:** {tool.id}\n\n**Tool Used:** {tool.function.name}\n\n**Tool Args:**\n```\n{tool.function.arguments}\n```"
        for tool in message.tool_calls
    )
    # full_message = f"{tool_responses}\n\n**Response:**\n\n{message.content}"
    print_message(tool_responses, stats, title=title)

def print_message(message: str, stats: dict = {}, title: str = "Agent Message", style: str = "bold green"):
    """Display message and stats in a formatted panel."""

    output = Markdown(message)
    try:
        # Try to parse as JSON to check if printable as JSON
        output = JSON.from_data(json.loads(message))
    except Exception:
        pass

    response_group = Group(
        output,
        JSON.from_data(stats)
    )
    display_panel(
        title,
        response_group,
        style
    )
