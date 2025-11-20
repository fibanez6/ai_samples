from time import sleep
from rich import print
from rich.markdown import Markdown
from rich.panel import Panel
from rich.console import Group
from rich.json import JSON

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
    success = not getattr(message, "refusal", False)
    usage = response.usage
    stats = {
        "prompt tokens": usage.prompt_tokens,
        "completion tokens": usage.completion_tokens,
        "total tokens": usage.total_tokens
    }

    response_content = message.content if success else getattr(message, "refusal", "")
    response_group = Group(
        Markdown(response_content),
        JSON.from_data(stats)
    )

    display_panel(
        title,
        response_group,
        "bold green" if success else "bold red"
    )
