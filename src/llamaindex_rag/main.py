"""FastAPI application exposing the RAG query and ingest APIs."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException

from llamaindex_rag import __version__
from llamaindex_rag.config import get_settings
from llamaindex_rag.logging_config import configure_logging, get_logger
from llamaindex_rag.models import (
    HealthStatus,
    IngestRequest,
    IngestResponse,
    QueryRequest,
    QueryResponse,
)
from llamaindex_rag.service import RagService

logger = get_logger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        A configured :class:`FastAPI` instance.
    """

    settings = get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(
        title=settings.app_name,
        version=__version__,
        description="Enterprise RAG service built on LlamaIndex.",
    )

    service = RagService(settings)
    app.state.service = service

    @app.get("/health", response_model=HealthStatus, tags=["system"])
    def health() -> HealthStatus:
        """Liveness probe."""

        return HealthStatus(status="ok", service=settings.app_name, version=__version__)

    @app.get("/ready", response_model=HealthStatus, tags=["system"])
    def ready() -> HealthStatus:
        """Readiness probe: reports 'ready' once an index has been built."""

        status = "ready" if service.is_ready else "pending"
        return HealthStatus(status=status, service=settings.app_name, version=__version__)

    @app.post("/ingest", response_model=IngestResponse, tags=["rag"])
    def ingest(request: IngestRequest) -> IngestResponse:
        """Ingest documents and (re)build the vector index."""

        return service.ingest(request.documents)

    @app.post("/query", response_model=QueryResponse, tags=["rag"])
    def query(request: QueryRequest) -> QueryResponse:
        """Answer a natural-language query against the index."""

        try:
            return service.query(request.query, request.similarity_top_k)
        except RuntimeError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

    @app.get("/documents", tags=["rag"])
    def documents() -> dict[str, int]:
        """Return simple statistics about ingested documents."""

        return {"documents_ingested": service.document_count}

    return app


app = create_app()


def run() -> None:
    """Run the application with uvicorn (development convenience entrypoint)."""

    import uvicorn

    uvicorn.run("llamaindex_rag.main:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    run()
