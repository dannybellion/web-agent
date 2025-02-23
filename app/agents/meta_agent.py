from dataclasses import dataclass
from typing import List
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
import httpx
import os

# ---------------------------
# Pydantic Agent Configuration
# ---------------------------
MODEL = "gemini-2.0-flash"
SYSTEM_PROMPT = """
You are a helpful assistant
"""

# ---------------------------
# Pydantic Response Models
# ---------------------------
class Response(BaseModel):
    content: str = Field(..., description="A summary of the search results")

# ---------------------------
# Dependencies
# ---------------------------
@dataclass
class MetaAgentDeps:
    web_agent_url: str = "http://127.0.0.1:8000"
    pass

# ---------------------------
# Tools
# ---------------------------
async def call_web_agent(self, ctx: RunContext, input_text: str):
    url = ctx.deps.web_agent_url
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{url}/run",
            json={"input_text": input_text}
        )
        response.raise_for_status()
        data = response.json()
        return data


# ---------------------------   
# Single WebAgent Class
# ---------------------------
class MetaAgent:
    def __init__(self):
        self.deps = MetaAgentDeps()
        self.agent = Agent(
            model=MODEL,
            deps_type=MetaAgentDeps,
            result_type=Response,
            system_prompt=SYSTEM_PROMPT,
        )
        # Register both tools.
        self.agent.tool(call_web_agent)

    async def run(self, input_text: str) -> Response:
        """
        Run the agent. The input_text can be a search query or a URL.
        The agent will decide which tool to call based on the input.
        """
        result = await self.agent.run(input_text, deps=self.deps)
        return result