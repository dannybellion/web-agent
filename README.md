# Web Agent Project

This project implements a multi-agent system base on [pydantic-ai](https://ai.pydantic.dev) to assist with web-related tasks using asynchronous operations in Python. The system consists of two primary agents:
- **Meta Agent**: Orchestrates tasks and decides which tool to call based on input queries.
- **Web Agent**: Handles web scraping and search functionalities via external services and libraries.

## Features

- **Asynchronous Processing**: Leverages async capabilities with `httpx`, `uvicorn`, and `FastAPI` to handle concurrent requests.
- **Pydantic-based Agents**: Uses Pydantic for data validation and type enforcement in agent interactions.
- **Dynamic Tool Documentation**: Automatically updates tool documentation by retrieving it from the Web Agent.
- **Web Scraping and Search**: Integrates with Crawl4AI for scraping and simulates web search using Tavily.

## Project Structure

- **app/main.py**: The main entry point for running the Meta Agent.
- **app/agents/meta_agent.py**: Implements the Meta Agent that coordinates between various tools.
- **app/agents/web_agent.py**: Implements the Web Agent as a FastAPI application, providing endpoints for running the agent and retrieving tool documentation.

## Setup

1. **Clone the Repository**  
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set up environment**  
   Project is configured to run with UV:
   ```bash
   uv sync
   ```

3. **Configure Environment Variables**  
   The Web Agent requires the following environment variable:
   - `TAVILY_API_KEY`: Your API key for the Tavily search service.
   - `GEMINI_API_KEY`: Your API key for the Gemini search service.

4. **Run the Web Agent**  
   Start the Web Agent API using:
   ```bash
   uv run fastapi dev app/agents/web_agent.py
   ```

5. **Run the Meta Agent**  
   In another terminal, run:
   ```bash
   uv run -m app.main
   ```

## Usage

- **Meta Agent**: When you run `app/main.py`, you will be prompted to enter a query. The 
Meta Agent processes your input and decides whether to perform a web search or scrape a 
URL using the Web Agent.
- **Web Agent API**: The Web Agent listens on port 8000 by default, handling web scraping 
and search requests as well as providing dynamic documentation via the `/tool-docs` 
endpoint.

## Libraries

- [Pydantic](https://pydantic-docs.helpmanual.io/) for robust data validation.
- [Pydantic-AI](https://ai.pydantic.dev) for building agents.
- [Logfire](https://logfire.pydantic.dev/docs/) for logging and monitoring.
- [FastAPI](https://fastapi.tiangolo.com/) for providing a modern, high-performance web 
framework.
- [UV](https://docs.astral.sh/uv/getting-started/installation/) for dependency management.