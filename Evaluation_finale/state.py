"""
state.py
--------
Etat personnalise de l'agent de credit bancaire.

"""

from operator import add
from typing import List
from typing_extensions import TypedDict, Annotated
from langchain_core.messages import AnyMessage


class CreditAgentState(TypedDict):
    # Historique complet de la conversation. Reducer "add" -> concatenation automatique
    messages: Annotated[List[AnyMessage], add]

    # Compteurs utiles pour le monitoring et l'evaluation du systeme
    llm_calls: int
    tool_calls_count: int

    # Trace cumulee des sources utilisees (RAG interne ou Web) sur tout le fil
    # de discussion. Reducer "add" -> on garde l'historique complet des sources.
    retrieved_sources: Annotated[List[str], add]
