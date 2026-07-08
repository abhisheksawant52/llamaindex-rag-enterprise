"""Build and persist a LlamaIndex ``VectorStoreIndex`` from documents."""

from __future__ import annotations

from pathlib import Path

from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.core.schema import BaseNode

from llamaindex_rag.config import Settings
from llamaindex_rag.embeddings import build_embedding_model
from llamaindex_rag.ingestion import parse_documents
from llamaindex_rag.logging_config import get_logger
from llamaindex_rag.models import Document
from llamaindex_rag.vectorstore import build_storage_context

logger = get_logger(__name__)


def build_index_from_nodes(
    nodes: list[BaseNode],
    settings: Settings,
) -> VectorStoreIndex:
    """Build a vector index from pre-parsed nodes.

    Args:
        nodes: Parsed LlamaIndex nodes.
        settings: Application settings (embedding model, vector store).

    Returns:
        A populated :class:`VectorStoreIndex`.
    """

    embed_model = build_embedding_model(settings)
    storage_context = build_storage_context(settings)
    logger.info("Building VectorStoreIndex from %d nodes", len(nodes))
    return VectorStoreIndex(
        nodes=nodes,
        storage_context=storage_context,
        embed_model=embed_model,
    )


def build_index_from_documents(
    documents: list[Document],
    settings: Settings,
) -> VectorStoreIndex:
    """Parse documents and build a vector index in one step.

    Args:
        documents: Domain documents to index.
        settings: Application settings.

    Returns:
        A populated :class:`VectorStoreIndex`.
    """

    nodes = parse_documents(documents, settings)
    return build_index_from_nodes(nodes, settings)


def persist_index(index: VectorStoreIndex, persist_dir: str | Path) -> None:
    """Persist an index to disk.

    Args:
        index: The index to persist.
        persist_dir: Target directory for persisted storage.
    """

    path = Path(persist_dir)
    path.mkdir(parents=True, exist_ok=True)
    index.storage_context.persist(persist_dir=str(path))
    logger.info("Persisted index to %s", path)


def load_index(persist_dir: str | Path, settings: Settings) -> VectorStoreIndex:
    """Load a previously persisted index from disk.

    Args:
        persist_dir: Directory containing persisted storage.
        settings: Application settings (embedding model).

    Returns:
        The reconstructed :class:`VectorStoreIndex`.
    """

    embed_model = build_embedding_model(settings)
    storage_context = StorageContext.from_defaults(persist_dir=str(persist_dir))
    logger.info("Loading index from %s", persist_dir)
    return load_index_from_storage(storage_context, embed_model=embed_model)
