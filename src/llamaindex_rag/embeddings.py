"""Embedding provider abstractions.

Wraps LlamaIndex embedding backends behind a small factory so the rest of the
codebase depends on configuration rather than concrete providers.
"""

from __future__ import annotations

from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding

from llamaindex_rag.config import Settings
from llamaindex_rag.logging_config import get_logger

logger = get_logger(__name__)


def build_embedding_model(settings: Settings) -> BaseEmbedding:
    """Construct an embedding model from application settings.

    Args:
        settings: Application settings providing the model name and API key.

    Returns:
        A LlamaIndex :class:`BaseEmbedding` implementation.
    """

    logger.debug("Building embedding model %s", settings.embedding_model)
    return OpenAIEmbedding(
        model=settings.embedding_model,
        api_key=settings.openai_api_key,
    )
