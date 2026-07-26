import os
import json
from datetime import datetime


def get_log_filepath() -> str:
    """Retorna y asegura la ruta del archivo de registros de auditoria JSON."""
    log_dir = os.path.join("Chat", "logs")
    os.makedirs(log_dir, exist_ok=True)
    return os.path.join(log_dir, "historial_consultas.json")


def log_interaction(query: str, response: str):
    """Registra una consulta y respuesta en el historial de auditoria."""
    filepath = get_log_filepath()
    
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "query": query,
        "response": response
    }
    
    history = []
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            history = []
            
    history.append(entry)
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
