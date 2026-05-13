import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PERSIST_DIR = os.path.join(BASE_DIR, "data", "chroma_db")

def create_vector_store(chunks, persist_directory=PERSIST_DIR):
    embeddings = HuggingFaceEmbeddings(
        model_name = "all-MiniLM-L6-v2"
    )
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
    )
    print("Vector store created")
    return vector_store


def load_vector_store(persist_directory=PERSIST_DIR):
    """Load an already-persisted ChromaDB — skips PDF ingestion entirely."""
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    vector_store = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
    )
    print("Vector store loaded from disk")
    return vector_store


def get_or_create_vector_store(knowledge_base_path, persist_directory=PERSIST_DIR):
    """Load existing vector store if available, otherwise ingest PDFs and create it."""
    if os.path.exists(persist_directory) and os.listdir(persist_directory):
        return load_vector_store(persist_directory)
    else:
        from src.rag.data_ingestion import load_and_chunk_documents
        chunks = load_and_chunk_documents(knowledge_base_path)
        return create_vector_store(chunks, persist_directory)

