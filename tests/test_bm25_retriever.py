from rag_eval_gov.ingestion.chunker import DocumentChunk
from rag_eval_gov.retrieval.bm25_retriever import BM25Retriever


def test_bm25_retriever_preserves_traceability() -> None:
    chunk = DocumentChunk(
        chunk_id="DOC-X:SEC-1:001",
        document_id="DOC-X",
        section_id="SEC-1",
        chunk_index=1,
        text="Human review is required for high risk outputs.",
        title="Review policy",
        version="1.0",
        date="2026-01-01",
        owner="Owner",
        risk_domain="governance",
        section_heading="SEC-1 Review",
        metadata={"source_file": "doc-x.md"},
    )
    result = BM25Retriever([chunk]).search("Q", "human review", top_k=1)[0]
    assert result.document_id == "DOC-X"
    assert result.section_id == "SEC-1"
    assert result.metadata["source_file"] == "doc-x.md"
