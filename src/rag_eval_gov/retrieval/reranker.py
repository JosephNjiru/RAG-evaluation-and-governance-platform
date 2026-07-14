"""Deterministic reranking placeholder."""

from __future__ import annotations

from rag_eval_gov.retrieval.vector_store import RetrievedChunk


def identity_rerank(results: list[RetrievedChunk]) -> list[RetrievedChunk]:
    """Return TF-IDF results unchanged."""

    return results
