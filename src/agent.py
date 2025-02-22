from dataclasses import dataclass
from typing import List, Union
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

# ---------------------------
# Pydantic Response Models
# ---------------------------
class WebSearchResponse(BaseModel):
    query: str = Field(..., description="The search query")
    urls: List[str] = Field(..., description="List of URLs returned from the search")

class WebScrapeResponse(BaseModel):
    url: str = Field(..., description="The URL that was scraped")
    content: str = Field(..., description="The scraped content from the URL")

# Define a union type for the agent's response.
Response = Union[WebSearchResponse, WebScrapeResponse]  # type: ignore

# ---------------------------
# Empty Dependency (if no shared dependency is needed)
# ---------------------------
@dataclass
class EmptyDeps:
    pass

# ---------------------------
# Shared Tools
# ---------------------------
def tavily_search(ctx: RunContext, query: str) -> List[str]:
    """
    Simulate a web search using Tavily.
    In production, replace this with an actual API call.
    """
    # For demonstration, return two dummy URLs.
    return [
        f"https://example.com/search_result1?q={query}",
        f"https://example.com/search_result2?q={query}"
    ]

def crawl4ai_scrape(ctx: RunContext, url: str) -> str:
    """
    Simulate scraping a web page using Crawl4AI.
    In production, this could use an HTTP library and parsing logic.
    """
    # Return dummy scraped content.
    return f"Scraped content from {url}"

# ---------------------------
# Single WebAgent Class
# ---------------------------
class WebAgent:
    def __init__(self, model_identifier: str = "openai:gpt-4o"):
        self.deps = EmptyDeps()
        # The agent is configured with a union response type.
        self.agent = Agent(
            model=model_identifier,
            deps_type=EmptyDeps,
            result_type=Response,  # type: ignore
            system_prompt=(
                "You are an intelligent web agent that can perform two tasks:\n"
                "1. If the user input is a URL, scrape the page using Crawl4AI.\n"
                "2. Otherwise, perform a web search using Tavily to return a list of URLs, "
                "and then scrape one of the URLs to provide sample content.\n"
                "Make sure your final response is structured as follows:\n"
                "- For a search: { 'query': <query>, 'urls': [<url1>, <url2>, ...] }\n"
                "- For a scrape: { 'url': <url>, 'content': <scraped content> }.\n"
                "Decide based on the input whether to search or scrape."
            ),
        )
        # Register both tools.
        self.agent.tool(tavily_search)
        self.agent.tool(crawl4ai_scrape)

    def run_sync(self, input_text: str) -> Response:
        """
        Run the agent synchronously. The input_text can be a search query or a URL.
        The agent will decide which tool to call based on the input.
        """
        result = self.agent.run_sync(input_text, deps=self.deps)
        return result.data

# ---------------------------
# Example Usage
# ---------------------------
if __name__ == "__main__":
    web_agent = WebAgent()

    # Example 1: Input is a search query
    query = "latest AI news"
    response = web_agent.run_sync(query)
    print("Response for search query:")
    print(response.json(indent=2))

    # Example 2: Input is a URL
    url = "https://example.com"
    response = web_agent.run_sync(url)
    print("\nResponse for URL scraping:")
    print(response.json(indent=2))