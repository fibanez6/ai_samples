#!/bin/sh
set -e

# Default to deployed if not provided by runtime
MCP_ENTRY_VAL="${MCP_ENTRY:-server_http_azure_deployed}"

# Build ASGI target module path
APP_MODULE="${MCP_ENTRY_VAL}:app"

echo "Starting uvicorn with module: ${APP_MODULE}"
exec uvicorn "${APP_MODULE}" --host 0.0.0.0 --port 8000