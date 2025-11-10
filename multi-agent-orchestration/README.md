# Multi-Agent Orchestration System

🎭 A modern multi-agent orchestration system using **LangGraph**, **OpenAI Agents**, and **MCP (Model Context Protocol) servers** for intelligent research, analysis, and action planning workflows.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                LangGraph Orchestrator                       │
│    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│    │  Research   │  │  Analysis   │  │   Action    │       │
│    │   Agent     │─▶│   Agent     │─▶│   Agent     │       │
│    │   (A)       │  │   (B)       │  │   (C)       │       │
│    └─────────────┘  └─────────────┘  └─────────────┘       │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    MCP Servers                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ HTTP Fetcher│  │  Web Scraper│  │  Database   │         │
│  │   Server    │  │   Server    │  │   Server    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   External APIs                             │
│         Web APIs • Databases • File Systems                │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Features

### ✅ Multi-Agent Coordination
- **Research Agent**: Gathers information using MCP tools (HTTP fetching, web scraping)
- **Analysis Agent**: Analyzes and synthesizes information from multiple sources
- **Action Agent**: Generates strategic recommendations and action plans
- **LangGraph Orchestrator**: Coordinates agent workflows with state management

### ✅ MCP Server Integration
- **HTTP Fetcher**: Retrieves content from URLs with headers and timeout management
- **Web Scraper**: Extracts structured data using CSS selectors and intelligent parsing
- **Database Storage**: SQLite-based storage for research data and analysis results
- **Search Capabilities**: Full-text search across stored content

### ✅ Modern Architecture
- **LangGraph Workflows**: State-based agent coordination with conditional routing
- **OpenAI Integration**: GPT-4 powered agents with specialized prompts
- **FastAPI MCP Server**: RESTful API for external tool integration
- **Async/Await**: Non-blocking operations for improved performance

## 🚀 Quick Start

### 1. Installation

#### Option A: Using Make (Easiest)
```bash
# Clone the repository
git clone <repository-url>
cd multi-agent-orchestration

# Install dependencies with Make
make install

# See all available commands
make help
```

#### Option B: Using UV directly
```bash
# Clone the repository
git clone <repository-url>
cd multi-agent-orchestration

# Install with UV (recommended)
uv sync
```



### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
nano .env
```

**Required Configuration:**
```env
OPENAI_API_KEY=your_openai_api_key_here
MCP_SERVER_URL=http://localhost:8000
```

### 3. Start MCP Server

#### Option A: Using Make
```bash
# Start MCP server with auto-reload
make start

# Or start development environment (server + monitoring)
make dev
```

#### Option B: Using UV directly
```bash
# Start MCP server with UV (recommended)
uv run uvicorn src.mcp_server.server:app --host 0.0.0.0 --port 8000 --reload

# Or using CLI with UV
uv run python -m src.cli start-mcp-server
```

### 4. Run Your First Orchestration

#### Option A: Using Make
```bash
# Quick demo
make demo

# Execute custom queries
make execute QUERY="What are the latest AI trends for 2024?"

# Run examples
make examples

# Check system health
make health
```

#### Option B: Using UV directly
```bash
# Quick demo
uv run python quick_start.py

# Execute custom queries with UV
uv run python -m src.cli execute "What are the latest AI trends for 2024?"

# Run examples
uv run python -m src.cli examples
```

## �️ Make Commands Reference

The project includes a comprehensive Makefile for easier development:

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make install` | Install dependencies with UV |
| `make start` | Start MCP server with auto-reload |
| `make demo` | Run quick demo |
| `make examples` | Run example workflows |
| `make health` | Check system health |
| `make config` | Create default configuration |
| `make execute QUERY="..."` | Execute a custom query |
| `make dev` | Start development environment |
| `make format` | Format code with Black |
| `make lint` | Lint code with Ruff |
| `make test` | Run tests |
| `make check` | Format, lint, and test |
| `make clean` | Clean up cache and temporary files |

**Example Usage:**
```bash
# Start the system
make install
make start

# In another terminal, run a demo
make demo

# Execute a custom query
make execute QUERY="Analyze the impact of AI on healthcare"
```

## �📖 Usage Examples

### Basic Usage

