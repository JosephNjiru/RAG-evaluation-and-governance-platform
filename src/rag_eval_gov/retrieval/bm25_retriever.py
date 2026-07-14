"""Local BM25-style lexical retrieval."""

from __future__ import annotations

import math
import re
from collections import Counter

from rag_eval_gov.ingestion.chunker import DocumentChunk
from rag_eval_gov.retrieval.vector_store import RetrievedChunk

TOKEN_RE = re.compile(r"[a-z0-9]+")


class BM25Retriever:
    """Small dependency-free BM25 implementation for local experiments."""

    def __init__(self, chunks: list[DocumentChunk], k1: float = 1.5, b: float = 0.75) -> None:
        if not chunks:
            raise ValueError("BM25Retriever requires at least one chunk")
        self.chunks = chunks
        self.k1 = k1
        self.b = b
        self.documents = [_tokenize(_search_text(chunk)) for chunk in chunks]
        self.term_counts = [Counter(document) for document in self.documents]
        self.doc_lengths = [len(document) for document in self.documents]
        self.avg_doc_length = sum(self.doc_lengths) / len(self.doc_lengths)
        self.idf = self._build_idf()

    def search(self, query_id: str, query_text: str, top_k: int = 5) -> list[RetrievedChunk]:
        query_terms = _tokenize(query_text)
        scores = [self._score(query_terms, index) for index in range(len(self.chunks))]
        ranked = sorted(range(len(scores)), key=lambda index: scores[index], reverse=True)[:top_k]
        return [
            _to_retrieved_chunk(query_id, self.chunks[index], rank, scores[index])
            for rank, index in enumerate(ranked, start=1)
        ]

    def _build_idf(self) -> dict[str, float]:
        document_count = len(self.documents)
        document_frequency: Counter[str] = Counter()
        for document in self.documents:
            document_frequency.update(set(document))
        return {
            term: math.log(1 + (document_count - count + 0.5) / (count + 0.5))
            for term, count in document_frequency.items()
        }

    def _score(self, query_terms: list[str], index: int) -> float:
        score = 0.0
        counts = self.term_counts[index]
        doc_length = self.doc_lengths[index]
        for term in query_terms:
            frequency = counts.get(term, 0)
            if frequency == 0:
                continue
            denominator = frequency + self.k1 * (
                1 - self.b + self.b * doc_length / self.avg_doc_length
            )
            score += self.idf.get(term, 0.0) * frequency * (self.k1 + 1) / denominator
        return float(score)


def _search_text(chunk: DocumentChunk) -> str:
    return "\n".join(
        [
            chunk.title,
            chunk.section_heading,
            chunk.risk_domain,
            chunk.text,
        ]
    )


def _tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


def _to_retrieved_chunk(
    query_id: str,
    chunk: DocumentChunk,
    rank: int,
    score: float,
) -> RetrievedChunk:
    metadata = dict(chunk.metadata)
    metadata.setdefault("source_file", metadata.get("document_id", chunk.document_id))
    return RetrievedChunk(
        query_id=query_id,
        chunk_id=chunk.chunk_id,
        document_id=chunk.document_id,
        section_id=chunk.section_id,
        rank=rank,
        score=score,
        text=chunk.text,
        metadata=metadata,
    )
