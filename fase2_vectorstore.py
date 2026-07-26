import os
from typing import List

from fase1_ingestion import run_ingestion
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


def get_embedding_model() -> HuggingFaceEmbeddings:
    """Inicializa el modelo de embeddings multilingüe en CPU."""
    model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    return embeddings


def build_vectorstore(
    chunks: List[Document], 
    persist_directory: str = os.path.join("Chat", "chroma_db")
) -> Chroma:
    """Genera embeddings y los persiste en la base de datos vectorial ChromaDB."""
    embeddings = get_embedding_model()
    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name="utl_jc_docs"
    )
    print(f"Vectorstore indexado y almacenado en {persist_directory}.")
    return vectorstore


def run_vectorstore_phase() -> Chroma:
    """Ejecuta la ingesta e indexacion en ChromaDB."""
    chunks = run_ingestion()
    if not chunks:
        raise ValueError("No se obtuvieron chunks para la indexacion.")
    
    vectorstore = build_vectorstore(chunks)
    return vectorstore


if __name__ == "__main__":
    run_vectorstore_phase()
