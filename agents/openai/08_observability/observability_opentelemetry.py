"""
FastMCP server with OpenTelemetry middleware integration

This example demonstrates a FastMCP server using HTTP transport with OpenTelemetry
middleware for observability. The server implements an "Expenses Tracker" service
that allows adding expenses, retrieving expense data, and analyzing spending patterns.

Features:
- OpenTelemetry instrumentation with OTLP exporter
- Aspire Dashboard integration for telemetry visualization
- CSV-based expense storage
- Tools for adding expenses
- Resources for retrieving expense data
- Prompts for spending analysis

Pre-requirements:
1. Aspire Dashboard running locally (or OTLP endpoint configured)
   You can run Aspire Dashboard using Docker:
    `docker run --rm -d -p 18888:18888 -p 4317:18889 --name aspire-dashboard mcr.microsoft.com/dotnet/aspire-dashboard:latest`
2. Get the dashboard URL and login token from the container logs:
    `docker logs aspire-dashboard 2>&1 | grep "Login to the dashboard"`

To run this example:
1. (Optional) Set OTEL_EXPORTER_OTLP_ENDPOINT environment variable to enable telemetry
2. Start the server: `uv run python -m 06_middleware.middleware_mcp_opentelemetry`
3. In a separate terminal, start the FastMCP Inspector: `npx @modelcontextprotocol/inspector http://localhost:8000/mcp`

Example adapted from https://github.com/Azure-Samples/python-mcp-demos
"""
import csv
import logging
import os
from datetime import date
from enum import Enum
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.server.middleware import Middleware

from .opentelemetry_middleware import (
    OpenTelemetryMiddleware,
    configure_aspire_dashboard,
)

load_dotenv(override=True)

# Configure logging
logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(message)s")
logger = logging.getLogger("ExpensesMCP")
logger.setLevel(logging.INFO)

# OpenTelemetry setup
middleware: list[Middleware] = []
if os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT"):
    logger.info("Setting up Aspire Dashboard instrumentation (OTLP)")
    configure_aspire_dashboard(service_name="expenses-mcp")
    middleware = [OpenTelemetryMiddleware(tracer_name="expenses.mcp")]

# Define the MCP server
mcp = FastMCP("Expenses Tracker", middleware=middleware) # <---- Here

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
    logger.info("MCP Expenses server starting (HTTP mode on port 8000)")

    # Run with HTTP transport
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        show_banner=os.getenv("SHOW_BANNER", "true").lower() == "true",
    )
