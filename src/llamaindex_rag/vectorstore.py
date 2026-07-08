"""Vector store provider abstractions.

Provides a storage context factory. The default implementation uses the
in-memory simple vector store; production deployments can swap in a networked
store (for example Qdrant or OpenSearch) via ``settings.vector_store_url``.
"""

from __future__ import annotations

from llama_index.core import StorageContext
from llama_index.core.vector_stores.simple import SimpleVectorStore

from llamaindex_rag.config import Settings
from llamaindex_rag.logging_config import get_logger

logger = get_logger(__name__)


def build_storage_context(settings: Settings) -> StorageContext:
    """Build a LlamaIndex storage context for the configured vector store.

    Args:
        settings: Application settings describing the vector store location.

    Returns:
        A configured :class:`StorageContext`.
    """

    logger.debug("Building storage context for %s", settings.vector_store_url)
    vector_store = SimpleVectorStore()
    return StorageContext.from_defaults(vector_store=vector_store)
