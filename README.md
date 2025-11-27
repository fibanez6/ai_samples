# AI Samples Repository

This repository contains a collection of AI and agentic workflow samples, including multi-agent orchestration systems, agent frameworks, and practical examples for research, analysis, and automation.

## 📁 Repository Structure

```
ai_samples/
├── 01-chat/                       # Basic chat agent example
├── 02-chat-stream/                # Streaming chat agent example
├── 03-tools/                      # Tool-using agent examples
├── 04-agent/                      # General agent framework samples
├── 0X-agent-framework/
│   ├── langchain/                 # LangChain agent framework samples
│   └── microsoft-agent-framework/ # Microsoft agent framework samples
├── 0X-agentic-pattern/
│   └── reflection-pattern/        # Agentic reflection pattern example
├── 0X-mcp/                        # Model Context Protocol (MCP) samples
├── 0X-multi-agent-orchestration/  # Multi-agent orchestration system (LangGraph, MCP, OpenAI)
│   ├── src/
│   │   ├── agents/                # Agent implementations (Research, Analysis, Action)
│   │   ├── orchestrator/          # LangGraph orchestrator
│   │   ├── mcp_server/            # MCP server (FastAPI)
│   │   ├── config/                # Configuration management
│   │   ├── utils/                 # Utilities
│   │   ├── examples/              # Usage examples
│   │   └── cli.py                 # CLI interface
│   ├── quick_start.py             # Quick start script
│   ├── Makefile                   # Development commands
│   ├── pyproject.toml             # Project dependencies
│   ├── config.json                # Configuration template
│   ├── .env.example               # Environment template
│   └── README.md                  # Detailed system documentation
├── LICENSE
└── README.md                      # This file
```

## 🚀 Key Projects

- **Multi-Agent Orchestration System** (`0X-multi-agent-orchestration/`)
	- LangGraph-based orchestrator for coordinating Research, Analysis, and Action agents
	- MCP server for tool integration (HTTP fetcher, web scraper, database)
	- OpenAI-powered agents for intelligent workflows
	- Async, stateful, and extensible architecture

- **Agent Frameworks**
	- LangChain and Microsoft agent framework samples for building custom agents

- **Agentic Patterns**
	- Reflection pattern and other agentic workflow examples


## Resources

- [Microsoft ai-agents-for-beginners](https://github.com/microsoft/ai-agents-for-beginners)


## 🛠️ Installation

### Prerequisites

- **Python 3.13+**
- **uv** (recommended) or **pip** 
- One of the AI providers configured (see AI Provider Setup below)

### Quick Start

1. **Clone and navigate to the project:**
   ```bash
   cd ai-samples
   ```

2. **Install dependencies:**

   **Option A: Using uv (recommended - fastest):**
   ```bash
   # Install uv if not already installed
   curl -LsSf https://astral.sh/uv/install.sh | sh
   source $HOME/.local/bin/env

   # Sync all dependencies (creates virtual environment automatically)
   uv sync
   ```

   **Option B: Traditional pip installation:**
   ```bash
   python3.13 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install --upgrade pip
   pip install -e .
   ```

4. **Configure AI provider:**
   ```bash
   # Create environment file
   cp .env.example .env     # If available, or create new .env file

   # Edit .env with your credentials
   nano .env
   ```

5. **Run the application:**
   ```bash
   make select
   ```

## 📜 License

MIT License. See the [LICENSE](LICENSE) file for details.

---

**Built for modern AI-powered agentic workflows.**