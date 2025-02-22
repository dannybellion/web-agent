from agent import WebAgent
import asyncio
def main():
    web_agent = WebAgent()

    query = input("Enter a query: ")

    response = asyncio.run(web_agent.run(query))

    print(response.data)
    

if __name__ == "__main__":
    main()