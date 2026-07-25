"""
Paths

Centralized project paths.
"""

from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT_DIR / "data"

KNOWLEDGE_DIR = DATA_DIR / "knowledge_library"

CHROMA_DIR = DATA_DIR / "chromadb"

LOG_DIR = DATA_DIR / "logs"
