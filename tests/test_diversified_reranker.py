from rag_eval_gov.retrieval.diversified_reranker import diversified_rerank
from rag_eval_gov.retrieval.vector_store import RetrievedChunk


def test_diversified_reranker_prefers_section_diversity_for_multi_hop() -> None:
    chunks = [
        _chunk("C1", "DOC-1", "S1", 0.9),
        _chunk("C2", "DOC-1", "S1", 0.8),
        _chunk("C3", "DOC-2", "S2", 0.7),
    ]
    reranked = diversified_rerank("What controls and who reviews?", chunks, top_k=2)
    assert {item.section_id for item in reranked} == {"S1", "S2"}


def _chunk(chunk_id: str, document_id: str, section_id: str, score: float) -> RetrievedChunk:
    return RetrievedChunk(
        query_id="Q",
        chunk_id=chunk_id,
        document_id=document_id,
        section_id=section_id,
        rank=1,
        score=score,
        text="evidence text",
        metadata={"section_heading": section_id},
    )
