from app.agents.meta_agent import MetaAgent
import asyncio

def main():
    meta_agent = MetaAgent()

    query = input("Enter a query: ")

    response = asyncio.run(meta_agent.run(query))

    print("*** Model Response: ***")
    print(response.data.content)
    

if __name__ == "__main__":
    main()