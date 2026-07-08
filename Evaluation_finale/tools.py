"""
tools.py
--------
Outils (Tools) de l'agent CreditBot. Les docstrings sont lues par le LLM
pour decider quand et comment appeler chaque outil
"""

from langchain.tools import tool
from rag import get_credit_vector_store, search_with_relevance
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()
tavily_client = TavilyClient()


# Base vectorielle construite une seule fois au chargement du module
_vector_store = get_credit_vector_store()


# --- Tool 1 : RAG interne ---------------------------------------------------
@tool
def search_credit_kb(query: str) -> str:
    """Recherche dans la base documentaire interne (PDF) sur le credit bancaire
    (credit personnel, immobilier, taux, garanties, remboursement, eligibilite).
    A utiliser TOUJOURS en priorite avant toute recherche web."""
    results, sufficient = search_with_relevance(_vector_store, query)
    if not results:
        return "AUCUN_RESULTAT: la base documentaire ne contient aucune information pertinente."
    content = "\n---\n".join(doc.page_content for doc, _ in results)
    flag = "SUFFISANT" if sufficient else "INSUFFISANT"
    return f"[{flag}]\n{content}"


# --- Tool 2 : Recherche Web (Tavily) ----------------------------------------
@tool
def search_web(query: str) -> str:
    """Recherche des informations a jour sur le web"""
    results = tavily_client.search(query)
    return str(results)


# --- Tool 3 : Calcul de mensualite -------------------------------------------
@tool
def calculate_monthly_payment(principal: float, annual_rate_percent: float, years: int) -> str:
    """Calcule la mensualite d'un pret (credit personnel ou immobilier) a taux
    fixe, a partir du capital emprunte, du taux annuel en pourcentage et de la
    duree en annees. Utiliser cet outil pour tout calcul de mensualite."""
    monthly_rate = (annual_rate_percent / 100) / 12
    n = years * 12
    if n <= 0:
        return "Erreur: la duree doit etre superieure a 0."
    if monthly_rate == 0:
        payment = principal / n
    else:
        payment = principal * monthly_rate / (1 - (1 + monthly_rate) ** (-n))
    total_cost = payment * n
    return (f"Mensualite estimee : {payment:.2f} sur {n} mois. "
            f"Cout total du credit : {total_cost:.2f}, dont "
            f"{total_cost - principal:.2f} d'interets.")


# --- Tool 4 : Verification d'eligibilite (taux d'endettement) --------------
@tool
def check_eligibility(monthly_income: float, existing_monthly_debt: float,
                       requested_monthly_payment: float) -> str:
    """Verifie l'eligibilite a un credit en calculant le taux d'endettement
    (regle des 33%) a partir du revenu mensuel, des charges de credit
    existantes et de la mensualite demandee pour le nouveau credit."""
    total_debt = existing_monthly_debt + requested_monthly_payment
    debt_ratio = (total_debt / monthly_income) * 100 if monthly_income else 100
    eligible = debt_ratio <= 33
    verdict = "ELIGIBLE" if eligible else "NON ELIGIBLE (risque de surendettement)"
    return f"Taux d'endettement estime : {debt_ratio:.1f}%. Verdict : {verdict} (seuil usuel : 33%)."


all_tools = [search_credit_kb, search_web, calculate_monthly_payment, check_eligibility]
tools_by_name = {t.name: t for t in all_tools}
