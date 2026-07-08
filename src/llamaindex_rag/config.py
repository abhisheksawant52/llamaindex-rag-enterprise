"""Application configuration.

Settings are loaded from environment variables (prefixed with ``LIRAG_``) or an
optional ``.env`` file using :mod:`pydantic_settings`.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the RAG service.

    All values may be overridden via environment variables using the
    ``LIRAG_`` prefix (for example ``LIRAG_LLM_MODEL=gpt-4o``).
    """

    model_config = SettingsConfigDict(
        env_prefix="LIRAG_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = Field(
        default="llamaindex-rag-enterprise",
        description="Human-readable application name.",
    )
    environment: str = Field(
        default="development",
        description="Deployment environment (development, staging, production).",
    )
    log_level: str = Field(
        default="INFO",
        description="Root logging level.",
    )

    openai_api_key: str | None = Field(
        default=None,
        description="OpenAI API key used for embeddings and LLM calls.",
    )
    embedding_model: str = Field(
        default="text-embedding-3-small",
        description="Embedding model identifier.",
    )
    llm_model: str = Field(
        default="gpt-4o-mini",
        description="LLM model identifier used by the query engine.",
    )

    vector_store_url: str = Field(
        default="http://localhost:6333",
        description="Connection URL for the backing vector store.",
    )
    similarity_top_k: int = Field(
        default=4,
        ge=1,
        description="Number of top nodes to retrieve for a query.",
    )
    chunk_size: int = Field(
        default=1024,
        ge=1,
        description="Maximum token size of a parsed node/chunk.",
    )
    chunk_overlap: int = Field(
        default=128,
        ge=0,
        description="Token overlap between adjacent chunks.",
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached :class:`Settings` instance.

    The result is memoised so configuration is parsed from the environment
    only once per process.
    """

    return Settings()
