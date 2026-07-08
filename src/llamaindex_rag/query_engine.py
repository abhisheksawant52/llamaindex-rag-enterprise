"""Query-engine construction.

Assembles a retriever, response synthesizer, and LLM into a LlamaIndex
``RetrieverQueryEngine`` configured with the desired ``similarity_top_k``.
"""

from __future__ import annotations

from llama_index.core import VectorStoreIndex
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.llms.openai import OpenAI

from llamaindex_rag.config import Settings
from llamaindex_rag.logging_config import get_logger

logger = get_logger(__name__)


def build_query_engine(
    index: VectorStoreIndex,
    settings: Settings,
    similarity_top_k: int | None = None,
) -> RetrieverQueryEngine:
    """Construct a query engine over the given index.

    Args:
        index: The vector index to query.
        settings: Application settings (LLM model, default top-k).
        similarity_top_k: Optional override for the number of nodes retrieved.

    Returns:
        A configured :class:`RetrieverQueryEngine`.
    """

    top_k = similarity_top_k or settings.similarity_top_k
    llm = OpenAI(model=settings.llm_model, api_key=settings.openai_api_key)

    retriever = VectorIndexRetriever(index=index, similarity_top_k=top_k)
    response_synthesizer = get_response_synthesizer(llm=llm)

    logger.debug("Building query engine with similarity_top_k=%d", top_k)
    return RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
    )
