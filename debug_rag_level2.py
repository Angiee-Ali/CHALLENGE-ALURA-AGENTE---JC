import os
from pathlib import Path
from fase1_ingestion import load_documents
from fase3_rag_chain import load_vectorstore


def audit_pdf_ingestion(output_file: str = "debug_raw_text.txt") -> str:
    """Extrae el texto completo de los 5 PDFs y lo guarda en un archivo plano para inspeccion."""
    documents = load_documents()
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("=== AUDITORIA DE EXTRACCION DE TEXTO (PDF RAW TEXT) ===\n\n")
        for doc in documents:
            source = doc.metadata.get("source", "desconocido")
            page = doc.metadata.get("page", 1)
            f.write(f"--- ARCHIVO: {source} | PAGINA: {page} ---\n")
            f.write(f"{doc.page_content}\n\n")
            
    print(f"Auditoria de Ingestion finalizada. Texto guardado en: {output_file}")
    return output_file


def audit_retriever_scores(queries: list = None):
    """Ejecuta una busqueda por similitud con scores directamente en ChromaDB omitiendo el LLM."""
    if queries is None:
        queries = [
            "Cuál es la nota mínima",
            "calificación aprobatoria",
            "nota mínima aprobatoria",
            "asistencia mínima"
        ]
        
    vectorstore = load_vectorstore()
    
    print("\n=== AUDITORIA DEL RETRIEVER (SIMILARITY SEARCH WITH SCORE) ===")
    for query in queries:
        print(f"\n[QUERY]: '{query}'")
        results = vectorstore.similarity_search_with_score(query, k=4)
        
        if not results:
            print("  [ERROR]: El retriever retorno una lista vacia [].")
            continue
            
        for idx, (doc, score) in enumerate(results, start=1):
            source = doc.metadata.get("source", "desconocido")
            page = doc.metadata.get("page", 1)
            print(f"  Resultado #{idx} | Score (Distancia): {score:.4f} | Fuente: {source} (Pagina {page})")
            print(f"  Contenido Chunk:\n  {doc.page_content[:200]}...\n")


if __name__ == "__main__":
    audit_pdf_ingestion()
    audit_retriever_scores()
