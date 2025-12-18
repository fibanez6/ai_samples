# Makefile for Multi-Agent Orchestration System
# Provides convenient shortcuts for UV commands

.PHONY: help install start demo health config format lint test clean

help: ## Show this help message
	@echo "🎭 Multi-Agent Orchestration System - Make Commands"
	@echo "=================================================="
	@echo ""
	@echo "Available commands:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)


select:
	@echo "Select example:"
	@echo "1) openai samples"
	@echo "2) microsoft agent framework samples"

	@read -p "Choose an option: " choice; \
	case $$choice in \
		1) make select_openai;; \
		2) make select_maf;; \
	esac

select_openai: ## Select and run an OpenAI example
	@echo "Select OpenAI example:"
	@echo "Select example:"
	@echo "100) openai - chat - basic"
	@echo "101) openAi - chat - stream"
	@echo "102) openAi - chat - async"
	@echo "103) openAi - chat - history"
	@echo "104) openAi - chat - safety"
	@echo "110) openAi - tools - basic"
	@echo "111) openAi - tools - basic extended"
	@echo "112) openAi - tools - stream"
	@echo "113) openAi - tools - multiple parallel"
	@echo "120) openAi - structured output - basic"
	@echo "121) openAi - structured output - pydantic"
	@echo "122) openAi - structured output - pydantic description"
	@echo "123) openAi - structured output - pydantic enum"
	@echo "124) openAi - structured output - pydantic function tool"
	@echo "125) openAi - structured output - pydantic nested"
	@echo "130) openAi - rag - basic"
	@echo "140) openAi - mcp - basic - server stdio"
	@echo "141) openAi - mcp - basic - server sse"
	@echo "142) openAi - mcp - basic - server http"	
	@echo "143) openAi - mcp - LangChain - client http"
	@echo "144) openAi - mcp - LangChain - client sse"
	@echo "145) openAi - mcp - LangChain - client github"
	@echo "146) openAi - mcp - inspector - stdio"
	@echo "147) openAi - mcp - inspector - sse"
	@echo "148) openAi - mcp - inspector - http"
	@echo "150) openAi - middleware - mcp - opentelemetry"	

	@read -p "Choose an option: " choice; \
	case $$choice in \
		100) make execute example="agents.openai.01_chat.chat_basic" ;; \
		101) make execute example="agents.openai.01_chat.chat_stream" ;; \
		102) make execute example="agents.openai.01_chat.chat_async" ;; \
		103) make execute example="agents.openai.01_chat.chat_history" ;; \
		104) make execute example="agents.openai.01_chat.chat_safety" ;; \
		110) make execute example="agents.openai.02_function_tools.tools_basic" ;; \
		111) make execute example="agents.openai.02_function_tools.tools_basic_extended" ;; \
		112) make execute example="agents.openai.02_function_tools.tools_stream" ;; \
		113) make execute example="agents.openai.02_function_tools.tools_multiple_parallel" ;; \
		120) make execute example="agents.openai.03_structured_outputs.structured_basic" ;; \
		121) make execute example="agents.openai.03_structured_outputs.structured_pydantic" ;; \
		122) make execute example="agents.openai.03_structured_outputs.structured_pydantic_description" ;; \
		123) make execute example="agents.openai.03_structured_outputs.structured_pydantic_enum" ;; \
		124) make execute example="agents.openai.03_structured_outputs.structured_pydantic_function_tool" ;; \
		125) make execute example="agents.openai.03_structured_outputs.structured_pydantic_nested" ;; \
		130) make execute example="agents.openai.04_rag.rag_basic" ;; \
		140) make execute example="agents.openai.05_mcp.mcp_basic_server_stdio" ;; \
		141) make execute example="agents.openai.05_mcp.mcp_basic_server_sse" ;; \
		142) make execute example="agents.openai.05_mcp.mcp_basic_server_http" ;; \
		143) make execute example="agents.openai.05_mcp.mcp_langchain_client_http" ;; \
		144) make execute example="agents.openai.05_mcp.mcp_langchain_client_sse" ;; \
		145) make execute example="agents.openai.05_mcp.mcp_langchain_client_github" ;; \
		146) npx @modelcontextprotocol/inspector .venv/bin/python 05_mcp/mcp_basic_stdio.py ;; \
		147) npx @modelcontextprotocol/inspector http://localhost:8000/sse ;; \
		148) npx @modelcontextprotocol/inspector  http://localhost:8000/mcp ;; \
		150) make execute example="agents.openai.06_middleware.middleware_mcp_opentelemetry" ;; \
	esac

select_maf:
	@echo "microsoft agent framework example:"
	@echo "100) microsoft agent framework - azure ai - chat - basic"	
	@echo "101) microsoft agent framework - azure ai - chat - basic stream"
	@echo "102) microsoft agent framework - azure ai - chat - structured output"
	@echo "103) microsoft agent framework - azure ai - chat - images_uri"
	@echo "104) microsoft agent framework - azure ai - chat - images_uri_local"
	@echo "105) microsoft agent framework - azure ai - chat - function tools"
	@echo "106) microsoft agent framework - azure ai - chat - function tools human approval"
	@echo "200) microsoft agent framework - azure ai - agent - basic"	
	@echo "201) microsoft agent framework - azure ai - agent - basic stream"
	@echo "202) microsoft agent framework - azure ai - agent - structured output"
	@echo "203) microsoft agent framework - azure ai - agent - function tools"

	@read -p "Choose an option: " choice; \
	case $$choice in \
		100) make execute example="agents.microsoft_agent_framework.azure_ai.agent_framework_basic" ;; \
		101) make execute example="agents.microsoft_agent_framework.azure_ai.agent_framework_basic_stream" ;; \
		102) make execute example="agents.microsoft_agent_framework.azure_ai.agent_framework_structured_output" ;; \
		103) make execute example="agents.microsoft_agent_framework.azure_ai.agent_framework_images_uri" ;; \
		104) make execute example="agents.microsoft_agent_framework.azure_ai.agent_framework_images_uri_local" ;; \
		105) make execute example="agents.microsoft_agent_framework.azure_ai.agent_framework_function_tools" ;; \
		106) make execute example="agents.microsoft_agent_framework.azure_ai.agent_framework_function_tools_human_approvals" ;; \
		200) make execute example="agents.microsoft_agent_framework.azure_ai_agent.agent_framework_basic" ;; \
		201) make execute example="agents.microsoft_agent_framework.azure_ai_agent.agent_framework_basic_stream" ;; \
		202) make execute example="agents.microsoft_agent_framework.azure_ai_agent.agent_framework_structured_output" ;; \
		203) make execute example="agents.microsoft_agent_framework.azure_ai_agent.agent_framework_function_tools" ;; \
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
