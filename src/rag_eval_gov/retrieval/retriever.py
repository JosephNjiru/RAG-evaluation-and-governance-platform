"""High-level retrieval interface."""

from __future__ import annotations

from rag_eval_gov.retrieval.reranker import identity_rerank
from rag_eval_gov.retrieval.vector_store import LocalVectorStore, RetrievedChunk


class Retriever:
    """Retrieve source-linked chunks from a local vector store."""

    def __init__(self, vector_store: LocalVectorStore, top_k: int = 5) -> None:
        self.vector_store = vector_store
        self.top_k = top_k

    def retrieve(self, query_id: str, query_text: str) -> list[RetrievedChunk]:
        return identity_rerank(self.vector_store.search(query_id, query_text, self.top_k))
