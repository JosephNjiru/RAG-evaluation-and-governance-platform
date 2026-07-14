"""Metadata-weighted and hybrid lexical retrieval."""

from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer

from rag_eval_gov.ingestion.chunker import DocumentChunk
from rag_eval_gov.retrieval.bm25_retriever import BM25Retriever, _to_retrieved_chunk
from rag_eval_gov.retrieval.vector_store import RetrievedChunk


class MetadataWeightedTfidfRetriever:
    """TF-IDF retrieval with explicit metadata weighting."""

    def __init__(self, chunks: list[DocumentChunk]) -> None:
        if not chunks:
            raise ValueError("MetadataWeightedTfidfRetriever requires chunks")
        self.chunks = chunks
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            stop_words="english",
            norm="l2",
        )
        self.matrix = self.vectorizer.fit_transform([weighted_text(chunk) for chunk in chunks])

    def search(self, query_id: str, query_text: str, top_k: int = 5) -> list[RetrievedChunk]:
        query_vector = self.vectorizer.transform([query_text])
        scores = (query_vector @ self.matrix.T).toarray()[0]
        ranked = sorted(range(len(scores)), key=lambda index: scores[index], reverse=True)[:top_k]
        return [
            _to_retrieved_chunk(query_id, self.chunks[index], rank, float(scores[index]))
            for rank, index in enumerate(ranked, start=1)
        ]


class HybridLexicalRetriever:
    """Local score fusion of metadata-weighted TF-IDF and BM25."""

    def __init__(self, chunks: list[DocumentChunk], tfidf_weight: float = 0.55) -> None:
        self.chunks = chunks
        self.tfidf = MetadataWeightedTfidfRetriever(chunks)
        self.bm25 = BM25Retriever(chunks)
        self.tfidf_weight = tfidf_weight

    def search(self, query_id: str, query_text: str, top_k: int = 5) -> list[RetrievedChunk]:
        tfidf_results = self.tfidf.search(query_id, query_text, top_k=len(self.chunks))
        bm25_results = self.bm25.search(query_id, query_text, top_k=len(self.chunks))
        tfidf_scores = _normalised_scores(tfidf_results)
        bm25_scores = _normalised_scores(bm25_results)
        fused = {
            chunk.chunk_id: self.tfidf_weight * tfidf_scores.get(chunk.chunk_id, 0.0)
            + (1 - self.tfidf_weight) * bm25_scores.get(chunk.chunk_id, 0.0)
            for chunk in tfidf_results
        }
        chunk_lookup = {chunk.chunk_id: chunk for chunk in tfidf_results}
        ranked_ids = sorted(fused, key=lambda chunk_id: fused[chunk_id], reverse=True)[:top_k]
        return [
            chunk_lookup[chunk_id].model_copy(update={"rank": rank, "score": fused[chunk_id]})
            for rank, chunk_id in enumerate(ranked_ids, start=1)
        ]


def weighted_text(chunk: DocumentChunk) -> str:
    """Repeat metadata fields explicitly while leaving cited evidence unchanged."""

    return "\n".join(
        [
            " ".join([chunk.title] * 4),
            " ".join([chunk.section_heading] * 4),
            " ".join([chunk.risk_domain] * 3),
            chunk.text,
        ]
    )


def _normalised_scores(chunks: list[RetrievedChunk]) -> dict[str, float]:
    if not chunks:
        return {}
    max_score = max((chunk.score for chunk in chunks), default=0.0)
    if max_score <= 0:
        return {chunk.chunk_id: 0.0 for chunk in chunks}
    return {chunk.chunk_id: chunk.score / max_score for chunk in chunks}