```python
import asyncio
from src.orchestrator.langgraph_orchestrator import MultiAgentOrchestrator

async def main():
    # Initialize orchestrator
    orchestrator = MultiAgentOrchestrator()
    
    # Define your research query
    query = "What are the latest trends in AI and machine learning?"
    
    # Optional parameters
    user_input = {
        "urls": ["https://arxiv.org/list/cs.AI/recent"],
        "search_terms": ["AI trends 2024"],
        "max_sources": 3,
        "analysis_type": "comprehensive"
    }
    
    # Execute multi-agent workflow
    results = await orchestrator.execute(query, user_input)
    
    # Access results
    print("Research Summary:", results["research_summary"])
    print("Key Insights:", results["key_insights"])
    print("Recommendations:", results["strategic_recommendations"])
    print("Action Plan:", results["action_plan"])

asyncio.run(main())
```

### Advanced Usage with Configuration

```python
from src.config.settings import get_config, MultiAgentConfig
from src.orchestrator.langgraph_orchestrator import MultiAgentOrchestrator

# Load custom configuration
config = MultiAgentConfig.from_file("custom_config.json")

# Initialize with custom settings
orchestrator = MultiAgentOrchestrator(
    mcp_base_url=config.mcp_server.base_url
)

# Complex query with objectives and constraints
user_input = {
    "objectives": [
        "Identify market opportunities",
        "Assess competitive landscape",
        "Provide actionable recommendations"
    ],
    "constraints": {
        "budget": "Limited budget",
        "timeline": "6-month implementation"
    },
    "focus_areas": ["Technology", "Market", "Strategy"]
}

results = await orchestrator.execute(
    "Analyze the AI customer service market", 
    user_input
)
```

## 🛠️ Commands with UV

### Main Commands (Recommended)

```bash
# Start MCP server with auto-reload
uv run uvicorn src.mcp_server.server:app --host 0.0.0.0 --port 8000 --reload

# Quick demo
uv run python quick_start.py

# Run examples
uv run python -m src.cli examples

# Check system health
uv run python -m src.cli health

# Development commands
uv run pytest                    # Run tests
uv run black src/               # Format code
uv run ruff check src/          # Lint code
```

### CLI Commands with UV

```bash
# Execute a query
uv run python -m src.cli execute "Your query here" \
    --url https://example.com \
    --search "search terms" \
    --max-sources 5 \
    --analysis comprehensive \
    --output results.json

# Check system health
uv run python -m src.cli health

# Configuration management
uv run python -m src.cli config --create
uv run python -m src.cli config --validate
uv run python -m src.cli config --show

# Start MCP server
uv run python -m src.cli start-mcp-server --host 0.0.0.0 --port 8000

# Run examples
uv run python -m src.cli examples
```

### Alternative Methods

```bash
# If you have the package installed
multi-agent execute "Your query here"

# Direct Python execution
uv run python -m src.cli execute "Your query here"
```

## 🏗️ Project Structure

```
multi-agent-orchestration/
├── src/
│   ├── agents/                    # Agent implementations
│   │   ├── base_agent.py         # Base agent class
│   │   ├── research_agent.py     # Research Agent (A)
│   │   ├── analysis_agent.py     # Analysis Agent (B)
│   │   └── action_agent.py       # Action Agent (C)
│   ├── orchestrator/             # LangGraph orchestration
│   │   └── langgraph_orchestrator.py
│   ├── mcp_server/               # MCP server implementation
│   │   ├── server.py            # FastAPI server
│   │   └── client.py            # MCP client utilities
│   ├── config/                   # Configuration management
│   │   └── settings.py          # Settings and validation
│   ├── utils/                    # Utility functions
│   │   └── workflow_utils.py    # Workflow helpers
│   ├── examples/                 # Usage examples
│   │   └── usage_examples.py    # Example scripts
│   └── cli.py                   # Command-line interface
├── tests/                       # Test suite
├── .env.example                 # Environment template
├── config.json                  # Configuration template
└── README.md                    # This file
```

## 🔧 Configuration

### Environment Variables

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.7

# MCP Server Configuration
MCP_SERVER_URL=http://localhost:8000
MCP_TIMEOUT=30
MCP_MAX_RETRIES=3

# Orchestrator Configuration
ORCHESTRATOR_MAX_RETRIES=2
ORCHESTRATOR_TIMEOUT=300
CACHE_ENABLED=true

