import os
import sys
import importlib

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import streamlit as st
import fase3_rag_chain
import logger

importlib.reload(fase3_rag_chain)
importlib.reload(logger)

from fase3_rag_chain import build_rag_chain
from logger import log_interaction

st.set_page_config(
    page_title="Agente JC - UTL",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f1f5f9;
    }
    
    [data-testid="stSidebar"] {
        background-color: #1e293b;
        border-right: 1px solid #334155;
    }
    
    .header-banner {
        background: linear-gradient(90deg, #1e3a8a 0%, #2563eb 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        margin-bottom: 2rem;
        border-left: 6px solid #60a5fa;
    }
    
    .header-title {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
    }
    
    .header-subtitle {
        color: #93c5fd;
        font-size: 1.05rem;
        margin-top: 0.3rem;
        font-weight: 400;
    }
    
    .stChatMessage {
        background-color: #334155 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        border: 1px solid #475569 !important;
        margin-bottom: 0.8rem;
    }
    
    .stButton > button, .stDownloadButton > button {
        background: linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 500;
        width: 100%;
    }
    
    .doc-info-box {
        background-color: #0f172a;
        border-left: 4px solid #3b82f6;
        padding: 10px 14px;
        border-radius: 8px;
        margin-top: 5px;
        margin-bottom: 10px;
        font-size: 0.88rem;
        color: #cbd5e1;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource(show_spinner=False)
def get_rag_chain_cached():
    return build_rag_chain()


with st.sidebar:
    logo_path = "utl_logo.png"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.markdown("### Universidad Tecnológica de Lima")
        
    st.markdown("<h3 style='text-align: center; margin-top: 10px;'>Agente IA - JC</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Atencion al Estudiante UTL</p>", unsafe_allow_html=True)
    st.divider()
    
    st.markdown("#### Documentos Institucionales")
    
    # 1. Reglamento del Estudiante
    with st.expander("Reglamento del Estudiante"):
        st.markdown("""
        <div class="doc-info-box">
        <strong>Especificaciones:</strong><br>
        - Asistencia minima requerida: 80%.<br>
        - Evaluaciones: Parcial (30%), Final (40%), Continua (30%).<br>
        - Nota minima aprobatoria: 13.<br>
        </div>
        """, unsafe_allow_html=True)
        pdf_path = os.path.join("Chat", "Documentos", "reglamento_estudiante.pdf")
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="Descargar PDF Reglamento",
                    data=f.read(),
                    file_name="reglamento_estudiante.pdf",
                    mime="application/pdf",
                    key="dl_reg"
                )

    # 2. Política de Reembolso
    with st.expander("Politica de Reembolso de Matriculas"):
        st.markdown("""
        <div class="doc-info-box">
        <strong>Especificaciones:</strong><br>
        - Reembolso 100%: Hasta 7 dias antes del inicio.<br>
        - Reembolso 50%: Primeros 3 dias de inicio.<br>
        </div>
        """, unsafe_allow_html=True)
        pdf_path = os.path.join("Chat", "Documentos", "politica_reembolso_matriculas.pdf")
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="Descargar PDF Reembolso",
                    data=f.read(),
                    file_name="politica_reembolso_matriculas.pdf",
                    mime="application/pdf",
                    key="dl_rem"
                )

    # 3. Preguntas Frecuentes
    with st.expander("Preguntas Frecuentes (FAQ)"):
        st.markdown("""
        <div class="doc-info-box">
        <strong>Especificaciones:</strong><br>
        - Certificados digitales en 5 dias habiles.<br>
        - Doble especializacion simultanea.<br>
        </div>
        """, unsafe_allow_html=True)
        pdf_path = os.path.join("Chat", "Documentos", "preguntas_frecuentes_cursos_certificados.pdf")
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="Descargar PDF FAQ",
                    data=f.read(),
                    file_name="preguntas_frecuentes_cursos_certificados.pdf",
                    mime="application/pdf",
                    key="dl_faq"
                )

    # 4. Guía de Uso de la Plataforma
    with st.expander("Guia de Uso de la Plataforma"):
        st.markdown("""
        <div class="doc-info-box">
        <strong>Especificaciones:</strong><br>
        - Acceso a campus.utl.edu.pe.<br>
        - Tareas PDF/ZIP hasta 25 MB.<br>
        </div>
        """, unsafe_allow_html=True)
        pdf_path = os.path.join("Chat", "Documentos", "guia_uso_plataforma.pdf")
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="Descargar PDF Guia",
                    data=f.read(),
                    file_name="guia_uso_plataforma.pdf",
                    mime="application/pdf",
                    key="dl_gui"
                )

    # 5. Programa de Becas
    with st.expander("Programa de Becas y Afiliados"):
        st.markdown("""
        <div class="doc-info-box">
        <strong>Especificaciones:</strong><br>
        - Beca Excelencia: 50% de descuento.<br>
        - Referidos: 10% acumulable.<br>
        </div>
        """, unsafe_allow_html=True)
        pdf_path = os.path.join("Chat", "Documentos", "programa_becas_afiliados.pdf")
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="Descargar PDF Becas",
                    data=f.read(),
                    file_name="programa_becas_afiliados.pdf",
                    mime="application/pdf",
                    key="dl_bec"
                )

    st.divider()
    
    if st.button("Reiniciar Conversacion", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


st.markdown("""
    <div class="header-banner">
        <div class="header-title">Agente Inteligente UTL - JC</div>
        <div class="header-subtitle">Plataforma Educativa Online - Atencion al Estudiante</div>
    </div>
""", unsafe_allow_html=True)


if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Bienvenido al portal institucional. Soy JC, el agente virtual de la Universidad Tecnologica de Lima. Puedo resolver consultas sobre reglamentos, reembolsos, certificados, becas y uso de la plataforma."
        }
    ]


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


prompt_usuario = st.chat_input("Ingrese su consulta academica o administrativa...")

if prompt_usuario:
    st.session_state.messages.append({"role": "user", "content": prompt_usuario})
    with st.chat_message("user"):
        st.markdown(prompt_usuario)

    with st.chat_message("assistant"):
        with st.spinner("Procesando consulta en la base documental UTL..."):
            try:
                rag_chain = get_rag_chain_cached()
                response_jc = rag_chain.invoke(prompt_usuario)
                
                st.markdown(response_jc)
                st.session_state.messages.append({"role": "assistant", "content": response_jc})
                
                log_interaction(prompt_usuario, response_jc)
            except Exception as e:
                st.error(f"Error al procesar la consulta: {str(e)}")
