from pathlib import Path

from rag_eval_gov.ingestion.chunker import chunk_documents
from rag_eval_gov.ingestion.document_loader import load_markdown_documents
from rag_eval_gov.retrieval.vector_store import LocalVectorStore

ROOT = Path(__file__).resolve().parents[1]


def test_vector_store_retrieves_relevant_chunk() -> None:
    documents = load_markdown_documents(ROOT / "data/corpus/source_documents")
    chunks = chunk_documents(documents)
    store = LocalVectorStore.build(chunks)
    results = store.search("QTEST", "What must secrets and passwords not be copied into?", top_k=3)
    assert results[0].document_id == "DOC-003"
    assert results[0].section_id == "SEC-PROC-001"
    assert results[0].score > 0
