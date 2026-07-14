from pathlib import Path

from rag_eval_gov.config.load_config import load_config
from rag_eval_gov.config.schemas import CorpusConfig, ProjectConfig

ROOT = Path(__file__).resolve().parents[1]


def test_project_config_validates() -> None:
    config = load_config(ROOT / "configs/project.yaml", ProjectConfig)
    assert config.package_name == "rag_eval_gov"
    assert "high" in config.approved_risk_levels


def test_corpus_config_validates() -> None:
    config = load_config(ROOT / "configs/corpus.yaml", CorpusConfig)
    assert config.expected_document_count_min == 8
    assert "document_id" in config.required_metadata_fields
