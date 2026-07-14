"""Diversity-aware reranking for source-linked retrieval results."""

from __future__ import annotations

from collections import defaultdict

from rag_eval_gov.retrieval.question_intent import QuestionIntent, detect_question_intent
from rag_eval_gov.retrieval.vector_store import RetrievedChunk


def diversified_rerank(
    query_text: str,
    chunks: list[RetrievedChunk],
    top_k: int = 5,
) -> list[RetrievedChunk]:
    """Rerank chunks to reduce duplicate sections for multi-evidence questions."""

    intent = detect_question_intent(query_text)
    if intent != QuestionIntent.LIKELY_MULTI_HOP:
        return _renumber(chunks[:top_k])

    section_counts: dict[str, int] = defaultdict(int)
    document_counts: dict[str, int] = defaultdict(int)
    selected: list[RetrievedChunk] = []
    candidates = sorted(chunks, key=lambda item: item.score, reverse=True)
    while candidates and len(selected) < top_k:
        best_index = max(
            range(len(candidates)),
            key=lambda index: _diversity_score(
                candidates[index],
                section_counts,
                document_counts,
                query_text,
            ),
        )
        item = candidates.pop(best_index)
        selected.append(item)
        section_counts[f"{item.document_id}:{item.section_id}"] += 1
        document_counts[item.document_id] += 1
    return _renumber(selected)


def _diversity_score(
    chunk: RetrievedChunk,
    section_counts: dict[str, int],
    document_counts: dict[str, int],
    query_text: str,
) -> float:
    section_key = f"{chunk.document_id}:{chunk.section_id}"
    heading_bonus = (
        0.05 if _heading_overlap(query_text, chunk.metadata.get("section_heading", "")) else 0.0
    )
    section_penalty = 0.35 * section_counts[section_key]
    document_penalty = 0.10 * document_counts[chunk.document_id]
    return chunk.score + heading_bonus - section_penalty - document_penalty


def _heading_overlap(query_text: str, heading: str) -> bool:
    query_terms = {term for term in query_text.lower().split() if len(term) > 3}
    heading_terms = {term for term in heading.lower().split() if len(term) > 3}
    return bool(query_terms & heading_terms)


def _renumber(chunks: list[RetrievedChunk]) -> list[RetrievedChunk]:
    return [chunk.model_copy(update={"rank": rank}) for rank, chunk in enumerate(chunks, start=1)]
