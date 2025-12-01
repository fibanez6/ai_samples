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
	@echo "20) structured output basic"
	@echo "21) structured output pydantic"
	@echo "22) structured output pydantic description"
	@echo "23) structured output pydantic enum"
	@echo "24) structured output pydantic function tool"
	@echo "25) structured output pydantic nested"
	@echo "30) rag basic"
	@echo "40) mcp basic - server stdio"
	@echo "41) mcp basic - server http"	
	@echo "42) mcp basic - server sse"
	@echo "43) mcp LangChain - client http"
	@echo "44) mcp LangChain - client sse"
	@echo "45) mcp inspector - stdio"
	@echo "46) mcp inspector - http"
	@echo "47) mcp inspector - sse"

	@read -p "Choose an option: " choice; \
	case $$choice in \
		0) make execute example="01_chat.chat_basic" ;; \
		1) make execute example="01_chat.chat_stream" ;; \
		2) make execute example="01_chat.chat_async" ;; \
		3) make execute example="01_chat.chat_history" ;; \
		4) make execute example="01_chat.chat_safety" ;; \
		10) make execute example="02_function_tools.tools_basic" ;; \
		11) make execute example="02_function_tools.tools_basic_extended" ;; \
		12) make execute example="02_function_tools.tools_stream" ;; \
		13) make execute example="02_function_tools.tools_multiple_parallel" ;; \
		20) make execute example="03_structured_outputs.structured_basic" ;; \
		21) make execute example="03_structured_outputs.structured_pydantic" ;; \
		22) make execute example="03_structured_outputs.structured_pydantic_description" ;; \
		23) make execute example="03_structured_outputs.structured_pydantic_enum" ;; \
		24) make execute example="03_structured_outputs.structured_pydantic_function_tool" ;; \
		25) make execute example="03_structured_outputs.structured_pydantic_nested" ;; \
		30) make execute example="05_rag.rag_basic" ;; \
		40) make execute example="06_mcp.mcp_basic_server_stdio" ;; \
		41) make execute example="06_mcp.mcp_basic_server_http" ;; \
		42) make execute example="06_mcp.mcp_basic_server_sse" ;; \
		43) make execute example="06_mcp.mcp_langchain_client_http" ;; \
		44) make execute example="06_mcp.mcp_langchain_client_sse" ;; \
		45) npx @modelcontextprotocol/inspector .venv/bin/python 06_mcp/mcp_basic_stdio.py ;; \
		46) npx @modelcontextprotocol/inspector  http://localhost:8000/mcp ;; \
		47) npx @modelcontextprotocol/inspector http://localhost:8000/sse ;; \
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
