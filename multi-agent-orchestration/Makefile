# Makefile for Multi-Agent Orchestration System
# Provides convenient shortcuts for UV commands

.PHONY: help install start demo health config format lint test clean

help: ## Show this help message
	@echo "🎭 Multi-Agent Orchestration System - Make Commands"
	@echo "=================================================="
	@echo ""
	@echo "Available commands:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "UV Commands (if you prefer UV directly):"
	@echo "  uv run python quick_start.py"
	@echo "  uv run uvicorn src.mcp_server.server:app --reload"
	@echo "  uv run python -m src.cli execute 'Your query here'"

install: ## Install dependencies with UV
	uv sync

start: ## Start MCP server with auto-reload
	uv run python -m uvicorn src.mcp_server.server:app --host 0.0.0.0 --port 8000 --reload

demo: ## Run quick demo
	uv run python quick_start.py

examples: ## Run example workflows
	uv run python -m src.cli examples

health: ## Check system health
	uv run python -m src.cli health

config: ## Create default configuration
	uv run python -m src.cli config --create

format: ## Format code with Black
	uv run black src/

lint: ## Lint code with Ruff
	uv run ruff check src/

test: ## Run tests
	uv run pytest

check: format lint test ## Format, lint, and test

execute: ## Execute a query (use: make execute QUERY="Your question here")
	@if [ -z "$(QUERY)" ]; then \
		echo "Usage: make execute QUERY=\"Your question here\""; \
		exit 1; \
	fi
	uv run python -m src.cli execute "$(QUERY)"

clean: ## Clean up cache and temporary files
	rm -rf .pytest_cache/
	rm -rf src/__pycache__/
	rm -rf src/*/__pycache__/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +

dev: ## Start development environment (server + demo)
	@echo "🚀 Starting development environment..."
	@echo "Press Ctrl+C to stop"
	@trap 'kill 0' SIGINT; \
	uv run python -m uvicorn src.mcp_server.server:app --host 0.0.0.0 --port 8000 --reload &\
	sleep 2 && \
	echo "🎭 MCP Server started on http://localhost:8000" && \
	echo "Run 'make demo' in another terminal to test the system" && \
	wait