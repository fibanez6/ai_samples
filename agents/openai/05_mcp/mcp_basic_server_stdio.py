"""
Basic example of FastMCP with STDIO transport for tracking and analyzing expenses.

This module implements a Model Context Protocol (MCP) server for tracking and analyzing expenses.
It provides tools, prompts, and resources for managing expenses stored in a CSV file.

The server exposes three main capabilities:
1. A tool to add new expenses with validation
2. A prompt to analyze spending patterns with filters
3. A resource to list all recorded expenses

The expenses are stored in a CSV file (expenses.csv) with the following columns:
- date: ISO format date (YYYY-MM-DD)
- amount: Positive numeric value
- category: One of the predefined expense categories
- description: Human-readable description
- payment_method: Payment method used (AMEX, VISA, or CASH)

Usage:
    Start the server using STDIO transport:
    $ uv run python -m 06_mcp.mcp_basic_stdio
    
    Or use the FastMCP Inspector for debugging:
    $ npx @modelcontextprotocol/inspector .venv/bin/python 06_mcp/mcp_basic_stdio.py

Attributes:
    SCRIPT_DIR (Path): Directory containing this script
    EXPENSES_FILE (Path): Path to the expenses CSV file
    mcp (FastMCP): The FastMCP server instance

Note:
    @mcp.tool decorator: Registers a function as an MCP tool that can be invoked by AI models
    or clients. Tools are actions that the AI can execute to perform specific tasks, such as
    adding expenses, querying data, or performing calculations. The decorated function becomes
    callable through the MCP protocol with automatic parameter validation and serialization.

        - To run it, start the server from command line or mcp.json, then in the chat panel,
        the AI will automatically invoke the tool when appropriate based on your conversation.
        You can explicitly request it by asking: "Add an expense for $50 for groceries today
        paid with VISA in the food category."
 
    @mcp.prompt decorator: Defines a prompt that the AI model can use to generate responses
    based on user input. Prompts are templates or functions that guide the AI in generating
    text outputs. The decorated function can include parameters that the AI can fill in,
    allowing for dynamic and context-aware responses.

        - To run it, type '/' to open the command palette, then select
        '/mcp.basic-mcp-expenses.analyze_spending_prompt' and insert any desired parameters.

    @mcp.resource decorator: Registers a function as an MCP resource that can be accessed
    by AI models or clients. Resources are data providers that supply information or content
    to the AI. The decorated function can return data in various formats, such as text, JSON,
    or binary, making it accessible through the MCP protocol.


Example from https://github.com/Azure-Samples/python-mcp-demos
"""
import csv
import logging
from datetime import date
from enum import Enum
from pathlib import Path
from typing import Annotated

from fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger("ExpensesMCP")

# Define the MCP server
mcp = FastMCP("Expenses Tracker")

# Define constants
SCRIPT_DIR = Path(__file__).parent
EXPENSES_FILE = SCRIPT_DIR / "expenses.csv"

# Ensure the expenses file exists
if not EXPENSES_FILE.exists():
    EXPENSES_FILE.write_text("item,date,amount\n")

class PaymentMethod(Enum):
    AMEX = "amex"
    VISA = "visa"
    CASH = "cash"


class Category(Enum):
    FOOD = "food"
    TRANSPORT = "transport"
    ENTERTAINMENT = "entertainment"
    SHOPPING = "shopping"
    GADGET = "gadget"
    OTHER = "other"

@mcp.tool
async def add_expense(
    date: Annotated[date, "Date of the expense in YYYY-MM-DD format"],
    amount: Annotated[float, "Positive numeric amount of the expense"],
    category: Annotated[Category, "Category label"],
    description: Annotated[str, "Human-readable description of the expense"],
    payment_method: Annotated[PaymentMethod, "Payment method used"],
):
    """Add a new expense to the expenses.csv file."""
    if amount <= 0:
        return "Error: Amount must be positive"

    date_iso = date.isoformat()
    logger.info(f"Adding expense: ${amount} for {description} on {date_iso}")

    try:
        file_exists = EXPENSES_FILE.exists()

        with open(EXPENSES_FILE, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(["date", "amount", "category", "description", "payment_method"])

            writer.writerow([date_iso, amount, category.value, description, payment_method.value])

        return f"Successfully added expense: ${amount} for {description} on {date_iso}"

    except Exception as e:
        logger.error(f"Error adding expense: {str(e)}")
        return "Error: Unable to add expense"

@mcp.resource("resource://expenses")
async def get_expenses_data():
    """Get raw expense data from CSV file"""
    logger.info("Expenses data accessed")

    try:
        with open(EXPENSES_FILE, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            expenses_data = list(reader)

        csv_content = f"Expense data ({len(expenses_data)} entries):\n\n"
        for expense in expenses_data:
            csv_content += (
                f"Date: {expense['date']}, "
                f"Amount: ${expense['amount']}, "
                f"Category: {expense['category']}, "
                f"Description: {expense['description']}, "
                f"Payment: {expense['payment_method']}\n"
            )

        return csv_content

    except FileNotFoundError:
        logger.error("Expenses file not found")
        return "Error: Expense data unavailable"
    except Exception as e:
        logger.error(f"Error reading expenses: {str(e)}")
        return "Error: Unable to retrieve expense data"

@mcp.prompt
def analyze_spending_prompt(
    category: str | None = None, start_date: str | None = None, end_date: str | None = None
) -> str:
    """Generate a prompt to analyze spending patterns with optional filters."""

    filters = []
    if category:
        filters.append(f"Category: {category}")
    if start_date:
        filters.append(f"From: {start_date}")
    if end_date:
        filters.append(f"To: {end_date}")

    filter_text = f" ({', '.join(filters)})" if filters else ""

    return f"""
    Please analyze my spending patterns{filter_text} and provide:

    1. Total spending breakdown by category
    2. Average daily/weekly spending
    3. Most expensive single transaction
    4. Payment method distribution
    5. Spending trends or unusual patterns
    6. Recommendations for budget optimization

    Use the expense data to generate actionable insights.
    """


if __name__ == "__main__":
    logger.info("MCP Expenses server starting")
    mcp.run(transport="stdio", show_banner=False)
