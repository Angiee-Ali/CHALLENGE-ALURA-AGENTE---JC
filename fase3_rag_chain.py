import os
import sys
from typing import List, Any
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from fase1_ingestion import run_ingestion
from fase2_vectorstore import build_vectorstore


def get_embedding_model() -> HuggingFaceEmbeddings:
    """Inicializa el modelo de embeddings multilingüe."""
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )


def load_vectorstore() -> Chroma:
    """Carga o indexa automaticamente la base de datos vectorial local."""
    persist_directory = os.path.join("Chat", "chroma_db")
    embeddings = get_embedding_model()
    
    # Auto-indexacion si el directorio no existe o esta vacio
    if not os.path.exists(persist_directory) or not os.listdir(persist_directory):
        print("ADVERTENCIA: Base de datos vectorial no encontrada. Iniciando indexacion automatica...")
        chunks = run_ingestion()
        if not chunks:
            raise ValueError("Error critico: No se pudieron extraer chunks de los documentos PDF.")
        return build_vectorstore(chunks, persist_directory=persist_directory)
    
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
        collection_name="utl_jc_docs"
    )
    
    # Validacion del numero de documentos indexados
    doc_count = vectorstore._collection.count()
    print(f"DEBUG: Vectorstore cargado exitosamente. Total de elementos indexados: {doc_count}")
    if doc_count == 0:
        print("ADVERTENCIA: Vectorstore vacio. Re-indexando documentos...")
        chunks = run_ingestion()
        return build_vectorstore(chunks, persist_directory=persist_directory)
        
    return vectorstore


def get_llm():
    """Inicializa la instancia del modelo de lenguaje."""
    api_key_groq = os.getenv("GROQ_API_KEY")
    api_key_openai = os.getenv("OPENAI_API_KEY")
    
    if api_key_groq:
        from langchain_groq import ChatGroq
        return ChatGroq(
            model_name="llama-3.1-8b-instant",
            temperature=0.0,
            api_key=api_key_groq
        )
    elif api_key_openai:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0.0,
            api_key=api_key_openai
        )
    else:
        raise ValueError("Clave API de LLM no configurada en las variables de entorno.")


def create_strict_prompt() -> ChatPromptTemplate:
    """Construye la plantilla de prompt con restricciones estrictas de contexto."""
    system_template = """Eres JC, el agente de Inteligencia Artificial oficial de atencion al estudiante de la Universidad Tecnologica de Lima (UTL).

Tu mision es responder las dudas de los estudiantes basandote UNICAMENTE en el siguiente contexto extraido de los documentos PDF oficiales.

====================== CONTEXTO DE LOS DOCUMENTOS ======================
{context}
========================================================================

REGLAS OBLIGATORIAS:
1. Responde en un tono profesional, claro y directo en idioma español.
2. Basate UNICAMENTE en la informacion explicita del CONTEXTO proporcionado. No asumas ni inventes datos.
3. Al final de tu respuesta, DEBES CITAR la fuente indicando el nombre del archivo PDF y la pagina (ejemplo: Fuente: reglamento_estudiante.pdf | Pagina: 2).
4. Si la respuesta a la pregunta del estudiante NO se encuentra explicitamente en el contexto proporcionado, responde EXACTAMENTE:
"No encontré esta información en los documentos."

Pregunta del Estudiante: {question}

Respuesta de JC:"""

    return ChatPromptTemplate.from_template(system_template)


def format_documents_with_debug(docs: List[Any]) -> str:
    """Formatea los documentos recuperados e imprime diagnósticos en stdout."""
    print(f"\nDEBUG RETRIEVER: Cantidad de chunks recuperados = {len(docs)}")
    if not docs:
        print("ERROR RETRIEVER: El buscador retorno una lista vacia [] para la consulta.")
        return "SIN_CONTEXTO_RECUPERADO"
        
    formatted_blocks = []
    for idx, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "desconocido")
        page = doc.metadata.get("page", 1)
        print(f"  Chunk #{idx} -> Fuente: {source} | Pagina: {page} | Longitud: {len(doc.page_content)} caracteres")
        block = f"[Fuente: {source} | Pagina: {page}]\n{doc.page_content}"
        formatted_blocks.append(block)
        
    return "\n\n---\n\n".join(formatted_blocks)


def build_rag_chain():
    """Ensambla la cadena RAG con busqueda global por similitud semantica."""
    vectorstore = load_vectorstore()
    
    # Busqueda global sobre los 5 PDFs
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )
    
    llm = get_llm()
    prompt = create_strict_prompt()
    
    rag_chain = (
        {
            "context": retriever | format_documents_with_debug,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain


construir_cadena_rag = build_rag_chain


def run_rag_validation():
    """Ejecuta una prueba de depuracion de la cadena RAG."""
    chain = build_rag_chain()
    test_query = "¿Cuál es la nota mínima aprobatoria y cómo se evalúa?"
    print(f"\n--- PRUEBA DE DEPURACION: '{test_query}' ---")
    response = chain.invoke(test_query)
    print(f"\nRespuesta LLM:\n{response}\n")


if __name__ == "__main__":
    run_rag_validation()
