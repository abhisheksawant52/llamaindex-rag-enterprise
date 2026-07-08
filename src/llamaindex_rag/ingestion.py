"""Document loading and node-parsing pipeline.

Converts raw :class:`~llamaindex_rag.models.Document` payloads into LlamaIndex
``Document`` objects and parses them into nodes (chunks) using a sentence
splitter configured with the application chunk size and overlap.
"""

from __future__ import annotations

from llama_index.core import Document as LlamaDocument
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import BaseNode

from llamaindex_rag.config import Settings
from llamaindex_rag.logging_config import get_logger
from llamaindex_rag.models import Document

logger = get_logger(__name__)


def to_llama_documents(documents: list[Document]) -> list[LlamaDocument]:
    """Convert API documents into LlamaIndex documents.

    Args:
        documents: Domain documents received from the ingest API.

    Returns:
        A list of LlamaIndex :class:`Document` objects.
    """

    llama_docs: list[LlamaDocument] = []
    for doc in documents:
        llama_docs.append(
            LlamaDocument(
                text=doc.text,
                doc_id=doc.id,
                metadata=dict(doc.metadata),
            )
        )
    return llama_docs


def build_node_parser(settings: Settings) -> SentenceSplitter:
    """Create a sentence-splitting node parser from settings.

    Args:
        settings: Application settings providing chunk size and overlap.

    Returns:
        A configured :class:`SentenceSplitter`.
    """

    return SentenceSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )


def parse_documents(documents: list[Document], settings: Settings) -> list[BaseNode]:
    """Load documents and parse them into nodes.

    Args:
        documents: Domain documents to ingest.
        settings: Application settings controlling chunking behaviour.

    Returns:
        A list of parsed LlamaIndex nodes.
    """

    llama_docs = to_llama_documents(documents)
    parser = build_node_parser(settings)
    nodes = parser.get_nodes_from_documents(llama_docs)
    logger.info("Parsed %d documents into %d nodes", len(llama_docs), len(nodes))
    return nodes
