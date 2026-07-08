"""Tests for the ingestion / node-parsing pipeline."""

from __future__ import annotations

from llamaindex_rag.config import Settings
from llamaindex_rag.ingestion import parse_documents
from llamaindex_rag.models import Document


def test_parse_documents_produces_nodes() -> None:
    """A long sample text should be chunked into one or more nodes."""

    settings = Settings(chunk_size=64, chunk_overlap=8)
    sample = " ".join(f"Sentence number {i} about retrieval augmented generation." for i in range(200))
    documents = [Document(id="doc-1", text=sample, metadata={"source": "unit-test"})]

    nodes = parse_documents(documents, settings)

    assert len(nodes) >= 1
    assert all(node.get_content().strip() for node in nodes)


def test_parse_documents_small_text_single_node() -> None:
    """A short document should yield exactly one node."""

    settings = Settings(chunk_size=512, chunk_overlap=20)
    documents = [Document(text="A short document about vector search.")]

    nodes = parse_documents(documents, settings)

    assert len(nodes) == 1
