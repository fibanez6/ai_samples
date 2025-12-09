#!/usr/bin/env python3
"""
Main entry point for Multi-Agent Orchestration System.
This script showcases the available UV commands and provides easy access to system functionality.
"""

import os
import sys
from pathlib import Path


def show_available_commands():
    """Display available UV commands."""
    print("🎭 Multi-Agent Orchestration System")
    print("=" * 50)
    print()
    print("🚀 Available UV Commands:")
    print()
    
    commands = [
        ("uv run uvicorn src.mcp_server.server:app --reload", "Start MCP server with auto-reload"),
        ("uv run python quick_start.py", "Run quick demo"),
        ("uv run python -m src.cli examples", "Run example workflows"),
        ("uv run python -m src.cli health", "Check system health"),
        ("uv run python -m src.cli execute 'query'", "Execute custom research query"),
        ("uv run python -m src.cli config --create", "Create default configuration"),
        ("uv run pytest", "Run test suite"),
        ("uv run black src/", "Format code with Black"),
        ("uv run ruff check src/", "Lint code with Ruff"),
    ]
    
    for cmd, description in commands:
        print(f"  {cmd:<30} # {description}")
    
    print()
    print("📝 Getting Started:")
    print("  1. Copy .env.example to .env and add your OpenAI API key")
    print("  2. Run: uv run python quick_start.py")
    print("  3. Start MCP server: uv run uvicorn src.mcp_server.server:app --reload")
    print("  4. Execute queries: uv run python -m src.cli execute 'Your question here'")
    print()
    
    # Check if .env exists
    if not Path(".env").exists():
        print("⚠️  No .env file found. Create one with:")
        print("     cp .env.example .env")
        print("     # Then edit .env to add your OPENAI_API_KEY")
        print()
    
    # Check if OpenAI API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  OPENAI_API_KEY not found in environment")
        print("     Add it to your .env file or set it as an environment variable")
        print()

def main():
    """Main entry point."""
    if len(sys.argv) > 1 and sys.argv[1] == "--commands":
        show_available_commands()
        return
    
    print("🎭 Multi-Agent Orchestration System")
    print("=" * 40)
    print()
    print("This is a modern multi-agent system for research, analysis, and action planning.")
    print()
    print("📚 Quick Commands:")
    print("  python main.py --commands                      # Show all available UV commands")
    print("  uv run python quick_start.py                   # Run quick demo")
    print("  uv run uvicorn src.mcp_server.server:app --reload  # Start MCP server")
    print()
    print("📖 For full documentation, see README.md")
    print("🚀 For examples, run: uv run demo")

if __name__ == "__main__":
    main()
