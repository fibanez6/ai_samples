"""
Research Agent - Agent A
Responsible for obtaining information using MCP (fetching and scraping).
"""

import asyncio
import json
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin, urlparse

from ..mcp_server.client import (MCPClient, fetch_and_store,
                                 scrape_and_extract, search_stored_data)
from .base_agent import BaseAgent


class ResearchAgent(BaseAgent):
    """Agent responsible for research and data gathering via MCP."""
    
    def __init__(
        self,
        name: str = "Research Agent",
        model: str = "gpt-4",
        temperature: float = 0.3,  # Lower temperature for more focused research
        mcp_base_url: str = "http://localhost:8000"
    ):
        super().__init__(name, model, temperature)
        self.mcp_base_url = mcp_base_url
        self.research_cache: Dict[str, Any] = {}
    
    def get_system_prompt(self) -> str:
        return """
        You are a Research Agent specialized in gathering and organizing information from various sources.
        
        Your capabilities include:
        - Fetching content from URLs
        - Scraping and parsing web pages
        - Searching through previously collected data
        - Analyzing source reliability
        - Organizing research findings
        
        Your tasks:
        1. Understand research queries and identify the best sources
        2. Use MCP tools to fetch and scrape content
        3. Validate and organize the information
        4. Provide structured research summaries
        5. Suggest additional research directions when needed
        
        Always be thorough but efficient. Focus on high-quality, relevant sources.
        Provide source attribution for all information gathered.
        """
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process research request and gather information."""
        query = input_data.get("query", "")
        urls = input_data.get("urls", [])
        search_terms = input_data.get("search_terms", [])
        max_sources = input_data.get("max_sources", 5)
        
        if not query and not urls and not search_terms:
            return {
                "error": "No research query, URLs, or search terms provided",
                "status": "failed"
            }
        
        research_results = {
            "query": query,
            "sources_researched": [],
            "content_gathered": [],
            "search_results": [],
            "summary": "",
            "recommendations": [],
            "status": "completed"
        }
        
        try:
            async with MCPClient(self.mcp_base_url) as mcp_client:
                # Check MCP server health
                await mcp_client.health_check()
                
                # 1. Search existing data first
                if search_terms:
                    for term in search_terms:
                        search_result = await search_stored_data(term, mcp_client, limit=3)
                        research_results["search_results"].append({
                            "term": term,
                            "results": search_result
                        })
                
                # 2. Fetch new content from URLs
                if urls:
                    for url in urls[:max_sources]:
                        try:
                            # Determine if we should scrape or just fetch
                            if self._should_scrape_url(url):
                                content_data = await scrape_and_extract(url, mcp_client)
                                research_results["content_gathered"].append({
                                    "url": url,
                                    "type": "scraped",
                                    "title": content_data.get("title", ""),
                                    "content": content_data.get("content", "")[:2000],  # Truncate for processing
                                    "extracted_data": content_data.get("extracted_data", {})
                                })
                            else:
                                content = await fetch_and_store(url, mcp_client)
                                research_results["content_gathered"].append({
                                    "url": url,
                                    "type": "fetched",
                                    "content": content[:2000]  # Truncate for processing
                                })
                            
                            research_results["sources_researched"].append(url)
                            
                        except Exception as e:
                            research_results["content_gathered"].append({
                                "url": url,
                                "type": "error",
                                "error": str(e)
                            })
                
                # 3. If we have a query but no URLs, suggest research directions
                if query and not urls:
                    suggestions = await self._generate_research_suggestions(query)
                    research_results["recommendations"] = suggestions
                
                # 4. Generate research summary
                research_results["summary"] = await self._generate_research_summary(
                    query, research_results
                )
                
                # Cache results
                cache_key = f"{query}_{hash(str(urls))}"
                self.research_cache[cache_key] = research_results
                
        except Exception as e:
            research_results["status"] = "failed"
            research_results["error"] = str(e)
        
        return research_results
    
    def _should_scrape_url(self, url: str) -> bool:
        """Determine if URL should be scraped (web page) or just fetched."""
        parsed = urlparse(url)
        
        # Web pages that should be scraped
        web_domains = ['www.', 'blog.', 'news.', 'article.']
        web_extensions = ['.html', '.htm', '.php', '.asp', '.aspx']
        
        # Check domain
        if any(parsed.netloc.startswith(domain) for domain in web_domains):
            return True
        
        # Check path extension
        if any(parsed.path.endswith(ext) for ext in web_extensions):
            return True
        
        # Default to scraping for most HTTP/HTTPS URLs without file extensions
        if parsed.scheme in ['http', 'https'] and '.' not in parsed.path.split('/')[-1]:
            return True
        
        return False
    
    async def _generate_research_suggestions(self, query: str) -> List[str]:
        """Generate research suggestions for a query."""
        messages = [{
            "role": "user",
            "content": f"""
            Given the research query: "{query}"
            
            Suggest 5 specific and actionable research directions or sources that would help answer this query.
            Focus on:
            1. Reliable primary sources
            2. Academic or authoritative publications
            3. Recent data or studies
            4. Different perspectives on the topic
            5. Practical examples or case studies
            
            Provide each suggestion as a bullet point.
            """
        }]
        
        response = await self.invoke_llm(messages)
        
        # Parse suggestions from response
        suggestions = []
        for line in response.split('\n'):
            line = line.strip()
            if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                suggestions.append(line[1:].strip())
            elif line and not line.startswith('Given') and len(line) > 20:
                suggestions.append(line)
        
        return suggestions[:5]
    
    async def _generate_research_summary(
        self,
        query: str,
        research_results: Dict[str, Any]
    ) -> str:
        """Generate a comprehensive research summary."""
        content_summary = []
        
        for content in research_results["content_gathered"]:
            if content.get("type") == "scraped":
                content_summary.append(f"From {content['url']}:\nTitle: {content.get('title', 'N/A')}\nContent: {content.get('content', '')[:500]}...")
            elif content.get("type") == "fetched":
                content_summary.append(f"From {content['url']}:\nContent: {content.get('content', '')[:500]}...")
        
        search_summary = []
        for search in research_results["search_results"]:
            search_summary.append(f"Search for '{search['term']}' found {len(search['results'].get('scraped', [])) + len(search['results'].get('fetched', []))} results")
        
        messages = [{
            "role": "user",
            "content": f"""
            Research Query: {query}
            
            Gathered Content:
            {chr(10).join(content_summary)}
            
            Search Results:
            {chr(10).join(search_summary)}
            
            Please provide a comprehensive research summary that:
            1. Directly addresses the research query
            2. Synthesizes information from all sources
            3. Highlights key findings and insights
            4. Notes any gaps or limitations in the research
            5. Provides source attribution
            
            Format the summary in clear, organized sections.
            """
        }]
        
        summary = await self.invoke_llm(messages)
        return summary
    
    def get_capabilities(self) -> List[str]:
        """Return list of research agent capabilities."""
        base_capabilities = super().get_capabilities()
        research_capabilities = [
            "web_content_fetching",
            "web_scraping",
            "data_search",
            "source_validation",
            "research_synthesis",
            "mcp_integration"
        ]
        return base_capabilities + research_capabilities
    
    async def search_previous_research(self, search_term: str, limit: int = 5) -> Dict[str, Any]:
        """Search through previously conducted research."""
        async with MCPClient(self.mcp_base_url) as mcp_client:
            return await search_stored_data(search_term, mcp_client, limit)
    
    def get_research_cache(self) -> Dict[str, Any]:
        """Return current research cache."""
        return self.research_cache
    
    def clear_research_cache(self):
        """Clear research cache."""
        self.research_cache = {}