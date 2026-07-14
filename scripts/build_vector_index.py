"""Build the local Stage 2 TF-IDF vector index."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from rag_eval_gov.ingestion.chunker import ChunkingConfig, chunk_documents
from rag_eval_gov.ingestion.document_loader import load_markdown_documents
from rag_eval_gov.retrieval.vector_store import LocalVectorStore

ROOT = Path(__file__).resolve().parents[1]


def build_vector_index(root: Path = ROOT) -> dict[str, int]:
    documents = load_markdown_documents(root / "data/corpus/source_documents")
    chunks = chunk_documents(documents, ChunkingConfig(max_words=120, overlap_words=20))
    vector_store = LocalVectorStore.build(chunks)
    chunks_path = root / "data/processed/chunks.parquet"
    index_dir = root / "data/index"
    vector_store.save(index_dir=index_dir, chunks_path=chunks_path)

    summary = {
        "documents": len(documents),
        "chunks": len(chunks),
        "unique_documents": pd.Series([chunk.document_id for chunk in chunks]).nunique(),
    }
    return summary


def main() -> None:
    summary = build_vector_index()
    print("Stage 2 vector index built.")
    for key, value in summary.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
