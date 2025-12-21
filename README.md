# AI Samples

A curated set of practical AI examples and agentic workflows using OpenAI, Microsoft Agent Framework, MCP, RAG, and observability tooling. This repo is organized into small, runnable samples you can explore via a simple `Makefile` menu.

## Repository Structure

```
ai_samples/
├── agents/
│   ├── microsoft_agent_framework/        # Azure AI + Microsoft Agent Framework samples
│   │   ├── azure_ai/                     # Chat, tools, images, structured outputs, middleware
│   │   └── azure_ai_agent/               # Agent-focused variations (stream, structured, tools)
│   └── openai/                           # OpenAI provider samples and helpers
│       ├── 01_chat/                      # Chat basics (basic, stream, async, history, safety)
│       ├── 02_function_tools/            # Function/tool calling (basic, extended, stream, parallel)
│       ├── 03_structured_outputs/        # Pydantic and structured response patterns
│       ├── 04_rag/                       # Retrieval-Augmented Generation samples
│       ├── 05_mcp/                       # MCP server and LangChain MCP client demos
│       ├── 06_middleware/                # Observability and middleware demos
│       └── ...                           # Additional patterns and evaluations
├── cloud/
│   └── azure/
│       └── deploy_mcp_server/            # FastAPI MCP server for Azure deployment
├── docs/                                  # Reference docs and images
├── utils/                                 # Shared utilities
├── Makefile                               # Menu to run samples
├── pyproject.toml                         # Python 3.13+ and dependencies
├── LICENSE                                # MIT License
└── README.md                              # This file
```

## Quick Start

- Python 3.13+ and `uv` recommended; `pip` works too.
- Create `.env` with your provider credentials (see below).

Setup with `uv`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
```

Run the menu to explore samples:

```bash
make select
```

Or run a specific sample directly (example: OpenAI chat basic):

```bash
make execute example="agents.openai.01_chat.chat_basic"
```

Azure MCP server (HTTP) locally via Uvicorn:

```bash
make execute_uvicorn example="cloud.azure.deploy_mcp_server.app.server_http_basic_mcp"
```

## Provider Configuration

Set your preferred provider in `.env`:

- AGENT_PROVIDER: `github` (default) | `openai` | `azure` | `anthropic` | `ollama`
- Model name per provider via `{PROVIDER}_MODEL`, e.g. `OPENAI_MODEL`, `GITHUB_MODEL`, `AZURE_MODEL`, `ANTHROPIC_MODEL`, `OLLAMA_MODEL`

Credentials and endpoints used by the samples:

- OpenAI (sync client): `OPENAI_API_KEY`
- OpenAI (async client): `OPENAI_KEY` (used by async variants)
- GitHub Models: `GITHUB_TOKEN`, optional `GITHUB_API_URL` (defaults to https://models.github.ai/inference)
- Azure OpenAI: `AZURE_ENDPOINT` and local Azure auth via DefaultAzureCredential (Azure CLI/Workload Identity/Managed Identity)
- Anthropic: `ANTHROPIC_API_KEY`
- Ollama: `OLLAMA_HOST` (e.g., http://localhost:11434)

Note: Some samples use `AsyncOpenAI` and others `OpenAI`. Ensure the correct OpenAI key env var is present for the variant you run.

## Common Examples

- OpenAI Chat (basic): `agents.openai.01_chat.chat_basic`
- OpenAI Tools (parallel): `agents.openai.02_function_tools.tools_multiple_parallel`
- Structured Outputs (Pydantic): `agents.openai.03_structured_outputs.structured_pydantic`
- RAG Basic: `agents.openai.04_rag.rag_basic`
- MCP Server (stdio/SSE/HTTP): see `agents.openai.05_mcp.*`
- Middleware + OpenTelemetry: `agents.openai.06_middleware.middleware_mcp_opentelemetry`

Explore Microsoft Agent Framework samples under `agents/microsoft_agent_framework/azure_ai*`.

## References

- MCP servers and links: see [README_mcp.md](README_mcp.md)
- Curated external repos: see [README_repos.md](README_repos.md)

## License

MIT License. See [LICENSE](LICENSE).

---

Built to be small, focused, and easy to run.