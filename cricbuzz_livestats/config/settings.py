import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = BASE_DIR / "cricket.db"


def _read_secret(key: str):
    """Read from Streamlit secrets when available, else return None."""
    try:
        return st.secrets.get(key)
    except Exception:
        return None


RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY") or _read_secret("RAPIDAPI_KEY")
DB_PATH = os.getenv("DB_PATH") or _read_secret("DB_PATH") or str(DEFAULT_DB_PATH)

# Ensure the DB directory exists in local/dev deployments.
Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)

DB_URL = f"sqlite:///{DB_PATH}"