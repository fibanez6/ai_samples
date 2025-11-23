# Makefile for Multi-Agent Orchestration System
# Provides convenient shortcuts for UV commands

.PHONY: help install start demo health config format lint test clean

help: ## Show this help message
	@echo "🎭 Multi-Agent Orchestration System - Make Commands"
	@echo "=================================================="
	@echo ""
	@echo "Available commands:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

select: ## Select and run an example
	@echo "Select example:"
	@echo "0) chat basic"
	@echo "1) chat stream"
	@echo "2) chat async"
	@echo "3) chat history"
	@echo "4) chat safety"
	@echo "10) tools basic"
	@echo "11) tools basic extended"
	@echo "12) tools stream"
	@echo "13) tools multiple parallel"
	@read -p "Choose an option: " choice; \
	case $$choice in \
		0) make execute example="01_chat.chat_basic" ;; \
		1) make execute example="01_chat.chat_stream" ;; \
		2) make execute example="01_chat.chat_async" ;; \
		3) make execute example="01_chat.chat_history" ;; \
		4) make execute example="01_chat.chat_safety" ;; \
		10) make execute example="02_tools.tools_basic" ;; \
		11) make execute example="02_tools.tools_basic_extended" ;; \
		12) make execute example="02_tools.tools_stream" ;; \
		13) make execute example="02_tools.tools_multiple_parallel" ;; \
	esac

install: ## Install dependencies with UV
	uv sync


execute: ## Execute a query (use: make execute example="python filepath")
	@if [ -z "$(example)" ]; then \
		echo "Usage: make execute example=\"01_chat.chat_basic\""; \
		exit 1; \
	fi
	uv run python -m "$(example)"

clean: ## Clean up cache and temporary files
	rm -rf .pytest_cache/
	rm -rf src/__pycache__/
	rm -rf src/*/__pycache__/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +
