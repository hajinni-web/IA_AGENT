"""
rag.py
------
Construction de la base documentaire (RAG) pour le domaine du credit bancaire.

Pipeline repris du TP RAG :
1. Chargement des PDF avec PyPDFLoader
2. Decoupage avec RecursiveCharacterTextSplitter
3. Embeddings avec HuggingFaceEmbeddings (sentence-transformers/all-MiniLM-L6-v2)
4. Stockage dans un InMemoryVectorStore
5. Recherche semantique avec estimation de pertinence (pour decider d'un web search)
"""

import os
import glob
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

DOCS_DIR = os.path.join(os.path.dirname(__file__), "documents")


def load_pdfs(docs_dir: str = DOCS_DIR):
    """Charge tous les PDF du dossier documents/ avec PyPDFLoader."""
    all_docs = []
    pdf_paths = glob.glob(os.path.join(docs_dir, "*.pdf"))
    if not pdf_paths:
        print(f"[rag.py] Aucun PDF trouve dans {docs_dir}. Deposez-y vos "
              f"documents (conditions generales de credit, grilles de taux, "
              f"guides immobiliers, reglementation bancaire...).")
    for path in pdf_paths:
        loader = PyPDFLoader(path)
        docs = loader.load()
        all_docs.extend(docs)
        print(f"[rag.py] {os.path.basename(path)} charge ({len(docs)} pages)")
    return all_docs


def split_documents(documents, chunk_size: int = 1000, chunk_overlap: int = 200):
    """Decoupe les documents en chunks avec chevauchement."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True,
    )
    return splitter.split_documents(documents)


def build_vector_store(chunks):
    """Genere les embeddings et construit le vector store en memoire."""
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vector_store = InMemoryVectorStore(embeddings)
    if chunks:
        vector_store.add_documents(documents=chunks)
    return vector_store


def get_credit_vector_store():
    """Point d'entree unique : charge, decoupe et indexe la base documentaire."""
    documents = load_pdfs()
    chunks = split_documents(documents)
    vector_store = build_vector_store(chunks)
    print(f"[rag.py] Base vectorielle prete : {len(chunks)} chunks indexes.")
    return vector_store


def search_with_relevance(vector_store, query: str, k: int = 3, score_threshold: float = 0.55):
    """
    Recherche semantique renvoyant les documents ET un booleen 'sufficient'.
    Le score depend de la metrique de l'embedding utilise : ajustez
    score_threshold apres quelques tests sur votre propre corpus.
    """
    results = vector_store.similarity_search_with_score(query, k=k)
    sufficient = any(score >= score_threshold for _, score in results) if results else False
    return results, sufficient
