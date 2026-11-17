"""Configurações carregadas do ambiente; nenhuma credencial é embutida no código."""
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent

def db_path() -> Path:
    return Path(os.environ.get("PROJECT_DB_PATH", str(ROOT / "artifacts" / "projeto_ia.sqlite3")))

def model_path() -> Path:
    return Path(os.environ.get("PROJECT_MODEL_PATH", str(ROOT / "artifacts" / "sentiment.joblib")))

def openai_model() -> str:
    return os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")
