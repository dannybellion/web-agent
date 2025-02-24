from dataclasses import dataclass
from typing import List
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
import httpx
import logfire
import inspect
logfire.configure()

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
async def call_web_agent(ctx: RunContext, input_text: str):
    """Call the web agent with the given input text.

    Args:
        input_text (str): The input text to pass to the web agent.

    Returns:
        content (str): The content of the web agent's response.
    """
    url = ctx.deps.web_agent_url
    timeout = httpx.Timeout(20.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(
            f"{url}/run",
            json={"input_text": input_text}
        )
        response.raise_for_status()
        data = response.json()
        print("*** Web Agent Response: ***")
        print(data)
        print("*** End of Web Agent Response ***")
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

        self.agent.tool(call_web_agent)
        self.tool_docs = {
            "call_web_agent": inspect.getdoc(call_web_agent)
        }
        
    async def update_tool_docs(self):
        """
        Fetch up-to-date tool documentation from the remote web agent 
        and update the tool's docstring.
        """
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.deps.web_agent_url}/tool-docs")
            resp.raise_for_status()
            docs = resp.json()
            print("*** Tool Docs: ***")
            print(docs)
            print("*** End of Tool Docs ***")
            if "call_web_agent" in docs:
                call_web_agent.__doc__ = docs["call_web_agent"]
                self.tool_docs["call_web_agent"] = docs["call_web_agent"]
                
    @classmethod
    async def create(cls):
        """Async instance creation"""
        instance = cls()
        await instance.update_tool_docs()
        return instance

    async def run(self, input_text: str) -> Response:
        """
        Run the agent. The input_text can be a search query or a URL.
        The agent will decide which tool to call based on the input.
        """
        result = await self.agent.run(input_text, deps=self.deps)
        return result