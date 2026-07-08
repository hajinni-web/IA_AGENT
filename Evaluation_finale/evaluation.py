"""
evaluation.py
-------------
Test de l'agent sur un ensemble de questions.
Mesure le temps de réponse.
"""

import time

from langchain.messages import HumanMessage
from excel_report import add_result, save_excel
from graph import build_graph


SIMPLE_QUESTIONS = [
    "Qu'est-ce qu'un crédit personnel ?",
    "Quelle est la différence entre un taux fixe et un taux variable ?",
    "Qu'est-ce qu'une garantie hypothécaire ?",
    "Combien de temps dure généralement un crédit immobilier ?",
    "Qu'est-ce que le taux d'endettement ?",
    "Qu'est-ce qu'une assurance emprunteur ?",
    "Quels documents sont nécessaires pour une demande de crédit ?",
    "Qu'est-ce qu'un tableau d'amortissement ?",
    "Quelle est la différence entre caution et hypothèque ?",
    "Qu'est-ce que le TAEG ?",
]

COMPLEX_QUESTIONS = [
    "Calcule la mensualité d'un crédit immobilier de 200000 sur 20 ans à 3.5%.",
    "Je gagne 3000 € par mois et j'ai déjà 400 € de crédits. Puis-je emprunter avec une mensualité de 600 € ?",
    "Quel est le taux directeur actuel de la banque centrale ?",
    "Compare un crédit à taux fixe et un crédit à taux variable.",
    "Je gagne 3 500 € par mois, j'ai 500 € de crédits en cours et je souhaite une mensualité de 900 €. Suis-je éligible à un crédit immobilier ?",
    "Quelles garanties sont demandées pour un crédit personnel ?",
    "Explique l'impact du taux directeur sur un crédit à taux variable.",
    "Calcule le taux d'endettement pour un revenu de 4500 €, des charges de 900 € et une mensualité de 700 €.",
    "Quelles sont les dernières réglementations sur le crédit à la consommation ?",
    "Quelle stratégie permet de réduire le coût total d'un crédit ?",
]


def evaluate(questions, title):

    agent = build_graph()

    config = {
        "configurable": {
            "thread_id": "evaluation"
        }
    }

    print(f"\n===== {title} =====")

    for i, question in enumerate(questions, 1):

        start = time.perf_counter()

        response = agent.invoke(
            {
                "messages": [
                    HumanMessage(content=question)
                ]
            },
            config=config
        )

        temps_reponse = time.perf_counter() - start

        answer = response["messages"][-1].content

        add_result(
            question=question,
            time=round(temps_reponse, 2),
            llm_calls=response.get("llm_calls", 0),
            tool_calls=response.get("tool_calls_count", 0),
            answer=answer
)

        print(f"\nQuestion {i}")
        print(question)
        print("\nRéponse :")
        print(answer)
        print(f"\nTemps : {temps_reponse:.2f} s")


if __name__ == "__main__":

    evaluate(SIMPLE_QUESTIONS, "Questions simples")

    evaluate(COMPLEX_QUESTIONS, "Questions complexes")

    save_excel()

    print("\nRapport enregistré : Evaluation_CrediBot.xlsx")