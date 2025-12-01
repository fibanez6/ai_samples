"""
Basic example of FastMCP with http transport

This example demonstrates a basic implementation of a FastMCP server using HTTP as the transport layer.
It defines a simple service for an "Expenses Tracker" that can be extended with various operations.

To run this example:
1. Start the server: `uv run python -m 06_mcp.mcp_basic_http`
2. In a separate terminal, start the FastMCP Inspector: `npx @modelcontextprotocol/inspector http://localhost:8000/mcp`
"""

from datetime import date
from pathlib import Path
from typing import Annotated

from fastmcp import FastMCP

# Define the MCP server
mcp = FastMCP("Expenses Tracker")

# Define constants
SCRIPT_DIR = Path(__file__).parent
EXPENSES_FILE = SCRIPT_DIR / "expenses.csv"

# Ensure the expenses file exists
if not EXPENSES_FILE.exists():
    EXPENSES_FILE.write_text("item,date,amount\n")


@mcp.tool()
def add_expense(
    item: Annotated[str, "Description of the expense"],
    date: Annotated[date, "Date of the expense in YYYY-MM-DD format"],
    amount: Annotated[float, "Positive numeric amount of the expense"],
) -> str:
    """Add an expense to the tracker"""
    with open(EXPENSES_FILE, "a") as f:
        f.write(f"{item},{date},{amount}\n")
    return f"Added expense: {item} for ${amount}"


@mcp.prompt()
def analyze_spending(
    min_amount: Annotated[float, "Minimum amount to consider in the analysis"],
    item_filter: Annotated[str, "Optional filter for item description"],
) -> str:
    """Analyze spending patterns with optional filters"""
    if not EXPENSES_FILE.exists():
        return "No expenses recorded."

    expenses = []
    # Read lines and skip header
    lines = EXPENSES_FILE.read_text().strip().split("\n")
    if len(lines) > 1:
        for line in lines[1:]:
            if not line:
                continue
            try:
                item, date, amount = line.split(",")
                amount = float(amount)

                if amount >= min_amount and (
                    not item_filter or item_filter.lower() in item.lower()
                ):
                    expenses.append(f"- {item}: ${amount}")
            except ValueError:
                continue

    if not expenses:
        return "No expenses found matching the criteria."

    return (
        f"Please analyze the following expenses and identify any patterns or anomalies:\n\n"
        + "\n".join(expenses)
    )


@mcp.resource("expenses://list")
def list_expenses() -> str:
    """List all expenses"""
    return EXPENSES_FILE.read_text()


if __name__ == "__main__":
    # Run with SSE transport
    mcp.run(transport="http", host="0.0.0.0", port=8000)
