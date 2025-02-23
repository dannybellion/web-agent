from dataclasses import dataclass
from crawl4ai import AsyncWebCrawler
from typing import List
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
import httpx
import os
from fastapi import FastAPI, HTTPException


# ---------------------------
# Pydantic Agent Configuration
# ---------------------------
MODEL = "gemini-2.0-flash"
SYSTEM_PROMPT = """
You are an intelligent web agent that can perform two tasks:
1. Scrape a URL using Crawl4AI.
2. Perform a web search using Tavily
Provide a detailed report back to the user.
"""

# ---------------------------
# Pydantic Response Models
# ---------------------------
class WebResponse(BaseModel):
    content: str = Field(..., description="A summary of the search results")
    urls: List[str] = Field(..., description="List of URLs returned from the search")

# ---------------------------
# Dependencies
# ---------------------------
@dataclass
class WebAgentDeps:
    tavily_api_key: str = os.getenv('TAVILY_API_KEY')
    pass

# ---------------------------
# Tools
# ---------------------------
async def tavily_search(ctx: RunContext, query: str) -> List[str]:
    """
    Simulate a web search using Tavily.
    """
    tavily_api_key = ctx.deps.tavily_api_key
    url = "https://api.tavily.com/search"

    payload = {
        "query": query,
        "topic": "general",
        "search_depth": "basic",
        "max_results": 5,
        "include_answer": True,
        "include_raw_content": False,
        "include_images": False,
        "include_image_descriptions": False,
    }
    headers = {
        "Authorization": f"Bearer {tavily_api_key}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()

    return response.text

async def crawl4ai_scrape(ctx: RunContext, url: str) -> str:
    """
    Scrape a web page using Crawl4AI.
    """
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
    return result.markdown

# ---------------------------
# Single WebAgent Class
# ---------------------------
class WebAgent:
    def __init__(self, model_identifier: str = MODEL):
        self.deps = WebAgentDeps()
        self.agent = Agent(
            model=model_identifier,
            deps_type=WebAgentDeps,
            result_type=WebResponse,
            system_prompt=SYSTEM_PROMPT,
        )
        # Register both tools.
        self.agent.tool(tavily_search)
        self.agent.tool(crawl4ai_scrape)

    async def run(self, input_text: str) -> WebResponse:
        """
        Run the agent. The input_text can be a search query or a URL.
        The agent will decide which tool to call based on the input.
        """
        result = await self.agent.run(input_text, deps=self.deps)
        return result
    
# ---------------------------
# FastAPI App for the Web Agent
# ---------------------------
app = FastAPI(title="Web Agent API")

@app.get("/")
async def root():
    return {"message": "Web Agent API is running"}

class QueryInput(BaseModel):
    input_text: str

web_agent = WebAgent()

@app.post("/run")
async def run_web_agent(query: QueryInput):
    try:
        result = await web_agent.run(query.input_text)
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))