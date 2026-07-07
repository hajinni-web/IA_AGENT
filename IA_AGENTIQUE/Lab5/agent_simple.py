from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain.agents import create_agent


@tool
def rag_search_opt(query: str) -> str:
    """
    Recherche des informations dans le texte.

    Args:
        query (str): Question de l'utilisateur.

    Returns:
        str: Contexte retrouvé.
    """

    results = (
        "Le personnage principal est un jeune homme nommé Jack, "
        "qui découvre un ancien artefact magique."
    )

    return results


# Initialisation du modèle LLM
llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)


# Création de l'agent
agent = create_agent(
    model=llm,
    tools=[rag_search_opt],
    system_prompt=(
        "Tu es un assistant spécialisé dans l'analyse de texte. "
        "Utilise toujours l'outil 'rag_search_opt' pour rechercher des "
        "informations dans le texte avant de répondre. "
        "Réponds de manière précise et cite uniquement les informations "
        "présentes dans le contexte."
    ),
)


# Exemple d'utilisation
question = HumanMessage(
    content="Qui est le personnage principal de l'histoire ?"
)

response = agent.invoke(
    {
        "messages": [question]
    }
)

print(response)