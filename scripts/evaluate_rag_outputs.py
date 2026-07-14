"""Evaluate Stage 2 RAG outputs with deterministic Stage 3 metrics."""
# ruff: noqa: E402

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag_eval_gov.judging.rule_based_judge import evaluate_questions
from rag_eval_gov.metrics.summary_metrics import build_summary_table
from rag_eval_gov.reports.evaluation_report import build_evaluation_report
from scripts.build_vector_index import build_vector_index
from scripts.run_rag_batch import run_rag_batch
from scripts.validate_stage1_assets import validate_stage1_assets


def ensure_stage2_outputs(root: Path = ROOT) -> None:
    required = [
        root / "data/processed/chunks.parquet",
        root / "outputs/answers/rag_answers.parquet",
        root / "outputs/answers/retrieval_results.parquet",
    ]
    if all(path.exists() for path in required):
        return
    validate_stage1_assets(root)
    build_vector_index(root)
    run_rag_batch(root)


def evaluate_rag_outputs(root: Path = ROOT) -> dict[str, object]:
    ensure_stage2_outputs(root)
    question_bank = pd.read_csv(root / "data/evaluation/question_bank.csv").fillna("")
    reference_answers = pd.read_csv(root / "data/evaluation/reference_answers.csv").fillna("")
    evidence_map = pd.read_csv(root / "data/evaluation/evidence_map.csv").fillna("")
    answers = pd.read_parquet(root / "outputs/answers/rag_answers.parquet")
    retrieval_results = pd.read_parquet(root / "outputs/answers/retrieval_results.parquet")

    results = evaluate_questions(
        question_bank=question_bank,
        reference_answers=reference_answers,
        evidence_map=evidence_map,
        answers=answers,
        retrieval_results=retrieval_results,
        rubric_path=root / "configs/evaluation_rubrics.yaml",
    )
    summary = build_summary_table(results)

    evaluation_dir = root / "outputs/evaluation"
    evaluation_dir.mkdir(parents=True, exist_ok=True)
    report_dir = root / "outputs/reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    results.to_parquet(evaluation_dir / "rag_evaluation_results.parquet")
    summary.to_csv(evaluation_dir / "rag_evaluation_summary.csv", index=False)
    (report_dir / "stage_3_evaluation_report.md").write_text(
        build_evaluation_report(results, summary),
        encoding="utf-8",
    )
    return {
        "questions": len(results),
        "overall_pass_rate": float(results["overall_pass"].mean()),
        "summary_rows": len(summary),
        "human_review_queue": int(
            (
                results["human_review_expected"] | results["safety_flag"] | ~results["overall_pass"]
            ).sum()
        ),
    }


def main() -> None:
    summary = evaluate_rag_outputs()
    print("Stage 3 evaluation complete.")
    for key, value in summary.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
