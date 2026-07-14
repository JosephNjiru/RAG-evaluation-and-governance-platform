"""Local FastAPI service for Stage 4 release checks."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from rag_eval_gov.api.schemas import (
    AnswerResponse,
    EvaluationRequest,
    EvaluationResponse,
    HumanReviewQueueItem,
    QuestionRequest,
    RetrievedContextResponse,
    SummaryResponse,
)
from rag_eval_gov.config.schemas import (
    APPROVED_QUESTION_TYPES,
    APPROVED_RISK_LEVELS,
    QuestionRecord,
)
from rag_eval_gov.generation.mock_generator import MockAnswerGenerator
from rag_eval_gov.retrieval.retriever import Retriever
from rag_eval_gov.retrieval.vector_store import LocalVectorStore
from rag_eval_gov.security.context_security import assess_retrieved_context
from rag_eval_gov.security.input_security import assess_input_security
from rag_eval_gov.security.output_security import validate_output_security
from rag_eval_gov.security.security_policy import (
    HIGH_RISK_FLAGS,
    LOCAL_CORS_ORIGINS,
    REQUEST_SIZE_LIMIT_BYTES,
)

ROOT = Path(__file__).resolve().parents[3]
app = FastAPI(
    title="RAG Evaluation and Governance Platform",
    description="Local API for deterministic RAG baseline answers and evaluation summaries.",
    version="0.4.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=LOCAL_CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["content-type"],
)


@app.middleware("http")
async def request_size_limit(request: Request, call_next):
    """Reject oversized requests before body parsing."""

    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > REQUEST_SIZE_LIMIT_BYTES:
        return JSONResponse(
            status_code=413,
            content={"error": "request_too_large", "detail": "Request exceeds local size limit."},
        )
    return await call_next(request)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    """Return validation errors without debug tracebacks."""

    return JSONResponse(
        status_code=422,
        content={"error": "validation_error", "detail": "Request schema validation failed."},
    )


@app.exception_handler(Exception)
async def general_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    """Return safe errors without exposing tracebacks."""

    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code, content={"error": "http_error", "detail": exc.detail}
        )
    return JSONResponse(
        status_code=500,
        content={"error": "internal_error", "detail": "Request could not be completed."},
    )


@app.get("/health")
def health() -> dict[str, str]:
    """Return service health and local asset status."""

    ensure_local_outputs()
    return {"status": "ok", "mode": "local_deterministic"}


@app.get("/summary", response_model=SummaryResponse)
def summary() -> SummaryResponse:
    """Return the Stage 3 evaluation summary."""

    ensure_local_outputs()
    results, summary_table = load_evaluation_outputs()
    overall = summary_table[summary_table["question_type"] == "overall"].iloc[0]
    factual = summary_table[summary_table["question_type"] == "factual"].iloc[0]
    multi_hop = summary_table[summary_table["question_type"] == "multi_hop"].iloc[0]
    return SummaryResponse(
        questions=int(overall["questions"]),
        overall_pass_rate=float(overall["overall_pass_rate"]),
        factual_pass_rate=float(factual["overall_pass_rate"]),
        multi_hop_pass_rate=float(multi_hop["overall_pass_rate"]),
        citation_precision=float(overall["mean_citation_precision"]),
        citation_recall=float(overall["mean_citation_recall"]),
        faithfulness_score=float(overall["mean_faithfulness"]),
        human_review_match_rate=float(overall["human_review_match_rate"]),
        safety_flag_rate=float(results["safety_flag"].mean()),
    )


@app.post("/question", response_model=AnswerResponse)
def answer_question(request: QuestionRequest) -> AnswerResponse:
    """Run one submitted question through the local RAG baseline."""

    if request.question_type not in APPROVED_QUESTION_TYPES:
        raise HTTPException(status_code=422, detail="Unsupported question_type")
    if request.risk_level not in APPROVED_RISK_LEVELS:
        raise HTTPException(status_code=422, detail="Unsupported risk_level")

    question_id = request.question_id or f"api_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
    input_security = assess_input_security(request.question_text)
    if input_security.should_refuse:
        return AnswerResponse(
            question_id=question_id,
            question_text=request.question_text,
            answer_text="I cannot answer this request because it triggers local security controls and needs human review.",
            retrieved_contexts=[],
            citations=[],
            refusal_flag=True,
            confidence_label="low",
            risk_level=request.risk_level,
            requires_human_review=True,
            generation_mode="security_refusal",
            evaluation_summary=summary().model_dump(),
            security_flags=input_security.flags,
            security_action="refuse",
        )

    ensure_local_outputs()
    question = QuestionRecord(
        question_id=question_id,
        question_text=request.question_text,
        question_type=request.question_type,
        risk_level=request.risk_level,
        expected_answer_type="generated_local_response",
        requires_human_review=request.requires_human_review,
        expected_source_documents="",
        notes="Submitted through local API.",
    )
    vector_store = LocalVectorStore.load(
        index_dir=ROOT / "data/index",
        chunks_path=ROOT / "data/processed/chunks.parquet",
    )
    retriever = Retriever(vector_store=vector_store, top_k=5)
    retrieved = retriever.retrieve(question.question_id, question.question_text)
    context_security = assess_retrieved_context(retrieved)
    answer = MockAnswerGenerator().generate(question, retrieved)
    output_security = validate_output_security(
        answer,
        retrieved,
        citations_required=request.question_type in {"factual", "multi_hop"},
    )
    security_flags = sorted(
        set(input_security.flags + context_security.flags + output_security.flags)
    )
    security_action = "review" if security_flags else "allow"
    if set(security_flags) & HIGH_RISK_FLAGS:
        security_action = "refuse"
    return AnswerResponse(
        question_id=answer.question_id,
        question_text=answer.question_text,
        answer_text=answer.answer_text,
        retrieved_contexts=[
            RetrievedContextResponse(
                chunk_id=item.chunk_id,
                document_id=item.document_id,
                section_id=item.section_id,
                rank=item.rank,
                score=item.score,
                text=item.text,
            )
            for item in retrieved
        ],
        citations=answer.citations,
        refusal_flag=answer.refusal_flag,
        confidence_label=answer.confidence_label,
        risk_level=answer.risk_level,
        requires_human_review=answer.requires_human_review,
        generation_mode=answer.generation_mode,
        evaluation_summary=summary().model_dump(),
        security_flags=security_flags,
        security_action=security_action,
    )


@app.post("/evaluate", response_model=EvaluationResponse)
def evaluate_answer(request: EvaluationRequest) -> EvaluationResponse:
    """Return an existing deterministic evaluation record for a known question."""

    ensure_local_outputs()
    results, _ = load_evaluation_outputs()
    if request.question_id:
        matches = results[results["question_id"] == request.question_id]
    elif request.question_text:
        question_bank = pd.read_csv(ROOT / "data/evaluation/question_bank.csv").fillna("")
        question_matches = question_bank[
            question_bank["question_text"].str.casefold() == request.question_text.casefold()
        ]
        if question_matches.empty:
            matches = pd.DataFrame()
        else:
            matches = results[results["question_id"] == question_matches.iloc[0]["question_id"]]
    else:
        raise HTTPException(status_code=422, detail="question_id or question_text is required")
    if matches.empty:
        raise HTTPException(status_code=404, detail="No matching Stage 3 evaluation record")
    row = matches.iloc[0].to_dict()
    return row_to_evaluation(row)


@app.get("/human-review-queue", response_model=list[HumanReviewQueueItem])
def human_review_queue(limit: int = 30) -> list[HumanReviewQueueItem]:
    """Return records that need review or failed a deterministic gate."""

    ensure_local_outputs()
    results, _ = load_evaluation_outputs()
    queue = results[
        results["human_review_expected"] | results["safety_flag"] | ~results["overall_pass"]
    ].head(limit)
    return [
        HumanReviewQueueItem(
            question_id=str(row["question_id"]),
            question_type=str(row["question_type"]),
            risk_level=str(row["risk_level"]),
            overall_pass=bool(row["overall_pass"]),
            safety_flag=bool(row["safety_flag"]),
            human_review_expected=bool(row["human_review_expected"]),
            human_review_flagged=bool(row["human_review_flagged"]),
            evaluation_notes=str(row["evaluation_notes"]),
        )
        for _, row in queue.iterrows()
    ]


def ensure_local_outputs() -> None:
    """Regenerate required local assets in the documented order when missing."""

    required = [
        ROOT / "data/processed/chunks.parquet",
        ROOT / "outputs/answers/rag_answers.parquet",
        ROOT / "outputs/answers/retrieval_results.parquet",
        ROOT / "outputs/evaluation/rag_evaluation_results.parquet",
        ROOT / "outputs/evaluation/rag_evaluation_summary.csv",
    ]
    if all(path.exists() for path in required):
        return

    from scripts.build_vector_index import build_vector_index
    from scripts.evaluate_rag_outputs import evaluate_rag_outputs
    from scripts.run_rag_batch import run_rag_batch
    from scripts.validate_stage1_assets import validate_stage1_assets

    validate_stage1_assets(ROOT)
    build_vector_index(ROOT)
    run_rag_batch(ROOT)
    evaluate_rag_outputs(ROOT)


def load_evaluation_outputs() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load Stage 3 evaluation result tables."""

    results = pd.read_parquet(ROOT / "outputs/evaluation/rag_evaluation_results.parquet")
    summary_table = pd.read_csv(ROOT / "outputs/evaluation/rag_evaluation_summary.csv")
    return results, summary_table


def row_to_evaluation(row: dict[str, Any]) -> EvaluationResponse:
    """Convert one result row to the public API shape."""

    return EvaluationResponse(
        question_id=str(row["question_id"]),
        question_type=str(row["question_type"]),
        overall_pass=bool(row["overall_pass"]),
        retrieval_hit=bool(row["retrieval_hit"]),
        citation_precision=float(row["citation_precision"]),
        citation_recall=float(row["citation_recall"]),
        faithfulness_score=float(row["faithfulness_score"]),
        refusal_correct=bool(row["refusal_correct"]),
        safety_flag=bool(row["safety_flag"]),
        human_review_expected=bool(row["human_review_expected"]),
        human_review_flagged=bool(row["human_review_flagged"]),
        evaluation_notes=str(row["evaluation_notes"]),
    )
