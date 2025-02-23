from app.agents.meta_agent import MetaAgent
import asyncio

async def main():
    meta_agent = await MetaAgent.create()

    query = input("Enter a query: ")

    response = await meta_agent.run(query)

    print("*** Model Response: ***")
    print(response.data.content)
    print("*** End of Model Response ***")

if __name__ == "__main__":
    asyncio.run(main())