"""Citation formatting helpers."""

from __future__ import annotations

from rag_eval_gov.generation.answer_schema import Citation
from rag_eval_gov.retrieval.vector_store import RetrievedChunk


def citations_from_chunks(chunks: list[RetrievedChunk]) -> list[Citation]:
    """Build unique section citations from retrieved chunks."""

    seen: set[tuple[str, str]] = set()
    citations: list[Citation] = []
    for chunk in chunks:
        key = (chunk.document_id, chunk.section_id)
        if key in seen:
            continue
        seen.add(key)
        citations.append(
            Citation(
                document_id=chunk.document_id,
                section_id=chunk.section_id,
                chunk_id=chunk.chunk_id,
            )
        )
    return citations


def format_citation(citation: Citation) -> str:
    """Format one citation label."""

    return f"[{citation.document_id}:{citation.section_id}]"


def format_citations(citations: list[Citation]) -> list[str]:
    """Format citation labels for answer records."""

    return [format_citation(citation) for citation in citations]
