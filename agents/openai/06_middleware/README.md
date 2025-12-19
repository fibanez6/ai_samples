# Middleware with MCP + OpenTelemetry

[Azure-Samples / python-mcp-demos](https://github.com/Azure-Samples/python-mcp-demos/tree/main)

## Index
 - [Middleware with MCP + OpenTelemetry](#middleware-with-mcp--opentelemetry)
 - [Prerequisites](#prerequisites)
 - [Setup](#setup)
 - [Run Aspire Dashboard](#1-run-the-aspire-dashboard-otlp-endpoint)
 - [Run MCP server](#2-run-the-mcp-server)
 - [Run MCP client (Inspector)](#3-run-the-mcp-client-inspector)
 - [Try it out](#4-try-it-out)
 - [Open Aspire Dashboard](#5-open-the-aspire-dashboard-in-your-browser)
 - [Troubleshooting](#troubleshooting)
 - [References](#references)

This folder contains a minimal Model Context Protocol (MCP) server instrumented with OpenTelemetry middleware for observability. The example exposes a simple "Expenses Tracker" service you can inspect via the MCP Inspector and visualize telemetry in the Microsoft Aspire Dashboard.

Key files:
- [agents/openai/06_middleware/middleware_mcp_opentelemetry.py](agents/openai/06_middleware/middleware_mcp_opentelemetry.py): FastMCP server exposing tools, resources, and prompts, and wiring the middleware.
- [agents/openai/06_middleware/opentelemetry_middleware.py](agents/openai/06_middleware/opentelemetry_middleware.py): OpenTelemetry middleware that creates spans for MCP tool calls, resources, and prompts.

## Prerequisites

- Python 3.10+ and a virtual environment activated.
- Node.js (for the MCP Inspector `@modelcontextprotocol/inspector`).
- Docker (to run the Microsoft Aspire Dashboard easily).

Optional (but recommended for telemetry):
- An OTLP gRPC endpoint. The instructions below use the Aspire standalone dashboard.

## Setup

Install project dependencies using your preferred tool. If you're using `uv`:

```bash
uv sync
```

If you prefer `pip`, from the repository root:

```bash
pip install fastmcp python-dotenv opentelemetry-sdk opentelemetry-exporter-otlp
```

## 1) Run the Aspire Dashboard (OTLP endpoint)

Start the dashboard container exposing the UI and OTLP ports:

```bash
docker run --rm -d \
  -p 18888:18888 \
  -p 4317:18889 \
  --name aspire-dashboard \
  mcr.microsoft.com/dotnet/aspire-dashboard:latest

docker logs aspire-dashboard 2>&1 | grep "Login to the dashboard"
```

Export the OTLP endpoint so the server can send telemetry:

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4317"
```

## 2) Run the MCP server

From the repository root, start the server. Using `uv`:

```bash
uv run python agents/openai/06_middleware/middleware_mcp_opentelemetry.py
```

Or with plain Python:

```bash
python agents/openai/06_middleware/middleware_mcp_opentelemetry.py
```

The server listens on `http://localhost:8000/mcp` and will create/update an `expenses.csv` file in this folder.

## 3) Run the MCP client (Inspector)

In another terminal:

```bash
npx @modelcontextprotocol/inspector http://localhost:8000/mcp
```

This opens an interactive UI where you can call tools, read resources, and fetch prompts.

## 4) Try it out

In the Inspector:
- Call the tool `add_expense` with fields like `date`, `amount`, `category`, `description`, and `payment_method`.
- Read the resource `resource://expenses` to view entries.
- Fetch the prompt `analyze_spending_prompt` (optionally set `category`, `start_date`, `end_date`).

Telemetry spans will be emitted for each operation when `OTEL_EXPORTER_OTLP_ENDPOINT` is set.

## 5) Open the Aspire Dashboard in your browser

Go to `http://localhost:18888` and use the login token from the container logs. You should see traces, logs, and metrics from the MCP server.

## Troubleshooting

- No telemetry showing: verify `OTEL_EXPORTER_OTLP_ENDPOINT` is set and the Aspire container is running.
- Port conflicts: change `-p 18888:18888` and `-p 4317:18889` to available ports and update the endpoint accordingly.
- Inspector cannot connect: ensure the server is running and reachable at `http://localhost:8000/mcp`.

## References

- [MCP Inspector](https://www.npmjs.com/package/@modelcontextprotocol/inspector)
- [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/)
- [Microsoft Aspire Dashboard](https://learn.microsoft.com/dotnet/aspire/)
- [Azure MCP Demo](https://github.com/azure-samples/python-mcp-demo)

