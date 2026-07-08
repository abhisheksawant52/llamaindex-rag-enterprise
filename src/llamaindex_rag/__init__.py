"""llamaindex-rag-enterprise.

An enterprise-grade Retrieval-Augmented Generation (RAG) service built on
LlamaIndex and FastAPI. The package exposes document ingestion, vector
indexing, and query APIs suitable for production deployment.
"""

from __future__ import annotations

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "get_settings",
    "Settings",
    "RagService",
    "create_app",
]

from llamaindex_rag.config import Settings, get_settings
from llamaindex_rag.main import create_app
from llamaindex_rag.service import RagService
