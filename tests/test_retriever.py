from pathlib import Path

from rag_eval_gov.ingestion.chunker import chunk_documents
from rag_eval_gov.ingestion.document_loader import load_markdown_documents
from rag_eval_gov.retrieval.retriever import Retriever
from rag_eval_gov.retrieval.vector_store import LocalVectorStore

ROOT = Path(__file__).resolve().parents[1]


def test_retriever_returns_source_linked_results() -> None:
    documents = load_markdown_documents(ROOT / "data/corpus/source_documents")
    store = LocalVectorStore.build(chunk_documents(documents))
    retriever = Retriever(store, top_k=4)
    results = retriever.retrieve("QF-019", "What makes an answer faithful?")
    assert len(results) == 4
    assert results[0].query_id == "QF-019"
    assert all(result.chunk_id for result in results)
    assert all(result.metadata["document_id"] == result.document_id for result in results)
