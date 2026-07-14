from pathlib import Path

from rag_eval_gov.corpus.build_corpus import load_corpus
from scripts.validate_stage1_assets import validate_stage1_assets

ROOT = Path(__file__).resolve().parents[1]


def test_stage1_validation_script_passes() -> None:
    summary = validate_stage1_assets(ROOT)
    assert summary["status"] == "passed"
    assert summary["questions"] >= 60


def test_corpus_documents_have_sections() -> None:
    documents = load_corpus(ROOT / "data/corpus/source_documents")
    assert 8 <= len(documents) <= 12
    assert all(document.sections for document in documents)
