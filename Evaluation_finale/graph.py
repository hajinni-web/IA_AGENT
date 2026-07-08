"""
graph.py
--------
Construction du graphe LangGraph 
"""

from langgraph.graph import StateGraph, START, END
from langchain_core.messages import SystemMessage
from langchain.messages import ToolMessage
from langchain_ollama import ChatOllama  # remplacer par ChatOpenAI/ChatAnthropic si besoin

from state import CreditAgentState
from prompts import SYSTEM_PROMPT
from tools import all_tools, tools_by_name
from langgraph.checkpoint.memory import InMemorySaver

memory = InMemorySaver()

# --- Modele LLM avec tools ---------------------------------------------
model = ChatOllama(model="llama3.2:3b", temperature=0)
model_with_tools = model.bind_tools(all_tools)


# --- Noeud "agent" : Le LLM décide s'il doit appeler un outil--------
def agent_node(state: CreditAgentState):
    """Le LLM lit le System Prompt + l'historique et decide (tool calling)
    s'il doit interroger le RAG interne, le web, ou lancer un calcul."""
    response = model_with_tools.invoke(
        [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    )
    return {
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }


# --- Noeud "tool_node" : Exécute les outils demandés par le LLM -----
def tool_node(state: CreditAgentState):
    last_message = state["messages"][-1]
    tool_messages = []
    new_sources = []
    for call in last_message.tool_calls:
        tool = tools_by_name[call["name"]]
        result = tool.invoke(call["args"])
        tool_messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))
        if call["name"] in ("search_credit_kb", "search_web"):
            new_sources.append(f"{call['name']}: {call['args'].get('query', '')}")
    return {
        "messages": tool_messages,
        "tool_calls_count": state.get("tool_calls_count", 0) + len(last_message.tool_calls),
        "retrieved_sources": new_sources,
    }


# --- Arete conditionnelle : continuer vers tool_node ou terminer -----------
def should_continue(state: CreditAgentState):
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "tool_node"
    return END


# --- Construction du graphe --------------------------------------------------
def build_graph():
    builder = StateGraph(CreditAgentState)
    builder.add_node("agent", agent_node)
    builder.add_node("tool_node", tool_node)

    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", should_continue, ["tool_node", END])
    builder.add_edge("tool_node", "agent")

    
    graph = builder.compile(checkpointer=memory)
    return graph


def save_graph_image(graph, path: str = "graph.png"):
    """Genere et sauvegarde la visualisation du graphe (draw_mermaid_png)."""
    try:
        png_bytes = graph.get_graph().draw_mermaid_png()
        with open(path, "wb") as f:
            f.write(png_bytes)
        print(f"[graph.py] Visualisation du graphe sauvegardee dans {path}")
    except Exception as e:
        print(f"[graph.py] Impossible de generer l'image du graphe : {e}")
