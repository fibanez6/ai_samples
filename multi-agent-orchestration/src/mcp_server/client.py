"""
MCP Client for interacting with the MCP server.
"""

import asyncio
from typing import Any, Dict, List, Optional

import httpx
from pydantic import BaseModel


class MCPClient:
    """Client for interacting with MCP server."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def fetch_url(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 30
    ) -> Dict[str, Any]:
        """Fetch content from a URL."""
        payload = {
            "url": url,
            "timeout": timeout
        }
        if headers:
            payload["headers"] = headers
        
        response = await self.client.post(f"{self.base_url}/fetch", json=payload)
        response.raise_for_status()
        return response.json()
    
    async def scrape_url(
        self,
        url: str,
        selectors: Optional[Dict[str, str]] = None,
        extract_links: bool = False,
        extract_images: bool = False
    ) -> Dict[str, Any]:
        """Scrape and parse content from a URL."""
        payload = {
            "url": url,
            "extract_links": extract_links,
            "extract_images": extract_images
        }
        if selectors:
            payload["selectors"] = selectors
        
        response = await self.client.post(f"{self.base_url}/scrape", json=payload)
        response.raise_for_status()
        return response.json()
    
    async def query_database(
        self,
        query: str,
        params: Optional[List[Any]] = None
    ) -> Dict[str, Any]:
        """Execute a SQL query on the database."""
        payload = {
            "query": query
        }
        if params:
            payload["params"] = params
        
        response = await self.client.post(f"{self.base_url}/db/query", json=payload)
        response.raise_for_status()
        return response.json()
    
    async def search_data(
        self,
        table: str,
        search_term: str,
        limit: int = 10
    ) -> Dict[str, Any]:
        """Search for data in the database."""
        payload = {
            "table": table,
            "search_term": search_term,
            "limit": limit
        }
        
        response = await self.client.post(f"{self.base_url}/db/search", json=payload)
        response.raise_for_status()
        return response.json()
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        response = await self.client.get(f"{self.base_url}/db/stats")
        response.raise_for_status()
        return response.json()
    
    async def health_check(self) -> Dict[str, Any]:
        """Check if the MCP server is healthy."""
        response = await self.client.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()

# Utility functions for common operations
async def fetch_and_store(url: str, mcp_client: MCPClient) -> str:
    """Fetch content from URL and return the stored content."""
    result = await mcp_client.fetch_url(url)
    return result.get("content", "")

async def scrape_and_extract(
    url: str,
    mcp_client: MCPClient,
    selectors: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """Scrape URL and return extracted data."""
    result = await mcp_client.scrape_url(
        url=url,
        selectors=selectors,
        extract_links=True,
        extract_images=True
    )
    return {
        "title": result.get("title", ""),
        "content": result.get("content", ""),
        "extracted_data": result.get("extracted_data", {})
    }

async def search_stored_data(
    search_term: str,
    mcp_client: MCPClient,
    limit: int = 5
) -> List[Dict[str, Any]]:
    """Search both fetched and scraped data."""
    fetched_results = await mcp_client.search_data("fetched_data", search_term, limit)
    scraped_results = await mcp_client.search_data("scraped_data", search_term, limit)
    
    return {
        "fetched": fetched_results.get("results", []),
        "scraped": scraped_results.get("results", [])
    }