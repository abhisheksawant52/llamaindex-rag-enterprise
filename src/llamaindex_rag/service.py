"""High-level RAG service orchestration.

:class:`RagService` ties together ingestion, indexing, and querying, holding the
active :class:`VectorStoreIndex` in memory across requests.
"""

from __future__ import annotations

from llama_index.core import VectorStoreIndex

from llamaindex_rag.config import Settings, get_settings
from llamaindex_rag.indexing import build_index_from_nodes
from llamaindex_rag.ingestion import parse_documents
from llamaindex_rag.logging_config import get_logger
from llamaindex_rag.models import (
    Document,
    IngestResponse,
    QueryResponse,
    SourceNode,
)
from llamaindex_rag.query_engine import build_query_engine

logger = get_logger(__name__)


class RagService:
    """Orchestrates document ingestion and querying over a vector index."""

    def __init__(self, settings: Settings | None = None) -> None:
        """Initialise the service.

        Args:
            settings: Optional settings override; defaults to :func:`get_settings`.
        """

        self._settings = settings or get_settings()
        self._index: VectorStoreIndex | None = None
        self._node_count: int = 0
        self._document_count: int = 0

    @property
    def is_ready(self) -> bool:
        """Return ``True`` once an index has been built."""

        return self._index is not None

    @property
    def document_count(self) -> int:
        """Number of documents ingested so far."""

        return self._document_count

    def ingest(self, documents: list[Document]) -> IngestResponse:
        """Ingest documents, parse them, and (re)build the index.

        Args:
            documents: Documents to ingest.

        Returns:
            An :class:`IngestResponse` summarising the operation.
        """

        nodes = parse_documents(documents, self._settings)
        self._index = build_index_from_nodes(nodes, self._settings)
        self._document_count += len(documents)
        self._node_count = len(nodes)
        logger.info("Ingested %d documents (%d nodes)", len(documents), len(nodes))
        return IngestResponse(
            documents_ingested=len(documents),
            nodes_created=len(nodes),
        )

    def query(self, question: str, similarity_top_k: int | None = None) -> QueryResponse:
        """Answer a question against the current index.

        Args:
            question: Natural-language query.
            similarity_top_k: Optional retrieval depth override.

        Returns:
            A :class:`QueryResponse` with the answer and source nodes.

        Raises:
            RuntimeError: If no documents have been ingested yet.
        """

        if self._index is None:
            raise RuntimeError("Index is empty; ingest documents before querying.")

        engine = build_query_engine(self._index, self._settings, similarity_top_k)
        response = engine.query(question)

        source_nodes: list[SourceNode] = []
        for node_with_score in getattr(response, "source_nodes", []) or []:
            source_nodes.append(
                SourceNode(
                    node_id=node_with_score.node.node_id,
                    text=node_with_score.node.get_content(),
                    score=node_with_score.score,
                    metadata={
                        str(k): str(v)
                        for k, v in (node_with_score.node.metadata or {}).items()
                    },
                )
            )

        return QueryResponse(answer=str(response), source_nodes=source_nodes)
