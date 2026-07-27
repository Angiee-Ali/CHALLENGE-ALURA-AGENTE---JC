# Agente Inteligente RAG "JC" - Universidad Tecnologica de Lima (UTL)

## 1. Descripcion General del Proyecto

Proyecto final desarrollado como estudiante de ingenieria de software para la Universidad Tecnologica de Lima (UTL). El sistema implementa a JC, un Agente de Inteligencia Artificial funcional basado en Arquitectura RAG (Retrieval-Augmented Generation) diseñado para resolver consultas academicas y administrativas de los estudiantes basandose exclusivamente en la documentacion oficial en formato PDF, garantizando respuestas fundamentadas y libres de alucinaciones.

---

## 2. Arquitectura de la Solucion Implementada

El sistema opera mediante un pipeline desacoplado en cinco fases principales:

```text
[PDFs Oficiales UTL] -> (PyPDFLoader) -> (Limpieza & Chunking)
                                                |
                                                v
[Interfaz Streamlit] <- (LLM Llama-3.1) <- (Prompt Estricto) <- (ChromaDB Vectorstore)
```

1. **Ingestion**: Lectura estructurada de los 5 PDFs oficiales mediante PyPDFLoader, aplicando expresiones regulares para normalizar saltos de linea y filtrando portadas ruidosas de menos de 80 caracteres.
2. **Vectorstore**: Indexacion semantica de fragmentos mediante el modelo de embeddings `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` almacenados de forma persistente en una base de datos vectorial local (ChromaDB).
3. **Rag_chain**: Ejecucion de busqueda por similitud semantica (k=6) para construir un contexto enriquecido que se envia a un LLM (Llama 3.1 8B via Groq API) sujeto a un prompt de sistema estricto con asociacion semantica y citacion obligatoria de fuente (nombre del PDF y numero de pagina).
4. **Interfaz y Registro**: Despliegue de una aplicacion web interactiva en Streamlit con logo institucional (`utl_logo.png`), descargas directas de PDF y registro de auditoria en formato JSON (`Chat/logs/historial_consultas.json`).
5. **Deploy**: Despliegue continuo en produccion mediante Streamlit Community Cloud y preparado para contenerizacion con Docker en Oracle Cloud Infrastructure (OCI).

---

## 3. Tecnologias y Herramientas Utilizadas

- **Lenguaje de Programacion**: Python 3.10+
- **Orquestador RAG**: LangChain Core / LangChain Community / LCEL
- **Lectura y Procesamiento Documental**: PyPDFLoader & RecursiveCharacterTextSplitter
- **Base de Datos Vectorial**: ChromaDB
- **Modelo de Embeddings**: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (HuggingFace)
- **Modelo de Lenguaje (LLM)**: Meta Llama 3.1 8B Instant (via Groq API) / OpenAI GPT-4o-mini
- **Interfaz de Usuario**: Streamlit
- **Plataforma de Despliegue Cloud**: Streamlit Community Cloud / Docker / Oracle Cloud Infrastructure (OCI)

---

## 4. Procesamiento de Documentos

El codigo fuente procesa la base de conocimiento compuesta por 5 archivos PDF en `Chat/Documentos/` (`reglamento_estudiante.pdf`, `politica_reembolso_matriculas.pdf`, `preguntas_frecuentes_cursos_certificados.pdf`, `guia_uso_plataforma.pdf` y `programa_becas_afiliados.pdf`):

1. **Lectura y Limpieza**: `fase1_ingestion.py` lee cada pagina mediante `PyPDFLoader`, remueve tabulaciones basura y espacios redundantes, y descarta portadas de encabezado ruidosas (< 80 caracteres).
2. **Chunking Jerarquico**: Los textos extraidos son segmentados con `RecursiveCharacterTextSplitter` utilizando un tamaño de bloque de 1000 caracteres y una superposicion (overlap) de 200 caracteres para preservar la continuidad entre frases.
3. **Preservacion de Metadatos**: Cada fragmento generado es etiquetado con su metadato de origen (`source`: nombre del PDF, `page`: numero de pagina).

---

## 5. Instrucciones para Ejecutar el Proyecto

### Requisitos Previos
- Python 3.10 o superior instalado.
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
Crear un archivo `.env` en la raiz del proyecto con la clave API:
```env
GROQ_API_KEY=tu_clave_api_aqui
```

### Paso 4: Ejecutar el Pipeline e Iniciar la Interfaz Web
```bash
python fase1_ingestion.py
python fase2_vectorstore.py
streamlit run app.py
```
Acceder en el navegador a `http://localhost:8501`.

---

## 6. Ejemplos de Interaccion

### A. Ejemplos de Preguntas que el Agente puede Responder
1. ¿Cuál es la nota mínima aprobatoria para obtener el certificado?
2. ¿Hasta cuántos días antes del inicio de clases puedo solicitar el 100% de reembolso de mi matrícula?
3. ¿Cómo se entregan las tareas en la plataforma y cuál es el tamaño máximo de archivo permitido?

### B. Ejemplos de Respuestas Generadas por el Agente

#### Ejemplo 1:
- **Consulta**: ¿Cuál es la nota mínima aprobatoria para obtener el certificado?
- **Respuesta de JC**:
  > Según las preguntas frecuentes sobre cursos y certificados de la Universidad Tecnológica de Lima (UTL), para obtener el certificado el estudiante debe haber visualizado todos los módulos y aprobado las evaluaciones con una nota mínima de 14.
  >
  > Fuente: preguntas_frecuentes_cursos_certificados.pdf | Pagina: 2

#### Ejemplo 2:
- **Consulta**: ¿Hasta cuántos días antes del inicio de clases puedo solicitar el 100% de reembolso de mi matrícula?
- **Respuesta de JC**:
  > La cancelación con devolución del 100% de la matrícula se aplicará si el estudiante realiza la solicitud formal hasta siete (7) días calendario antes de la fecha de inicio oficial del curso.
  >
  > Fuente: politica_reembolso_matriculas.pdf | Pagina: 2

#### Ejemplo 3:
- **Consulta**: ¿Cómo se entregan las tareas en la plataforma y cuál es el tamaño máximo de archivo permitido?
- **Respuesta de JC**:
  > Para entregar tareas en la plataforma educativa, debe ingresar a la sección 'Mis Cursos', seleccionar la asignatura, hacer clic en 'Tareas' y adjuntar su archivo en formato PDF o ZIP. El tamaño máximo permitido por archivo es de 25 MB.
  >
  > Fuente: guia_uso_plataforma.pdf | Pagina: 2

---

## 7. Evidencia del Deploy en Streamlit Community Cloud (Produccion)

### Enlace Publico en Produccion
- **Aplicacion Desplegada**: [https://alura-agente---jc.streamlit.app/](https://alura-agente---jc.streamlit.app/)

### Evidencia Visual en Produccion

![Aplicación en producción](assets/deploy_evidencia.png)
