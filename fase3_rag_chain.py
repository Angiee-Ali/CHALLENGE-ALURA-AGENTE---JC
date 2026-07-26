import os
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


def load_vectorstore() -> Chroma:
    """Carga la base de datos vectorial local desde Chat/chroma_db."""
    persist_directory = os.path.join("Chat", "chroma_db")
    
    if not os.path.exists(persist_directory):
        raise FileNotFoundError(f"Base de datos vectorial no encontrada en {persist_directory}")
    
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    
    return Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
        collection_name="utl_jc_docs"
    )


def get_llm():
    """Inicializa el modelo de lenguaje configurado en las variables de entorno."""
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
        raise ValueError("Clave API de LLM no configurada en el archivo .env")


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


def format_documents(docs: List[Any]) -> str:
    """Formatea los documentos recuperados incluyendo metadatos de fuente y pagina."""
    formatted_blocks = []
    for doc in docs:
        source = doc.metadata.get("source", "desconocido")
        page = doc.metadata.get("page", 1)
        block = f"[Fuente: {source} | Pagina: {page}]\n{doc.page_content}"
        formatted_blocks.append(block)
    return "\n\n---\n\n".join(formatted_blocks)


def build_rag_chain():
    """Ensambla el flujo RAG de recuperacion y generacion."""
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = get_llm()
    prompt = create_strict_prompt()
    
    rag_chain = (
        {
            "context": retriever | format_documents,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain


# Alias de retrocompatibilidad
construir_cadena_rag = build_rag_chain


def run_rag_validation():
    """Valida la ejecucion de la cadena RAG con consultas de prueba."""
    chain = build_rag_chain()
    
    test_queries = [
        "¿Cuál es la nota mínima aprobatoria y cómo se evalúa?",
        "¿Hasta cuántos días antes del inicio puedo pedir el 100% de reembolso de mi matrícula?",
        "¿Quién es el presidente de Francia?"
    ]
    
    print("--- VALIDACION DE CADENA RAG (AGENTE JC) ---")
    for query in test_queries:
        print(f"\nConsulta: {query}")
        response = chain.invoke(query)
        print(f"Respuesta JC:\n{response}")
        print("-" * 50)


if __name__ == "__main__":
    run_rag_validation()
