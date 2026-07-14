from rag_eval_gov.generation.citation_formatter import citations_from_chunks, format_citations
from rag_eval_gov.retrieval.vector_store import RetrievedChunk


def test_citation_formatter_deduplicates_sections() -> None:
    chunks = [
        RetrievedChunk(
            query_id="Q",
            chunk_id="DOC-001:SEC-001:001",
            document_id="DOC-001",
            section_id="SEC-001",
            rank=1,
            score=0.9,
            text="Evidence.",
            metadata={"document_id": "DOC-001", "section_id": "SEC-001"},
        ),
        RetrievedChunk(
            query_id="Q",
            chunk_id="DOC-001:SEC-001:002",
            document_id="DOC-001",
            section_id="SEC-001",
            rank=2,
            score=0.7,
            text="More evidence.",
            metadata={"document_id": "DOC-001", "section_id": "SEC-001"},
        ),
    ]
    citations = citations_from_chunks(chunks)
    assert format_citations(citations) == ["[DOC-001:SEC-001]"]
