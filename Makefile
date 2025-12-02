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
	@echo "100) chat - basic"
	@echo "101) chat - stream"
	@echo "102) chat - async"
	@echo "103) chat - history"
	@echo "104) chat - safety"
	@echo "200) tools - basic"
	@echo "201) tools - basic extended"
	@echo "202) tools - stream"
	@echo "203) tools - multiple parallel"
	@echo "300) structured output - basic"
	@echo "301) structured output - pydantic"
	@echo "302) structured output - pydantic description"
	@echo "303) structured output - pydantic enum"
	@echo "304) structured output - pydantic function tool"
	@echo "305) structured output - pydantic nested"
	@echo "400) rag - basic"
	@echo "500) mcp - basic - server stdio"
	@echo "501) mcp - basic - server http"	
	@echo "502) mcp - basic - server sse"
	@echo "503) mcp LangChain - client http"
	@echo "504) mcp LangChain - client sse"
	@echo "505) mcp LangChain - client github"
	@echo "506) mcp inspector - stdio"
	@echo "507) mcp inspector - http"
	@echo "508) mcp inspector - sse"
	@echo "700) microsoft agent framework - azure ai - basic"	

	@read -p "Choose an option: " choice; \
	case $$choice in \
		100) make execute example="01_chat.chat_basic" ;; \
		101) make execute example="01_chat.chat_stream" ;; \
		102) make execute example="01_chat.chat_async" ;; \
		103) make execute example="01_chat.chat_history" ;; \
		104) make execute example="01_chat.chat_safety" ;; \
		200) make execute example="02_function_tools.tools_basic" ;; \
		201) make execute example="02_function_tools.tools_basic_extended" ;; \
		202) make execute example="02_function_tools.tools_stream" ;; \
		203) make execute example="02_function_tools.tools_multiple_parallel" ;; \
		300) make execute example="03_structured_outputs.structured_basic" ;; \
		301) make execute example="03_structured_outputs.structured_pydantic" ;; \
		302) make execute example="03_structured_outputs.structured_pydantic_description" ;; \
		303) make execute example="03_structured_outputs.structured_pydantic_enum" ;; \
		304) make execute example="03_structured_outputs.structured_pydantic_function_tool" ;; \
		305) make execute example="03_structured_outputs.structured_pydantic_nested" ;; \
		400) make execute example="04_rag.rag_basic" ;; \
		500) make execute example="05_mcp.mcp_basic_server_stdio" ;; \
		501) make execute example="05_mcp.mcp_basic_server_http" ;; \
		502) make execute example="05_mcp.mcp_basic_server_sse" ;; \
		503) make execute example="05_mcp.mcp_langchain_client_http" ;; \
		504) make execute example="05_mcp.mcp_langchain_client_sse" ;; \
		505) make execute example="05_mcp.mcp_langchain_client_github" ;; \
		506) npx @modelcontextprotocol/inspector .venv/bin/python 05_mcp/mcp_basic_stdio.py ;; \
		507) npx @modelcontextprotocol/inspector  http://localhost:8000/mcp ;; \
		508) npx @modelcontextprotocol/inspector http://localhost:8000/sse ;; \
		700) make execute example="07_frameworks.microsoft_agent_framework.azure_ai.agent_framework_basic" ;; \
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
