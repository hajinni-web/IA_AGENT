# CrediBot - Assistant Intelligent pour le Domaine du Crédit

## Description

CrediBot est un agent conversationnel intelligent développé avec **LangGraph**, **LangChain** et **RAG (Retrieval-Augmented Generation)**.

---

# Architecture du projet

```
Evaluation_finale/

│── app.py
│── evaluation.py
│── graph.py
│── state.py
│── tools.py
│── rag.py
│── prompts.py
│── memory.py
│── report.py
│── excel_report.py
│── requirements.txt
│── .env
│
├── documents/
│      credit_guide.pdf
│      banque.pdf
│      ...
│
└── graph.png
```

---

# Prérequis
Python 3.11 ou supérieur
Ollama
Modèle Llama 3.2
langchain
langchain-community
langchain-core
langchain-text-splitters
langchain-ollama
langgraph
sentence-transformers
tavily-python
pypdf

# Lancer l'application

```bash
python app.py
```

# Évaluer l'agent

```bash
python evaluation.py
```

L'évaluation génère automatiquement :

- Evaluation_CrediBot.xlsx

---

# Fonctionnalités

- Recherche documentaire (RAG)
- Recherche Web
- Calcul de mensualité
- Calcul du taux d'endettement
- Vérification d'éligibilité
- Mémoire conversationnelle
- Workflow LangGraph
- Génération automatique du graphe
- Génération d'un rapport Word
- Génération d'un rapport Excel

---

# Technologies utilisées

- Python
- LangGraph
- LangChain
- Ollama
- HuggingFace Embeddings
- Sentence Transformers
- Tavily API
- OpenPyXL
- Python-docx


Projet développé dans le cadre de la conception d'un agent IA utilisant l'approche **Agentic RAG** avec **LangGraph**.
