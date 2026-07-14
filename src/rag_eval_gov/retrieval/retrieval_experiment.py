"""Retrieval ablation helpers."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import pandas as pd

from rag_eval_gov.config.schemas import QuestionRecord
from rag_eval_gov.evaluation.question_bank import load_question_bank
from rag_eval_gov.generation.answer_schema import AnswerRecord
from rag_eval_gov.generation.mock_generator import MockAnswerGenerator
from rag_eval_gov.ingestion.chunker import DocumentChunk
from rag_eval_gov.retrieval.bm25_retriever import BM25Retriever
from rag_eval_gov.retrieval.diversified_reranker import diversified_rerank
from rag_eval_gov.retrieval.hybrid_retriever import (
    HybridLexicalRetriever,
    MetadataWeightedTfidfRetriever,
)
from rag_eval_gov.retrieval.query_decomposition import decompose_query
from rag_eval_gov.retrieval.retriever import Retriever
from rag_eval_gov.retrieval.vector_store import LocalVectorStore, RetrievedChunk


@dataclass(frozen=True)
class RunConfig:
    """Run metadata recorded for baseline and improved runs."""

    run_id: str
    run_label: str
    retrieval_method: str
    chunking_method: str
    top_k: int
    reranking_method: str
    query_decomposition_enabled: bool
    generator_mode: str
    evaluation_method: str
    created_at: str


class MultiHopDecompositionRetriever:
    """Hybrid retrieval with text-only decomposition and diversified reranking."""

    def __init__(self, chunks: list[DocumentChunk]) -> None:
        self.hybrid = HybridLexicalRetriever(chunks)

    def search(self, query_id: str, query_text: str, top_k: int = 5) -> list[RetrievedChunk]:
        combined: dict[str, RetrievedChunk] = {}
        sub_queries = decompose_query(query_text)
        for sub_query in sub_queries:
            for chunk in self.hybrid.search(query_id, sub_query, top_k=top_k):
                existing = combined.get(chunk.chunk_id)
                score = chunk.score / max(len(sub_queries), 1)
                if existing is None:
                    combined[chunk.chunk_id] = chunk.model_copy(update={"score": score})
                else:
                    combined[chunk.chunk_id] = existing.model_copy(
                        update={"score": existing.score + score}
                    )
        candidates = sorted(combined.values(), key=lambda item: item.score, reverse=True)
        return diversified_rerank(query_text, candidates, top_k=top_k)


def load_chunks(chunks_path: Path) -> list[DocumentChunk]:
    records = pd.read_parquet(chunks_path).to_dict(orient="records")
    return [DocumentChunk.model_validate(record) for record in records]


def run_retrieval_method(
    method: str,
    questions: list[QuestionRecord],
    chunks_path: Path,
    index_dir: Path,
    top_k: int = 5,
) -> list[RetrievedChunk]:
    """Run a named retrieval method without using evaluation ground truth."""

    chunks = load_chunks(chunks_path)
    if method == "baseline_a_tfidf":
        retriever = Retriever(
            LocalVectorStore.load(index_dir=index_dir, chunks_path=chunks_path), top_k=top_k
        )
        return [
            chunk
            for question in questions
            for chunk in retriever.retrieve(question.question_id, question.question_text)
        ]
    if method == "baseline_b_metadata_weighted_tfidf":
        searcher = MetadataWeightedTfidfRetriever(chunks)
    elif method == "baseline_c_bm25":
        searcher = BM25Retriever(chunks)
    elif method == "baseline_d_hybrid":
        searcher = HybridLexicalRetriever(chunks)
    elif method == "baseline_e_decomposition_diversified":
        searcher = MultiHopDecompositionRetriever(chunks)
    else:
        raise ValueError(f"Unknown retrieval method: {method}")
    return [
        chunk
        for question in questions
        for chunk in searcher.search(question.question_id, question.question_text, top_k=top_k)
    ]


def generate_answers_for_retrieval(
    questions: list[QuestionRecord],
    retrieval_rows: list[RetrievedChunk],
) -> list[AnswerRecord]:
    """Generate answers from retrieval rows without reading evaluation labels."""

    generator = ImprovedCitationMockGenerator()
    by_question: dict[str, list[RetrievedChunk]] = {}
    for row in retrieval_rows:
        by_question.setdefault(row.query_id, []).append(row)
    return [
        generator.generate(
            question, sorted(by_question.get(question.question_id, []), key=lambda row: row.rank)
        )
        for question in questions
    ]


class ImprovedCitationMockGenerator(MockAnswerGenerator):
    """Mock generator that selects diverse cited sections from retrieved evidence."""

    generation_mode = "deterministic_mock_improved_retrieval"

    def generate(
        self,
        question: QuestionRecord,
        retrieved_chunks: list[RetrievedChunk],
    ) -> AnswerRecord:
        useful = [chunk for chunk in retrieved_chunks if chunk.score > 0]
        if self._should_refuse(question, useful):
            return super().generate(question, retrieved_chunks)
        citation_chunks = _diverse_chunks(useful, limit=2)
        if not citation_chunks:
            return super().generate(question, retrieved_chunks)
        return super().generate(
            question, citation_chunks + [chunk for chunk in useful if chunk not in citation_chunks]
        )


def write_run_manifest(rows: list[RunConfig], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([row.__dict__ for row in rows]).to_csv(output_path, index=False)


def default_run_config(
    run_id: str,
    run_label: str,
    retrieval_method: str,
    top_k: int,
    decomposition: bool = False,
    reranking: str = "none",
) -> RunConfig:
    return RunConfig(
        run_id=run_id,
        run_label=run_label,
        retrieval_method=retrieval_method,
        chunking_method="section-aware word window",
        top_k=top_k,
        reranking_method=reranking,
        query_decomposition_enabled=decomposition,
        generator_mode="deterministic_mock",
        evaluation_method="rule_based_post_generation_evaluation",
        created_at=datetime.utcnow().isoformat(),
    )


def load_default_questions(root: Path) -> list[QuestionRecord]:
    return load_question_bank(root / "data/evaluation/question_bank.csv")


def _diverse_chunks(chunks: list[RetrievedChunk], limit: int) -> list[RetrievedChunk]:
    selected: list[RetrievedChunk] = []
    seen_sections: set[str] = set()
    for chunk in chunks:
        key = f"{chunk.document_id}:{chunk.section_id}"
        if key in seen_sections:
            continue
        selected.append(chunk)
        seen_sections.add(key)
        if len(selected) >= limit:
            break
    return selected
