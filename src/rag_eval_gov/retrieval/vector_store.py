"""Local vector store for TF-IDF retrieval."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from pydantic import BaseModel, ConfigDict
from scipy import sparse

from rag_eval_gov.ingestion.chunker import DocumentChunk
from rag_eval_gov.retrieval.embeddings import TfidfEmbeddingModel


class RetrievedChunk(BaseModel):
    """A retrieved chunk with ranking metadata."""

    model_config = ConfigDict(extra="forbid")

    query_id: str
    chunk_id: str
    document_id: str
    section_id: str
    rank: int
    score: float
    text: str
    metadata: dict[str, str]


class LocalVectorStore:
    """Persisted TF-IDF matrix and chunk metadata."""

    def __init__(
        self,
        chunks: list[DocumentChunk],
        embedding_model: TfidfEmbeddingModel,
        matrix: sparse.csr_matrix,
    ) -> None:
        self.chunks = chunks
        self.embedding_model = embedding_model
        self.matrix = matrix

    @classmethod
    def build(cls, chunks: list[DocumentChunk]) -> LocalVectorStore:
        if not chunks:
            raise ValueError("Cannot build a vector store without chunks")
        model = TfidfEmbeddingModel()
        matrix = model.fit_transform([search_text(chunk) for chunk in chunks])
        return cls(chunks=chunks, embedding_model=model, matrix=matrix)

    def save(self, index_dir: Path, chunks_path: Path) -> None:
        index_dir.mkdir(parents=True, exist_ok=True)
        chunks_path.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame([chunk.model_dump() for chunk in self.chunks]).to_parquet(chunks_path)
        self.embedding_model.save(index_dir / "tfidf_vectorizer.joblib")
        sparse.save_npz(index_dir / "tfidf_matrix.npz", self.matrix)

    @classmethod
    def load(cls, index_dir: Path, chunks_path: Path) -> LocalVectorStore:
        chunk_records = pd.read_parquet(chunks_path).to_dict(orient="records")
        chunks = [DocumentChunk.model_validate(record) for record in chunk_records]
        model = TfidfEmbeddingModel.load(index_dir / "tfidf_vectorizer.joblib")
        matrix = sparse.load_npz(index_dir / "tfidf_matrix.npz").tocsr()
        return cls(chunks=chunks, embedding_model=model, matrix=matrix)

    def search(self, query_id: str, query_text: str, top_k: int = 5) -> list[RetrievedChunk]:
        query_vector = self.embedding_model.transform([query_text])
        scores = (query_vector @ self.matrix.T).toarray()[0]
        ranked_indices = sorted(range(len(scores)), key=lambda index: scores[index], reverse=True)
        results: list[RetrievedChunk] = []
        for rank, index in enumerate(ranked_indices[:top_k], start=1):
            chunk = self.chunks[index]
            results.append(
                RetrievedChunk(
                    query_id=query_id,
                    chunk_id=chunk.chunk_id,
                    document_id=chunk.document_id,
                    section_id=chunk.section_id,
                    rank=rank,
                    score=float(scores[index]),
                    text=chunk.text,
                    metadata=chunk.metadata,
                )
            )
        return results


def search_text(chunk: DocumentChunk) -> str:
    """Build transparent lexical text for indexing without changing cited evidence."""

    return "\n".join([chunk.title, chunk.section_heading, chunk.risk_domain, chunk.text])
