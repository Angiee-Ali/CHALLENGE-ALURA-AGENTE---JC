import os
import re
from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def clean_text(text: str) -> str:
    """Normaliza secuencias de saltos de linea y espacios en blanco continuos."""
    if not text:
        return ""
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()


def load_documents(docs_directory: str = os.path.join("Chat", "Documentos")) -> List[Document]:
    """Carga y limpia documentos PDF desde el directorio especificado."""
    docs_path = Path(docs_directory)
    
    if not docs_path.exists():
        raise FileNotFoundError(f"Directorio no encontrado: {docs_directory}")
    
    pdf_files = list(docs_path.glob("*.pdf"))
    if not pdf_files:
        print(f"No se encontraron archivos PDF en {docs_directory}")
        return []
    
    loaded_documents: List[Document] = []
    
    for pdf_path in pdf_files:
        try:
            loader = PyPDFLoader(str(pdf_path))
            pages = loader.load()
            
            for page in pages:
                page.page_content = clean_text(page.page_content)
                page.metadata["source"] = pdf_path.name
                page.metadata["page"] = int(page.metadata.get("page", 0)) + 1
                loaded_documents.append(page)
        except Exception as e:
            print(f"Error al procesar el archivo {pdf_path.name}: {e}")
            
    print(f"Archivos procesados: {len(pdf_files)} | Paginas extraidas: {len(loaded_documents)}")
    return loaded_documents


def split_documents(
    documents: List[Document], 
    chunk_size: int = 1000, 
    chunk_overlap: int = 200
) -> List[Document]:
    """Segmenta los documentos en bloques de texto preservando la coherencia semantica."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = splitter.split_documents(documents)
    print(f"Segmentacion finalizada: {len(chunks)} chunks generados (size={chunk_size}, overlap={chunk_overlap}).")
    return chunks


def run_ingestion(docs_directory: str = os.path.join("Chat", "Documentos")) -> List[Document]:
    """Ejecuta el flujo completo de ingesta, limpieza y fragmentacion."""
    documents = load_documents(docs_directory)
    if not documents:
        return []
    
    chunks = split_documents(documents)
    return chunks


if __name__ == "__main__":
    run_ingestion()
