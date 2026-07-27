# Agente Inteligente RAG "JC" - Universidad Tecnologica de Lima (UTL)

Proyecto final desarrollado como estudiante de ingenieria de software para la Universidad Tecnologica de Lima (UTL). El sistema implementa una arquitectura RAG (Retrieval-Augmented Generation) para responder consultas academicas y administrativas de los estudiantes basandose exclusivamente en la documentacion oficial en formato PDF, garantizando respuestas fundamentadas y libres de alucinaciones.

---

## 1. Resumen Tecnico y Arquitectura

El Agente JC opera mediante un pipeline desacoplado en cinco fases principales (Ingestion, Vectorstore, Rag_chain, Interfaz/Registro y Deploy):

```text
[PDFs Oficiales UTL] -> (PyPDFLoader) -> (Limpieza & Chunking)
                                                |
                                                v
[Interfaz Streamlit] <- (LLM Llama-3.1) <- (Prompt Estricto) <- (ChromaDB Vectorstore)
```

1. **Ingestion**: Extrae y limpia el texto de 5 documentos PDF oficiales omitiendo portadas o encabezados ruidosos.
2. **Vectorstore**: Indexa semanticamente los fragmentos utilizando embeddings multilingües en una base de datos vectorial local (ChromaDB).
3. **Rag_chain**: Ejecuta una busqueda por similitud (k=6) y construye el contexto que es procesado por un LLM (Llama 3.1 8B via Groq API) sujeto a un prompt de sistema estricto con citacion obligatoria de fuente (archivo PDF y pagina).
4. **Interfaz y Registro**: Expone una interfaz web interactiva en Streamlit con descarga directa de documentos PDF y registro de auditoria en formato JSON.
5. **Deploy**: Preparado para ejecucion continua en Streamlit Community Cloud o contenerizacion mediante Docker en Oracle Cloud Infrastructure (OCI).

---

## 2. Stack Tecnologico

- **Lenguaje de Programacion**: Python 3.10+
- **Orquestador RAG**: LangChain Core / LangChain Community / LCEL
- **Procesamiento Documental**: PyPDFLoader & RecursiveCharacterTextSplitter
- **Base de Datos Vectorial**: ChromaDB
- **Modelo de Embeddings**: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (HuggingFace)
- **Modelo de Lenguaje (LLM)**: Meta Llama 3.1 8B Instant (vía Groq API) / OpenAI GPT-4o-mini
- **Interfaz de Usuario**: Streamlit
- **Contenerizacion y Despliegue**: Docker / Streamlit Community Cloud / OCI

---

## 3. Evidencias de Funcionamiento

### Aplicativo en Produccion
- **URL Publica**: [https://alura-agente---jc.streamlit.app/](https://alura-agente---jc.streamlit.app/)
- **Repositorio Oficial**: [https://github.com/Angiee-Ali/CHALLENGE-ALURA-AGENTE---JC.git](https://github.com/Angiee-Ali/CHALLENGE-ALURA-AGENTE---JC.git)

### Capturas de Pantalla de la Interfaz

![Demostracion de la Interfaz del Chat](assets/interfaz_chat.png)

![Descarga de Documentos Oficiales en Panel Lateral](assets/descarga_documentos.png)

---

## 4. Guia de Instalacion y Ejecucion Local

### Requisitos Previos
- Python 3.10 o superior instalado en el sistema.
- Clave API de Groq Cloud (gratuita en https://console.groq.com) o clave de OpenAI.

### Paso 1: Clonar el Repositorio
```bash
git clone https://github.com/Angiee-Ali/CHALLENGE-ALURA-AGENTE---JC.git
cd CHALLENGE-ALURA-AGENTE---JC
```

### Paso 2: Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Paso 3: Configurar Variables de Entorno
Crear un archivo `.env` en la raiz del proyecto con la siguiente estructura:
```env
GROQ_API_KEY=tu_clave_api_aqui
```

### Paso 4: Ejecutar Pipeline e Iniciar Servidor Local
```bash
python fase1_ingestion.py
python fase2_vectorstore.py
streamlit run app.py
```
Acceder en el navegador a `http://localhost:8501`.

---

## 5. Instrucciones de Despliegue (Deploy)

### Opcion A: Streamlit Community Cloud (Recomendado)
1. Conectar el repositorio de GitHub en [share.streamlit.io](https://share.streamlit.io).
2. Seleccionar la rama `main` y la ruta del archivo principal `app.py`.
3. En **Advanced settings ➔ Secrets**, configurar la clave API:
   ```toml
   GROQ_API_KEY = "tu_clave_api_aqui"
   ```
4. Desplegar la aplicacion.

### Opcion B: Contenerizacion con Docker para OCI (Oracle Cloud Infrastructure)
1. Construir la imagen Docker:
   ```bash
   docker build -t chatbot-jc:v1 .
   ```
2. Ejecutar el contenedor pasando la variable de entorno:
   ```bash
   docker run -d -p 8501:8501 -e GROQ_API_KEY="tu_clave_api_aqui" --restart always chatbot-jc:v1
   ```