# Security Configuration
RATE_LIMIT_RPM=60
MAX_CONTENT_SIZE_MB=10
CONTENT_FILTERING=true
```

### Configuration File (config.json)

```json
{
  "openai": {
    "api_key": "your_api_key",
    "model": "gpt-4",
    "temperature": 0.7
  },
  "mcp_server": {
    "base_url": "http://localhost:8000",
    "timeout": 30
  },
  "orchestrator": {
    "max_retries": 2,
    "cache_enabled": true
  }
}
```

## 🔍 How It Works

### 1. Research Phase (Agent A)
- Receives research query and parameters
- Uses MCP server to fetch content from URLs
- Scrapes web pages with intelligent parsing
- Searches existing knowledge base
- Stores and organizes research data

### 2. Analysis Phase (Agent B)
- Receives research data from Agent A
- Extracts key insights and patterns
- Evaluates source credibility
- Synthesizes information from multiple sources
- Generates structured analysis report

### 3. Action Phase (Agent C)
- Receives analysis results from Agent B
- Develops strategic recommendations
- Creates prioritized action plans
- Assesses risks and resource requirements
- Defines success metrics and next steps

### 4. Orchestration (LangGraph)
- Manages workflow state between agents
- Handles error recovery and retries
- Implements conditional routing logic
- Provides execution monitoring and logging

## 🎯 Use Cases

### Business Intelligence
- **Market Research**: Analyze competitors, trends, and opportunities
- **Strategic Planning**: Generate actionable business strategies
- **Risk Assessment**: Identify and mitigate potential risks

### Research & Analysis
- **Academic Research**: Gather and synthesize research papers
- **Technology Assessment**: Evaluate new technologies and tools
- **Trend Analysis**: Identify emerging patterns and insights

### Content & Media
- **Content Strategy**: Research topics and create content plans
- **Media Monitoring**: Track brand mentions and sentiment
- **Competitive Analysis**: Monitor competitor activities

## 🔄 Workflow Examples

### Example 1: Market Research
```
Query: "Analyze the competitive landscape for AI customer service solutions"

Research Agent → Fetches competitor websites, product pages, pricing info
Analysis Agent → Compares features, identifies market gaps, assesses positioning
Action Agent → Recommends market entry strategy, pricing, and differentiation
```

### Example 2: Technology Assessment
```
Query: "Evaluate blockchain adoption in supply chain management"

Research Agent → Gathers case studies, whitepapers, industry reports
Analysis Agent → Identifies benefits, challenges, and success factors
Action Agent → Provides implementation roadmap and ROI projections
```

## 🔧 UV Development Workflow

This project is optimized for **UV**, the fast Python package manager. Here's the recommended development workflow:

### Daily Development Commands

```bash
# Start development server (with auto-reload)
uv run uvicorn src.mcp_server.server:app --host 0.0.0.0 --port 8000 --reload

# Quick testing of the system
uv run python quick_start.py

# Run comprehensive examples
uv run python -m src.cli examples
```

### Code Quality Commands

```bash
# Format code
uv run black src/

# Lint code  
uv run ruff check src/

# Run tests
uv run pytest
```

### Project Management

```bash
# Install/update dependencies
uv sync

# Add new dependency
uv add package-name

# Add development dependency
uv add --dev package-name

# Run any command in the project environment
uv run python your_script.py
```

### Why UV?

- ⚡ **Fast**: 10-100x faster than pip
- 🔒 **Reliable**: Lockfile-based dependency resolution
- 🎯 **Modern**: Python 3.12+ support with latest features
- 🛠️ **Developer-friendly**: Built-in script running and environment management

## ⚡ Performance & Scalability

- **Async Processing**: Non-blocking operations for better performance
- **Caching System**: Intelligent caching to avoid redundant operations
- **Rate Limiting**: Respects API limits and prevents overload
- **Error Handling**: Robust error recovery and retry mechanisms
- **Resource Management**: Efficient memory and connection pooling

## 🧪 Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Run specific test categories
uv run pytest tests/agents/
uv run pytest tests/orchestrator/
uv run pytest tests/mcp_server/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangGraph**: For state-based agent orchestration
- **OpenAI**: For powerful language model capabilities
- **FastAPI**: For high-performance API development
- **LangChain**: For agent framework and utilities

## 📞 Support

For questions, issues, or contributions:
- Open an issue on GitHub
- Check the [documentation](docs/)
- Review the [examples](src/examples/)

---

**Built with ❤️ for modern AI-powered workflows**
