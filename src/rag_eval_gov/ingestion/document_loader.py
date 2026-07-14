"""Load Stage 1 source documents for Stage 2 ingestion."""

from __future__ import annotations

from pathlib import Path

from rag_eval_gov.corpus.build_corpus import load_corpus
from rag_eval_gov.corpus.document_models import SourceDocument


def load_markdown_documents(source_dir: Path) -> list[SourceDocument]:
    """Load Markdown documents while preserving source metadata."""

    return load_corpus(source_dir)
