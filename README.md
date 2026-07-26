# Agente Inteligente RAG "JC" - Universidad Tecnologica de Lima (UTL)
### Arquitectura RAG con LangChain, ChromaDB, Streamlit y Despliegue en OCI

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![LangChain](https://img.shields.io/badge/Framework-LangChain-emerald?logo=chainlink)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red?logo=streamlit)
![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-purple)
![Oracle Cloud](https://img.shields.io/badge/Cloud-Oracle%20Cloud%20(OCI)-orange?logo=oracle)
![Docker](https://img.shields.io/badge/Container-Docker-blue?logo=docker)

JC es un agente virtual basado en Arquitectura RAG (Retrieval-Augmented Generation) desarrollado para la Universidad Tecnologica de Lima (UTL). Su objetivo es responder consultas de estudiantes basandose exclusivamente en la documentacion oficial en formato PDF, garantizando respuestas precisas y evitando la generacion de informacion no fundamentada.

---

## Repositorio del Proyecto
- Repositorio GitHub: [CHALLENGE-ALURA-AGENTE---JC](https://github.com/Angiee-Ali/CHALLENGE-ALURA-AGENTE---JC.git)
- Ruta de Desarrollo: `C:\Users\USER\Desktop\Oracle One\Agente IA`

---

## Arquitectura del Sistema RAG

```text
[PDFs Oficiales UTL] --> (PyPDFLoader) --> (Limpieza y Chunking)
                                                  |
                                                  v
[Respuesta Streamlit] <-- (LLM Llama-3.1) <-- (Prompt Estricto) <-- (ChromaDB Vectorstore)
```

---

## Fases Tecnicas de Implementacion

### Fase A: Ingestion (`fase1_ingestion.py`)
- Lectura estructurada de 5 PDFs oficiales mediante PyPDFLoader.
- Normalizacion del contenido mediante expresiones regulares.
- Fragmentacion con `RecursiveCharacterTextSplitter` (chunk_size=1000, chunk_overlap=200).
- Preservacion de metadatos de fuente y numero de pagina.

### Fase B: Vectorstore (`fase2_vectorstore.py`)
- Generacion de embeddings multilingües mediante `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`.
- Persistencia e indexacion vectorial en ChromaDB en el directorio `Chat/chroma_db`.

### Fase C: Rag_chain (`fase3_rag_chain.py`)
- Integracion del LLM (Llama 3.1 8B en Groq u OpenAI).
- Implementacion de prompt de sistema estricto con restricciones de dominio cerrado.
- Exigencia de citacion explicita de fuentes (archivo PDF y pagina).
- Respuesta predeterminada ante ausencia de contexto: *"No encontré esta información en los documentos."*

### Fase D: Interfaz y Registro (`app.py` & `logger.py`)
- Desarrollo de interfaz web interactiva en Streamlit con la paleta institucional (azul marino y gris pizarra) integrando el logo oficial (`utl_logo.png`).
- Sistema de auditoria en formato JSON estructurado en `Chat/logs/historial_consultas.json`.

### Fase E: Deploy y Documentacion (`Dockerfile` & `README.md`)
- Empaquetado en contenedor Docker utilizando imagen base Python 3.10-slim.
- Instrucciones de despliegue para Oracle Cloud Infrastructure (OCI).

---

## Estructura del Proyecto

```text
Agente IA/
│
├── Chat/
│   ├── Documentos/               # Archivos PDF oficiales UTL
│   ├── chroma_db/                # Base de datos vectorial persistente
│   └── logs/                     # Registros de auditoria JSON
│
├── fase1_ingestion.py            # Fase A: Ingestion de PDFs
├── fase2_vectorstore.py          # Fase B: Indexacion en ChromaDB
├── fase3_rag_chain.py            # Fase C: Cadena RAG y Prompt Estricto
├── logger.py                     # Modulo de auditoria JSON
├── app.py                        # Fase D: Aplicacion web Streamlit
├── utl_logo.png                  # Logo oficial UTL
│
├── Dockerfile                    # Fase E: Configuracion Docker
├── .dockerignore                 # Exclusiones de Docker
├── requirements.txt              # Dependencias de Python
├── .env.example                  # Plantilla de variables de entorno
└── README.md                     # Documentacion tecnica del proyecto
```

---

## Instalacion y Ejecucion Local

### 1. Clonar el Repositorio
```bash
git clone https://github.com/Angiee-Ali/CHALLENGE-ALURA-AGENTE---JC.git
cd CHALLENGE-ALURA-AGENTE---JC
```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar Variables de Entorno (.env)
Crear un archivo `.env` en la raiz del proyecto con la clave API:
```env
GROQ_API_KEY=tu_clave_api_aqui
```

### 4. Ejecutar Pipeline e Interfaz Web
```bash
python fase1_ingestion.py
python fase2_vectorstore.py
streamlit run app.py
```

Acceder desde el navegador a `http://localhost:8501`.

---

## Guia de Despliegue en Oracle Cloud Infrastructure (OCI)

### 1. Construir la Imagen Docker
```bash
docker build -t chatbot-jc:v1 .
```

### 2. Autenticacion en OCI Container Registry (OCIR)
```bash
docker login <region-key>.ocir.io
```

### 3. Etiquetar y Subir Imagen
```bash
docker tag chatbot-jc:v1 <region-key>.ocir.io/<tenancy-namespace>/chatbot-jc:v1
docker push <region-key>.ocir.io/<tenancy-namespace>/chatbot-jc:v1
```

### 4. Despliegue en Instancia OCI
```bash
docker run -d \
  --name chatbot_jc_container \
  -p 8501:8501 \
  -e GROQ_API_KEY="tu_clave_api_aqui" \
  --restart always \
  <region-key>.ocir.io/<tenancy-namespace>/chatbot-jc:v1
```

### 5. Configuracion de Regla de Ingress en OCI
Habilitar puerto TCP `8501` en la Security List de la VCN para habilitar acceso publico.

---

## Auditoria de Registros JSON (`Chat/logs/historial_consultas.json`)
```json
[
  {
    "timestamp": "2026-07-26 15:40:00",
    "query": "¿Cuál es la nota mínima aprobatoria?",
    "response": "La nota mínima aprobatoria es 13 en la escala vigesimal (0 a 20).\n[Fuente: reglamento_estudiante.pdf | Pagina: 2]"
  }
]
```

---

## Autor
Proyecto final desarrollado para Challenge Alura / Oracle Next Education (ONE).
- Repositorio Git: [Angiee-Ali/CHALLENGE-ALURA-AGENTE---JC](https://github.com/Angiee-Ali/CHALLENGE-ALURA-AGENTE---JC.git)
