"""Tests for pydantic model validation."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from llamaindex_rag.models import (
    Document,
    IngestRequest,
    QueryRequest,
    QueryResponse,
    SourceNode,
)


def test_document_requires_non_empty_text() -> None:
    """A document with empty text should fail validation."""

    with pytest.raises(ValidationError):
        Document(text="")


def test_query_request_defaults() -> None:
    """A minimal query request should validate with optional top_k unset."""

    req = QueryRequest(query="What is RAG?")
    assert req.query == "What is RAG?"
    assert req.similarity_top_k is None


def test_query_request_top_k_must_be_positive() -> None:
    """similarity_top_k below 1 should be rejected."""

    with pytest.raises(ValidationError):
        QueryRequest(query="hi", similarity_top_k=0)


def test_ingest_request_requires_documents() -> None:
    """An ingest request with no documents should fail validation."""

    with pytest.raises(ValidationError):
        IngestRequest(documents=[])


def test_query_response_source_nodes() -> None:
    """QueryResponse should accept a list of source nodes."""

    resp = QueryResponse(
        answer="42",
        source_nodes=[SourceNode(node_id="n1", text="ctx", score=0.9)],
    )
    assert resp.answer == "42"
    assert resp.source_nodes[0].node_id == "n1"
    assert resp.source_nodes[0].score == pytest.approx(0.9)
