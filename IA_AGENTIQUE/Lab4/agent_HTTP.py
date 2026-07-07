import asyncio

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import InMemorySaver


# Charger les variables d'environnement (.env)
load_dotenv()


async def main():
    # Connexion au serveur MCP Kiwi
    client = MultiServerMCPClient(
        {
            "travel_server": {
                "transport": "streamable_http",
                "url": "https://mcp.kiwi.com",
            }
        }
    )

    # Récupération des outils exposés par le serveur MCP
    tools = await client.get_tools()

    # Création de l'agent
    agent = create_agent(
        model="gpt-5-nano",
        tools=tools,
        checkpointer=InMemorySaver(),
        system_prompt="You are a travel agent. No follow-up questions.",
    )

    # Configuration de la conversation
    config = {
        "configurable": {
            "thread_id": "1",
        }
    }

    # Question envoyée à l'agent
    response = await agent.ainvoke(
        {
            "messages": [
                HumanMessage(
                    content="Get me a direct flight from Rabat to Agadir on August 31st."
                )
            ]
        },
        config=config,
    )

    print(response)


if __name__ == "__main__":
    asyncio.run(main())