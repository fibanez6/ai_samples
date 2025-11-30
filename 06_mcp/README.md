# MCP Examples


# Run Inpection in STDIO mode

1. Run the MCP server

```bash
uv run python -m 06_mcp.mcp_basic_stdio
```

![MCP Basic STDIO Server Run](../docs/mcp_basic_stdio_server_run.png)

2. Run the inspector

```bash
npx @modelcontextprotocol/inspector .venv/bin/python 06_mcp/mcp_basic_stdio.py
```

![MCP Basic STDIO Inspector Run](../docs/mcp_basic_stdio_inspector_run.png)

3. Open the inspector in your browser

* Copy the url with token from the inspector run
* Paster the url in your browser
* Ensure:
  * Transport is set to STDIO
  * Command is set to .venv/bin/python
  * Arguments is set to 06_mcp/mcp_basic_stdio.py
  * Proxy Session Token is set to the token from the inspector run
* Click on "Connect"

![MCP Basic STDIO Inspector Browser](../docs/mcp_basic_stdio_inspector_browser.png)

4. Use the inspector to interact with the MCP server

![MCP Basic STDIO Inspector Browser](../docs/mcp_basic_stdio_inspector_browser_sample.png)


# Run Inpection in SEE mode

1. Run the MCP server

```bash
uv run python -m 06_mcp.mcp_basic_sse
```

![MCP Basic SSE Server Run](../docs/mcp_basic_sse_server_run.png)

2. Run the inspector

```bash 
npx @modelcontextprotocol/inspector http://localhost:8000/mcp
```

![MCP Basic SSE Inspector Run](../docs/mcp_basic_sse_inspector_run.png)

3. Open the inspector in your browser

* Copy the url with token from the inspector run
* Paster the url in your browser
* Ensure:
  * Transport is set to SSE
  * Transport URL is set to http://localhost:8000/sse
  * Proxy Session Token is set to the token from the inspector run
* Click on "Connect"

![MCP Basic SSE Inspector Browser](../docs/mcp_basic_sse_inspector_browser.png)

