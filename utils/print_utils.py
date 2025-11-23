from rich import print
from rich.console import Group
from rich.json import JSON
from rich.markdown import Markdown
from rich.panel import Panel


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
    else:
        print_message(message.content, stats, title=title)

def print_message_tools(message, stats: dict, title: str = "Agent Tool Message"):
    """Display tool call messages in a formatted panel."""

    tool_responses = "\n\n".join(
        f"**Tool Id:** {tool.id}\n\n**Tool Used:** {tool.function.name}\n\n**Tool Args:**\n```\n{tool.function.arguments}\n```"
        for tool in message.tool_calls
    )
    # full_message = f"{tool_responses}\n\n**Response:**\n\n{message.content}"
    print_message(tool_responses, stats, title=title)

def print_message(message: str, stats: dict, title: str = "Agent Message", style: str = "bold green"):
    """Display message and stats in a formatted panel."""

    response_group = Group(
        Markdown(message),
        JSON.from_data(stats)
    )
    display_panel(
        title,
        response_group,
        style
    )
