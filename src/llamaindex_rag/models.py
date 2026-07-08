"""Pydantic models for API requests, responses, and domain objects."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Document(BaseModel):
    """A source document to be ingested into the index."""

    id: str | None = Field(default=None, description="Optional stable document identifier.")
    text: str = Field(..., min_length=1, description="Raw document text content.")
    metadata: dict[str, str] = Field(
        default_factory=dict,
        description="Arbitrary key/value metadata attached to the document.",
    )


class Node(BaseModel):
    """A parsed chunk (node) derived from a :class:`Document`."""

    id: str = Field(..., description="Unique node identifier.")
    text: str = Field(..., description="Chunk text content.")
    document_id: str | None = Field(
        default=None, description="Identifier of the parent document."
    )
    metadata: dict[str, str] = Field(
        default_factory=dict, description="Node-level metadata."
    )


class SourceNode(BaseModel):
    """A retrieved node returned as a citation alongside a query answer."""

    node_id: str = Field(..., description="Identifier of the retrieved node.")
    text: str = Field(..., description="Text of the retrieved node.")
    score: float | None = Field(
        default=None, description="Similarity score assigned by the retriever."
    )
    metadata: dict[str, str] = Field(
        default_factory=dict, description="Node-level metadata."
    )


class QueryRequest(BaseModel):
    """Request body for the ``/query`` endpoint."""

    query: str = Field(..., min_length=1, description="Natural-language question.")
    similarity_top_k: int | None = Field(
        default=None,
        ge=1,
        description="Optional override for the number of nodes to retrieve.",
    )


class QueryResponse(BaseModel):
    """Response body for the ``/query`` endpoint."""

    answer: str = Field(..., description="Synthesized answer to the query.")
    source_nodes: list[SourceNode] = Field(
        default_factory=list, description="Nodes used to ground the answer."
    )


class IngestRequest(BaseModel):
    """Request body for the ``/ingest`` endpoint."""

    documents: list[Document] = Field(
        ..., min_length=1, description="Documents to ingest and index."
    )


class IngestResponse(BaseModel):
    """Response body for the ``/ingest`` endpoint."""

    documents_ingested: int = Field(..., ge=0, description="Number of documents ingested.")
    nodes_created: int = Field(..., ge=0, description="Number of nodes created from parsing.")


class HealthStatus(BaseModel):
    """Health/readiness probe response."""

    status: str = Field(..., description="Overall status string, for example 'ok'.")
    service: str = Field(..., description="Service/application name.")
    version: str = Field(..., description="Application version.")
