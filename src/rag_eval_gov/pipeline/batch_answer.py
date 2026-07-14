"""Batch RAG answering for the Stage 1 question bank."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from rag_eval_gov.evaluation.question_bank import load_question_bank
from rag_eval_gov.generation.answer_schema import AnswerRecord
from rag_eval_gov.generation.mock_generator import MockAnswerGenerator
from rag_eval_gov.pipeline.run_rag import run_rag_question
from rag_eval_gov.retrieval.retriever import Retriever
from rag_eval_gov.retrieval.vector_store import LocalVectorStore, RetrievedChunk


def run_batch(
    question_bank_path: Path,
    index_dir: Path,
    chunks_path: Path,
    top_k: int = 5,
) -> list[AnswerRecord]:
    """Run all question-bank records through the local RAG pipeline."""

    questions = load_question_bank(question_bank_path)
    vector_store = LocalVectorStore.load(index_dir=index_dir, chunks_path=chunks_path)
    retriever = Retriever(vector_store=vector_store, top_k=top_k)
    return [run_rag_question(question, retriever) for question in questions]


def run_batch_with_retrieval(
    question_bank_path: Path,
    index_dir: Path,
    chunks_path: Path,
    top_k: int = 5,
) -> tuple[list[AnswerRecord], list[RetrievedChunk]]:
    """Run the batch pipeline and retain retrieval rows for evaluation."""

    questions = load_question_bank(question_bank_path)
    vector_store = LocalVectorStore.load(index_dir=index_dir, chunks_path=chunks_path)
    retriever = Retriever(vector_store=vector_store, top_k=top_k)
    generator = MockAnswerGenerator()
    answers: list[AnswerRecord] = []
    retrieval_rows: list[RetrievedChunk] = []
    for question in questions:
        retrieved_chunks = retriever.retrieve(question.question_id, question.question_text)
        retrieval_rows.extend(retrieved_chunks)
        answers.append(generator.generate(question, retrieved_chunks))
    return answers, retrieval_rows


def write_answer_records(records: list[AnswerRecord], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = [record.model_dump(mode="json") for record in records]
    pd.DataFrame(rows).to_parquet(output_path)


def write_retrieval_records(records: list[RetrievedChunk], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = [record.model_dump(mode="json") for record in records]
    pd.DataFrame(rows).to_parquet(output_path)
