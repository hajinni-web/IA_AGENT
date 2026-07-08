# AI Agentic Labs — Master BDCC

Ce dépôt regroupe l'ensemble des laboratoires (Labs) et du projet (TP) réalisés dans le cadre du module **Systèmes Multi-Agents (SMA)** et **Intelligence Artificielle Distribuée (IAD)** du **Master BDCC**.

## Repository Structure

| Folder | Description |
|---------|-------------|
| Lab1-prompt-engineering | Prompt engineering: tokenization, Ollama, Groq, OpenAI APIs, structured JSON outputs, image generation |
| Lab2-langchain-agents | LangChain agents with memory, web search and personal assistant examples |
| Lab3-RAG | Retrieval-Augmented Generation (RAG) using PDF documents and SQL Agent with Chinook database |
| Lab4-MCP | Model Context Protocol (MCP): stdio servers, time server and HTTP streaming |
| Lab5-LangGraph_Studio | LangGraph Studio for visualization, debugging and hierarchical multi-agent systems |
| Lab6-Contexte_et_Etat | Context management with invocation profiles and persistent application state |
| Lab7-Human_In_The_Loop | Human-in-the-Loop workflows using interrupts, approval, rejection and editing |
| Lab8-Workflow_avec_LangGraph | LangGraph workflows including reducers, conditional routing, loops and message state |
| Lab9-Agent_avec_LangGraph | Complete LangGraph agent with tools, entrypoints, tasks, conversation history and branching |
| TP-Chef_personnel | AI cooking assistant combining RAG, memory, web search and system prompts |

---

## Requirements

- Python 3.10+
- uv package manager
- Ollama

Download the required local model:

```bash
ollama pull llama3.2:3b
```

---

## Technologies

- Python
- LangChain
- LangGraph
- MCP
- Ollama
- OpenAI
- Groq
- HuggingFace
