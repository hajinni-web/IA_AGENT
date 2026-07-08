"""
Construit le graphe LangGraph et lance une conversation avec l'utilisateur.
"""

from langchain.messages import HumanMessage
from graph import build_graph, save_graph_image
from report import add_conversation, save_report


def main():
    # Construire le graphe
    agent = build_graph()

    # Générer une image du workflow
    save_graph_image(agent)

    # Configuration de la mémoire (identifiant de la conversation)
    config = {
        "configurable": {
            "thread_id": "1"
        }
    }

    print("======================================")
    print("      CreditBot - Assistant Crédit")
    print("======================================")
    print("Tapez 'exit' pour quitter.\n")

    while True:
        question = input("Vous : ")

        if question.lower() in ["exit", "quit"]:
            save_report()
            print("Rapport enregistré : CrediBot_Report.docx")
            print("Fin de la conversation.")
            break

        response = agent.invoke(
            {
                "messages": [
                    HumanMessage(content=question)
                ]
            },
            config=config
        )

        answer = response["messages"][-1].content

        print(f"\nCreditBot : {answer}\n")

        # Enregistrer la conversation dans le rapport
        add_conversation(question, answer)


if __name__ == "__main__":
    main()