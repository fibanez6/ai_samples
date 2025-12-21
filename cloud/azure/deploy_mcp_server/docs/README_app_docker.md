# Build Docker Image

## Prerequisites

- Docker installed on your system
- Docker daemon running
- Ensure `uv.lock` and `pyproject.toml` exist

## Building the Image

To build the Docker image, run the following command from the project root:

```bash
cd azure/deploy_mcp_server
docker build -f app/Dockerfile -t mcp-server:latest .
```

## Verifying the Build

Check that the image was created successfully:

```bash
docker images | grep mcp-server
```

## Running the Container

To run the container:

```bash
docker run -d \
    -e MCP_ENTRY=server_http_basic_mcp \
    -p 8000:8000 \
    --name mcp-server \
    mcp-server:latest
```

# Run with environment file
```bash
docker run -p 8000:8000 --env-file .env --name mcp-server mcp-server:latest
```

### Example .env file
```bash
MCP_ENTRY=app.server_http_basic
AZURE_COSMOSDB_ACCOUNT=your-account
AZURE_COSMOSDB_DATABASE=your-db
AZURE_COSMOSDB_CONTAINER=your-container
```

## Testing the Container

```bash
# Check health endpoint
curl http://localhost:8000/health

# View logs
docker logs mcp-server

# Stop container
docker stop mcp-server

# Remove container
docker rm mcp-server
```

## Additional Options

### Build with custom tag

```bash
docker build -f azure/deploy_mcp_server/Dockerfile -t mcp-server:v1.0.0 .
```

### Build for Azure Container Registry

```bash
docker build -f azure/deploy_mcp_server/Dockerfile -t yourregistry.azurecr.io/mcp-server:latest .
docker push yourregistry.azurecr.io/mcp-server:latest
```

### Build without cache (clean build)

```bash
docker build --no-cache -f azure/deploy_mcp_server/Dockerfile -t mcp-server:latest .
```