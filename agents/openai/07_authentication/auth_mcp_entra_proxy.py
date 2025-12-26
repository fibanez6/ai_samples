"""
Expense tracking MCP server with authentication.

Azure (Microsoft Entra ID) OAuth 🤝 FastMCP: https://gofastmcp.com/integrations/azure
"""

import csv
import logging
import os
from datetime import date
from enum import Enum
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv
from fastmcp import Context, FastMCP
from fastmcp.server.auth.providers.azure import AzureProvider
from fastmcp.server.dependencies import get_access_token
from fastmcp.server.middleware import Middleware, MiddlewareContext
from key_value.aio.stores.memory import MemoryStore
from rich.console import Console
from rich.logging import RichHandler
from starlette.responses import JSONResponse

# Load environment variables from .env file
load_dotenv(override=True)

logging.basicConfig(
    level=logging.WARNING,
    format="%(message)s",
    handlers=[
        RichHandler(
            console=Console(stderr=True),
            show_path=False,
            show_level=False,
            rich_tracebacks=True,
        )
    ],
)
logger = logging.getLogger("Expenses Auth MCP")
logger.setLevel(logging.INFO)

# Define constants
SCRIPT_DIR = Path(__file__).parent
EXPENSES_FILE = SCRIPT_DIR / "expenses.csv"

# Configure authentication provider
# Azure/Entra ID authentication using AzureProvider and Entra Proxy
oauth_client_store = MemoryStore()
entra_base_url = "http://localhost:8000"
auth = AzureProvider(
    client_id=os.environ["ENTRA_PROXY_AZURE_CLIENT_ID"],
    client_secret=os.environ["ENTRA_PROXY_AZURE_CLIENT_SECRET"],
    tenant_id=os.environ["AZURE_TENANT_ID"],
    base_url=entra_base_url,
    required_scopes=["mcp-access"],
    client_storage=oauth_client_store,
)

logger.info("Using Entra OAuth Proxy for server %s and %s storage and client_id", entra_base_url, type(oauth_client_store).__name__)

# Middleware to populate user_id in per-request context state
class UserAuthMiddleware(Middleware):
    def _get_user_id(self):
        token = get_access_token()
        if not (token and hasattr(token, "claims")):
            return None
        # Return 'oid' claim if present (for Entra), otherwise fallback to 'sub' (for KeyCloak)
        return token.claims.get("oid", token.claims.get("sub"))

    async def on_call_tool(self, context: MiddlewareContext, call_next):
        user_id = self._get_user_id()
        if context.fastmcp_context is not None:
            context.fastmcp_context.set_state("user_id", user_id)
        return await call_next(context)

    async def on_read_resource(self, context: MiddlewareContext, call_next):
        user_id = self._get_user_id()
        if context.fastmcp_context is not None:
            context.fastmcp_context.set_state("user_id", user_id)
        return await call_next(context)

# Create the MCP server
mcp = FastMCP("Expenses Tracker", auth=auth, middleware=[UserAuthMiddleware()])

"""Expense tracking MCP server with authentication and Cosmos DB storage."""

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
async def add_user_expense(
    date: Annotated[date, "Date of the expense in YYYY-MM-DD format"],
    amount: Annotated[float, "Positive numeric amount of the expense"],
    category: Annotated[Category, "Category label"],
    description: Annotated[str, "Human-readable description of the expense"],
    payment_method: Annotated[PaymentMethod, "Payment method used"],
    ctx: Context,
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
                writer.writerow(["date", "amount", "category", "description", "payment_method", "user_id"])

            writer.writerow([date_iso, amount, category.value, description, payment_method.value, ctx.get_state("user_id")])

        return f"User {ctx.get_state('user_id')} successfully added expense: ${amount} for {description} on {date_iso}"

    except Exception as e:
        logger.error(f"Error adding expense: {str(e)}")
        return "Error: Unable to add expense"
    

@mcp.tool
async def get_expenses(ctx: Context):
    """Get the authenticated user's expense data from Cosmos DB."""

    try:
        with open(EXPENSES_FILE, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            expenses_data = list(reader)

        csv_content = f"Expense data ({len(expenses_data)} entries):\n\n"
        for expense in expenses_data:
            if expense["user_id"] != ctx.get_state("user_id"):
                continue
            csv_content += (
                f"date: {expense['date']}, "
                f"amount: ${expense['amount']}, "
                f"category: {expense['category']}, "
                f"description: {expense['description']}, "
                f"payment_method: {expense['payment_method']},"
                f"user_id: {expense['user_id']}\n"
            )
        return csv_content

    except FileNotFoundError:
        logger.error("Expenses file not found")
        return "Error: Expense data unavailable"
    except Exception as e:
        logger.error(f"Error reading expenses: {str(e)}")
        return "Error: Unable to retrieve expense data"


@mcp.custom_route("/health", methods=["GET"])
async def health_check(_request):
    """Health check endpoint for service availability."""
    return JSONResponse({"status": "healthy", "service": "mcp-server"})


if __name__ == "__main__":
    logger.info("Auth MCP Expenses server starting (HTTP mode on port 8000)")

    # Run with HTTP transport
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        show_banner=os.getenv("SHOW_BANNER", "true").lower() == "true",
    )