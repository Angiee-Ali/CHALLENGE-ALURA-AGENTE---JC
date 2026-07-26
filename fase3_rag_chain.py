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
    
    return vectorstore


def get_llm():
    """Inicializa el modelo de lenguaje configurado."""
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


def create_flexible_prompt() -> ChatPromptTemplate:
    """Construye la plantilla de prompt con razonamiento semantico sobre el contexto disponible."""
    system_template = """Eres JC, el agente de Inteligencia Artificial oficial de atencion al estudiante de la Universidad Tecnologica de Lima (UTL).

Tu objetivo es responder las consultas de los estudiantes analizando y sintetizando la informacion contenida en el siguiente CONTEXTO extraido de los documentos oficiales.

====================== CONTEXTO DE LOS DOCUMENTOS ======================
{context}
========================================================================

DIRECTIVAS DE PROCESAMIENTO Y SINTESIS:
1. Analiza el contexto buscando conceptos equivalentes o relacionados. Si la pregunta consulta por "nota minima", "nota aprobatoria", "evaluaciones" o "calificaciones", responde con los requisitos de evaluacion o notas aprobatorias especificadas en el contexto (por ejemplo, la nota minima de 14 para aprobar evaluaciones).
2. Construye una respuesta util, clara, profesional y directa basada en los datos encontrados en el contexto.
3. AL FINAL DE TU RESPUESTA, CITA SIEMPRE la fuente indicando el nombre del archivo PDF y la pagina (ejemplo: Fuente: preguntas_frecuentes_cursos_certificados.pdf | Pagina: 2).
4. UNICAMENTE si el contexto proporcionado no guarda ninguna relacion o equivalencia con el tema consultado, responde EXACTAMENTE:
"No encontré esta información en los documentos."

Pregunta del Estudiante: {question}

Respuesta de JC:"""

    return ChatPromptTemplate.from_template(system_template)


def format_documents(docs: List[Any]) -> str:
    """Formatea los documentos recuperados formateando metadatos de origen."""
    if not docs:
        return "SIN_CONTEXTO_RECUPERADO"
        
    formatted_blocks = []
    for doc in docs:
        source = doc.metadata.get("source", "desconocido")
        page = doc.metadata.get("page", 1)
        block = f"[Fuente: {source} | Pagina: {page}]\n{doc.page_content}"
        formatted_blocks.append(block)
        
    return "\n\n---\n\n".join(formatted_blocks)


def build_rag_chain():
    """Ensambla la cadena RAG con un recuperador ampliado (k=6) y prompt con sintesis semantica."""
    vectorstore = load_vectorstore()
    
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 6}
    )
    
    llm = get_llm()
    prompt = create_flexible_prompt()
    
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


construir_cadena_rag = build_rag_chain


def run_rag_validation():
    """Valida la ejecucion de la cadena RAG refactorizada."""
    chain = build_rag_chain()
    
    test_queries = [
        "¿Cuál es la nota mínima?",
        "¿Cuáles son las calificaciones aprobatorias?"
    ]
    
    print("--- VALIDACION DE CADENA RAG REFACTORIZADA (NIVEL 3) ---")
    for query in test_queries:
        print(f"\nConsulta: {query}")
        response = chain.invoke(query)
        print(f"Respuesta JC:\n{response}")
        print("-" * 50)


if __name__ == "__main__":
    run_rag_validation()
