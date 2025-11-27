"""
Basic example of FastMCP with STDIO transport
"""
from pathlib import Path
from fastmcp import FastMCP

# Define the MCP server
mcp = FastMCP("Expenses Tracker")

# Define constants
SCRIPT_DIR = Path(__file__).parent
EXPENSES_FILE = SCRIPT_DIR / "expenses.csv"

# Ensure the expenses file exists
if not EXPENSES_FILE.exists():
    EXPENSES_FILE.write_text("item,amount\n")

@mcp.tool()
def add_expense(item: str, amount: float) -> str:
    """Add an expense to the tracker"""
    with open(EXPENSES_FILE, "a") as f:
        f.write(f"{item},{amount}\n")
    return f"Added expense: {item} for ${amount}"

@mcp.prompt()
def analyze_spending(min_amount: float = 0.0, item_filter: str = "") -> str:
    """Analyze spending patterns with optional filters"""
    if not EXPENSES_FILE.exists():
        return "No expenses recorded."
    
    expenses = []
    # Read lines and skip header
    lines = EXPENSES_FILE.read_text().strip().split('\n')
    if len(lines) > 1:
        for line in lines[1:]:
            if not line: continue
            try:
                item, amount = line.split(',')
                amount = float(amount)
                
                if amount >= min_amount and (not item_filter or item_filter.lower() in item.lower()):
                    expenses.append(f"- {item}: ${amount}")
            except ValueError:
                continue
            
    if not expenses:
        return "No expenses found matching the criteria."
        
    return f"Please analyze the following expenses and identify any patterns or anomalies:\n\n" + "\n".join(expenses)

@mcp.resource("expenses://list")
def list_expenses() -> str:
    """List all expenses"""
    return EXPENSES_FILE.read_text()

if __name__ == "__main__":
    mcp.run(transport='stdio')