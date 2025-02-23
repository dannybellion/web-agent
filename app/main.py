from app.agents.meta_agent import MetaAgent
import asyncio
import logfire
logfire.configure()

def main():
    meta_agent = MetaAgent()

    query = input("Enter a query: ")

    response = asyncio.run(meta_agent.run(query))

    print(response.data)
    

if __name__ == "__main__":
    main()