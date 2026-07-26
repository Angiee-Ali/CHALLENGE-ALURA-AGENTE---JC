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
    
    .stButton > button {
        background: linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 500;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
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
    
    with st.expander("Reglamento del Estudiante"):
        st.markdown("""
        <div class="doc-info-box">
        <strong>Especificaciones:</strong><br>
        - Asistencia minima requerida: 80%.<br>
        - Evaluaciones: Parcial (30%), Final (40%), Continua (30%).<br>
        - Nota minima aprobatoria: 13.<br>
        - Normativa de conducta academica.
        </div>
        """, unsafe_allow_html=True)
        if st.button("Consultar Reglamento", key="btn_reg", use_container_width=True):
            st.session_state.temp_prompt = "¿Cuáles son las normas del reglamento del estudiante sobre asistencia y evaluaciones?"

    with st.expander("Politica de Reembolso de Matriculas"):
        st.markdown("""
        <div class="doc-info-box">
        <strong>Especificaciones:</strong><br>
        - Reembolso 100%: Hasta 7 dias antes del inicio de clases.<br>
        - Reembolso 50%: Primeros 3 dias de inicio de clases.<br>
        - Tramite formal mediante el modulo de Soporte.
        </div>
        """, unsafe_allow_html=True)
        if st.button("Consultar Reembolsos", key="btn_rem", use_container_width=True):
            st.session_state.temp_prompt = "¿Cómo aplican las políticas de reembolso de matrícula y cuáles son sus plazos?"

    with st.expander("Preguntas Frecuentes (FAQ)"):
        st.markdown("""
        <div class="doc-info-box">
        <strong>Especificaciones:</strong><br>
        - Emision de certificados digitales en 5 dias habiles.<br>
        - Requisitos para cursar dos especializaciones simultaneas.
        </div>
        """, unsafe_allow_html=True)
        if st.button("Consultar Certificados", key="btn_faq", use_container_width=True):
            st.session_state.temp_prompt = "¿Cómo se obtiene el certificado de estudios y cuáles son los requisitos?"

    with st.expander("Guia de Uso de la Plataforma"):
        st.markdown("""
        <div class="doc-info-box">
        <strong>Especificaciones:</strong><br>
        - Acceso a campus.utl.edu.pe.<br>
        - Entrega de tareas en formato PDF/ZIP (maximo 25 MB).
        </div>
        """, unsafe_allow_html=True)
        if st.button("Consultar Plataforma", key="btn_gui", use_container_width=True):
            st.session_state.temp_prompt = "¿Cómo se entregan las tareas en la plataforma y cuál me el límite de tamaño?"

    with st.expander("Programa de Becas y Afiliados"):
        st.markdown("""
        <div class="doc-info-box">
        <strong>Especificaciones:</strong><br>
        - Beca Excelencia Academica: 50% de descuento en pension.<br>
        - Programa de Referidos: 10% de descuento acumulable.
        </div>
        """, unsafe_allow_html=True)
        if st.button("Consultar Becas", key="btn_bec", use_container_width=True):
            st.session_state.temp_prompt = "¿En qué consiste el programa de becas por excelencia y referidos de la UTL?"

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


prompt_sugerido = st.session_state.pop("temp_prompt", None)
prompt_usuario = prompt_sugerido or st.chat_input("Ingrese su consulta academica o administrativa...")

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
