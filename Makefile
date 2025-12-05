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
	@echo "700) microsoft agent framework - azure ai - chat - basic message"	
	@echo "701) microsoft agent framework - azure ai - chat - basic message stream"
# 	@echo "702) microsoft agent framework - azure ai - chat - structured output"
# 	@echo "703) microsoft agent framework - azure ai - chat - function tools"
# 	@echo "704) microsoft agent framework - azure ai - chat - function tools human approval"
# 	@echo "705) microsoft agent framework - azure ai - chat - mcp"
# 	@echo "706) microsoft agent framework - azure ai - chat - mcp inspector"
# 	@echo "707) microsoft agent framework - azure ai - chat - middleware"
# 	@echo "708) microsoft agent framework - azure ai - chat - middleware security"
	@echo "709) microsoft agent framework - azure ai - chat - images_uri"
	@echo "710) microsoft agent framework - azure ai - chat - images_uri_local"
# 	@echo "711) microsoft agent framework - azure ai - chat - openAPI"
# 	@echo "712) microsoft agent framework - azure ai - chat - multi-turn conversation"
# 	@echo "713) microsoft agent framework - azure ai - chat - persistent conversation"
# 	@echo "714) microsoft agent framework - azure ai - chat - workflow sequencial"
# 	@echo "715) microsoft agent framework - azure ai - chat - workflow concurrent"
# 	@echo "716) microsoft agent framework - azure ai - chat - observability"
# 	@echo "716) microsoft agent framework - azure ai - chat - evaluation"
	@echo "750) microsoft agent framework - azure ai - agent - basic chat agent"	
	@echo "751) microsoft agent framework - azure ai - agent - basic chat agent stream"

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
		700) make execute example="07_frameworks.microsoft_agent_framework.azure_ai.agent_framework_basic_chat_message" ;; \
		701) make execute example="07_frameworks.microsoft_agent_framework.azure_ai.agent_framework_basic_chat_message_stream" ;; \
		702) make execute example="07_frameworks.microsoft_agent_framework.azure_ai.agent_framework_structured_output" ;; \
		703) make execute example="07_frameworks.microsoft_agent_framework.azure_ai.agent_framework_function_tools" ;; \
		704) make execute example="07_frameworks.microsoft_agent_framework.azure_ai.agent_framework_function_tools_human_approval" ;; \
		705) make execute example="07_frameworks.microsoft_agent_framework.azure_ai.agent_framework_mcp" ;; \
		706) make execute example="07_frameworks.microsoft_agent_framework.azure_ai.agent_framework_mcp_inspector" ;; \
		707) make execute example="07_frameworks.microsoft_agent_framework.azure_ai.agent_framework_middleware" ;; \
		708) make execute example="07_frameworks.microsoft_agent_framework.azure_ai.agent_framework_middleware_security" ;; \
		709) make execute example="07_frameworks.microsoft_agent_framework.azure_ai.agent_framework_images_uri" ;; \
		710) make execute example="07_frameworks.microsoft_agent_framework.azure_ai.agent_framework_images_local" ;; \
		711) make execute example="07_frameworks.microsoft_agent_framework.azure_ai.agent_framework_openapi" ;; \
		712) make execute example="07_frameworks.microsoft_agent_framework.azure_ai.agent_framework_multi_turn_conversation" ;; \
		713) make execute example="07_frameworks.microsoft_agent_framework.azure_ai.agent_framework_persistent_conversation" ;; \
		714) make execute example="07_frameworks.microsoft_agent_framework.azure_ai.agent_framework_workflow_sequential" ;; \
		715) make execute example="07_frameworks.microsoft_agent_framework.azure_ai.agent_framework_workflow_concurrent" ;; \
		716) make execute example="07_frameworks.microsoft_agent_framework.azure_ai.agent_framework_observability" ;; \
		717) make execute example="07_frameworks.microsoft_agent_framework.azure_ai.agent_framework_evaluation" ;; \
		750) make execute example="07_frameworks.microsoft_agent_framework.azure_ai.chat.agent_framework_basic_chat_agent" ;; \
		751) make execute example="07_frameworks.microsoft_agent_framework.azure_ai.chat.agent_framework_basic_chat_agent_stream" ;; \
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
