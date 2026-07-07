#Intégration d’un serveur MCP local
#MCP local server via stdio
import asyncio
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_ollama import ChatOllama


async def main():
    client = MultiServerMCPClient(
        {
        "local_server": {
        "transport": "stdio",
        "command": "python",
        "args": ["../resources/mcp_local_server.py"],}})

#Récupération dynamique des tools

# get tools
    tools = await client.get_tools()

#Resources MCP
# get resources
    resources = await client.get_resources("local_server")

#Prompt dynamique côté serveur MCP

# get prompts
    prompt = await client.get_prompt("local_server", "prompt")
    prompt = prompt[0].content


#Agent LLM modulaire avec serveur MCP 
# Initialiser le modèle Ollama
    model = ChatOllama(
    model="llama3.2:3b", # ou mistral, gemma, etc.
    temperature=0)
    agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=prompt)
    config = {"configurable": {"thread_id": "1"}}
    response = await agent.ainvoke(
    {"messages": [HumanMessage(content="Tell me about the langchain-mcp-adapt-ers library")]},
    config=config)
    print(response)

asyncio.run(main())