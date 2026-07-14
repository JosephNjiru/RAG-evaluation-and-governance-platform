from pathlib import Path

from rag_eval_gov.ingestion.chunker import ChunkingConfig, chunk_documents
from rag_eval_gov.ingestion.document_loader import load_markdown_documents

ROOT = Path(__file__).resolve().parents[1]


def test_chunker_keeps_source_traceability() -> None:
    documents = load_markdown_documents(ROOT / "data/corpus/source_documents")
    chunks = chunk_documents(documents, ChunkingConfig(max_words=80, overlap_words=10))
    assert chunks
    assert all(chunk.document_id for chunk in chunks)
    assert all(chunk.section_id for chunk in chunks)
    assert all(chunk.chunk_id.startswith(chunk.document_id) for chunk in chunks)
    assert all(chunk.metadata["section_id"] == chunk.section_id for chunk in chunks)
