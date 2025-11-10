"""
MCP (Model Context Protocol) Server with FastAPI.
Provides HTTP fetcher, scraper, and database capabilities for agents.
"""

import asyncio
import json
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional

import httpx
import uvicorn
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl

app = FastAPI(
    title="MCP Server",
    description="Model Context Protocol server for multi-agent orchestration",
    version="1.0.0"
)

# Database setup
DB_PATH = "mcp_data.db"

def init_db():
    """Initialize SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fetched_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            content TEXT,
            metadata TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scraped_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            title TEXT,
            content TEXT,
            extracted_data TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Pydantic models
class FetchRequest(BaseModel):
    url: HttpUrl
    headers: Optional[Dict[str, str]] = None
    timeout: int = 30

class ScrapeRequest(BaseModel):
    url: HttpUrl
    selectors: Optional[Dict[str, str]] = None  # CSS selectors for specific data
    extract_links: bool = False
    extract_images: bool = False

class DatabaseQuery(BaseModel):
    query: str
    params: Optional[List[Any]] = None

class SearchRequest(BaseModel):
    table: str
    search_term: str
    limit: int = 10

# HTTP Fetcher endpoints
@app.post("/fetch")
async def fetch_url(request: FetchRequest):
    """Fetch content from a URL and store in database."""
    try:
        async with httpx.AsyncClient(timeout=request.timeout) as client:
            headers = request.headers or {}
            response = await client.get(str(request.url), headers=headers)
            response.raise_for_status()
            
            content = response.text
            metadata = {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content_type": response.headers.get("content-type", ""),
                "size": len(content)
            }
            
            # Store in database
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO fetched_data (url, content, metadata) VALUES (?, ?, ?)",
                (str(request.url), content, json.dumps(metadata))
            )
            data_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {
                "id": data_id,
                "url": str(request.url),
                "content": content[:1000] + "..." if len(content) > 1000 else content,
                "metadata": metadata,
                "stored": True
            }
            
    except httpx.RequestError as e:
        raise HTTPException(status_code=400, detail=f"Request failed: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"HTTP error: {str(e)}")

@app.post("/scrape")
async def scrape_url(request: ScrapeRequest):
    """Scrape and parse content from a URL with optional selectors."""
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(str(request.url))
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract basic info
            title = soup.find('title')
            title_text = title.get_text().strip() if title else ""
            
            # Extract content based on selectors or default
            extracted_data = {}
            
            if request.selectors:
                for key, selector in request.selectors.items():
                    elements = soup.select(selector)
                    if elements:
                        if len(elements) == 1:
                            extracted_data[key] = elements[0].get_text().strip()
                        else:
                            extracted_data[key] = [elem.get_text().strip() for elem in elements]
            else:
                # Default extraction
                extracted_data["paragraphs"] = [p.get_text().strip() for p in soup.find_all('p')]
                extracted_data["headings"] = [h.get_text().strip() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
            
            if request.extract_links:
                links = soup.find_all('a', href=True)
                extracted_data["links"] = [{"text": link.get_text().strip(), "href": link['href']} for link in links]
            
            if request.extract_images:
                images = soup.find_all('img', src=True)
                extracted_data["images"] = [{"alt": img.get('alt', ''), "src": img['src']} for img in images]
            
            # Get main content (try to be smart about it)
            main_content = ""
            content_selectors = ['main', 'article', '.content', '#content', '.post', '.entry']
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    main_content = content_elem.get_text().strip()
                    break
            
            if not main_content:
                # Fallback to body text
                body = soup.find('body')
                main_content = body.get_text().strip() if body else soup.get_text().strip()
            
            # Store in database
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO scraped_data (url, title, content, extracted_data) VALUES (?, ?, ?, ?)",
                (str(request.url), title_text, main_content, json.dumps(extracted_data))
            )
            data_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {
                "id": data_id,
                "url": str(request.url),
                "title": title_text,
                "content": main_content[:1000] + "..." if len(main_content) > 1000 else main_content,
                "extracted_data": extracted_data,
                "stored": True
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

# Database endpoints
@app.post("/db/query")
async def execute_query(request: DatabaseQuery):
    """Execute a custom SQL query."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        if request.params:
            cursor.execute(request.query, request.params)
        else:
            cursor.execute(request.query)
        
        if request.query.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            data = [dict(zip(columns, row)) for row in results]
        else:
            conn.commit()
            data = {"affected_rows": cursor.rowcount}
        
        conn.close()
        return {"success": True, "data": data}
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")

@app.post("/db/search")
async def search_data(request: SearchRequest):
    """Search for data in the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        if request.table == "fetched_data":
            query = """
                SELECT id, url, substr(content, 1, 200) as content_preview, metadata, timestamp
                FROM fetched_data 
                WHERE url LIKE ? OR content LIKE ?
                ORDER BY timestamp DESC
                LIMIT ?
            """
            search_pattern = f"%{request.search_term}%"
            cursor.execute(query, (search_pattern, search_pattern, request.limit))
            
        elif request.table == "scraped_data":
            query = """
                SELECT id, url, title, substr(content, 1, 200) as content_preview, extracted_data, timestamp
                FROM scraped_data 
                WHERE url LIKE ? OR title LIKE ? OR content LIKE ?
                ORDER BY timestamp DESC
                LIMIT ?
            """
            search_pattern = f"%{request.search_term}%"
            cursor.execute(query, (search_pattern, search_pattern, search_pattern, request.limit))
        else:
            raise HTTPException(status_code=400, detail="Invalid table name")
        
        results = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        data = [dict(zip(columns, row)) for row in results]
        
        conn.close()
        return {"success": True, "results": data, "count": len(data)}
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")

@app.get("/db/stats")
async def get_database_stats():
    """Get database statistics."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Count records in each table
        cursor.execute("SELECT COUNT(*) FROM fetched_data")
        fetched_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM scraped_data")
        scraped_count = cursor.fetchone()[0]
        
        # Get recent activity
        cursor.execute("""
            SELECT url, timestamp FROM fetched_data 
            ORDER BY timestamp DESC LIMIT 5
        """)
        recent_fetches = cursor.fetchall()
        
        cursor.execute("""
            SELECT url, title, timestamp FROM scraped_data 
            ORDER BY timestamp DESC LIMIT 5
        """)
        recent_scrapes = cursor.fetchall()
        
        conn.close()
        
        return {
            "fetched_data_count": fetched_count,
            "scraped_data_count": scraped_count,
            "recent_fetches": [{"url": r[0], "timestamp": r[1]} for r in recent_fetches],
            "recent_scrapes": [{"url": r[0], "title": r[1], "timestamp": r[2]} for r in recent_scrapes]
        }
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "MCP Server",
        "description": "Model Context Protocol server for multi-agent orchestration",
        "version": "1.0.0",
        "endpoints": {
            "fetch": "POST /fetch - Fetch content from URL",
            "scrape": "POST /scrape - Scrape and parse content",
            "query": "POST /db/query - Execute SQL query",
            "search": "POST /db/search - Search database",
            "stats": "GET /db/stats - Database statistics",
            "health": "GET /health - Health check"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)