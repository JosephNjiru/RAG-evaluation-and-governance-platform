from pathlib import Path

from rag_eval_gov.ingestion.document_loader import load_markdown_documents

ROOT = Path(__file__).resolve().parents[1]


def test_document_loader_preserves_metadata() -> None:
    documents = load_markdown_documents(ROOT / "data/corpus/source_documents")
    assert len(documents) == 10
    first = documents[0]
    assert first.document_id == "DOC-001"
    assert first.sections[0].section_id == "AI-POL-001"
    assert first.owner
