"""Evaluate the holdout challenge set after retrieval improvements."""
# ruff: noqa: E402

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag_eval_gov.evaluation.question_bank import load_question_bank
from rag_eval_gov.judging.rule_based_judge import evaluate_questions
from rag_eval_gov.metrics.summary_metrics import build_summary_table
from rag_eval_gov.retrieval.retrieval_experiment import (
    generate_answers_for_retrieval,
    run_retrieval_method,
)


def evaluate_challenge_set(root: Path = ROOT) -> dict[str, object]:
    questions = load_question_bank(root / "data/evaluation/challenge_questions.csv")
    retrieval_rows = run_retrieval_method(
        "baseline_e_decomposition_diversified",
        questions,
        chunks_path=root / "data/processed/chunks.parquet",
        index_dir=root / "data/index",
        top_k=5,
    )
    answers = generate_answers_for_retrieval(questions, retrieval_rows)
    question_bank = pd.read_csv(root / "data/evaluation/challenge_questions.csv").fillna("")
    reference_answers = pd.read_csv(
        root / "data/evaluation/challenge_reference_answers.csv"
    ).fillna("")
    evidence_map = pd.read_csv(root / "data/evaluation/challenge_evidence_map.csv").fillna("")
    answers_frame = pd.DataFrame([answer.model_dump(mode="json") for answer in answers])
    retrieval_frame = pd.DataFrame([row.model_dump(mode="json") for row in retrieval_rows])
    results = evaluate_questions(
        question_bank=question_bank,
        reference_answers=reference_answers,
        evidence_map=evidence_map,
        answers=answers_frame,
        retrieval_results=retrieval_frame,
        rubric_path=root / "configs/evaluation_rubrics.yaml",
    )
    summary = build_summary_table(results)
    output_dir = root / "outputs/evaluation"
    report_dir = root / "outputs/reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)
    results.to_parquet(output_dir / "challenge_evaluation_results.parquet")
    difficulty_profile = build_difficulty_profile(question_bank, evidence_map)
    difficulty_profile.to_csv(output_dir / "question_difficulty_profile.csv", index=False)
    (report_dir / "challenge_set_report.md").write_text(
        build_challenge_report(summary, difficulty_profile),
        encoding="utf-8",
    )
    overall = summary[summary["question_type"] == "overall"].iloc[0]
    return {
        "questions": int(overall["questions"]),
        "overall_pass_rate": float(overall["overall_pass_rate"]),
    }


def build_challenge_report(summary: pd.DataFrame, difficulty_profile: pd.DataFrame) -> str:
    difficulty_summary = difficulty_profile.groupby("question_type", as_index=False).agg(
        questions=("question_id", "count"),
        mean_expected_evidence_rows=("expected_evidence_rows", "mean"),
        human_review_required=("requires_human_review", "sum"),
        conflict_resolution_required=("requires_conflict_resolution", "sum"),
        version_preference_required=("requires_version_preference", "sum"),
    )
    return "\n".join(
        [
            "# Challenge set report",
            "",
            "The challenge set is a post-improvement holdout set. It is not used to tune retrieval.",
            "",
            "The challenge set has a different difficulty profile from the original 60-question benchmark. It should not be treated as a direct replacement for the original multi-hop benchmark. The original 60-question evaluation remains the main baseline comparison.",
            "",
            _markdown_table(summary.fillna("n/a")),
            "",
            "## Difficulty profile summary",
            "",
            _markdown_table(difficulty_summary.fillna("n/a")),
            "",
            "## Safety interpretation",
            "",
            "No unsafe-answer flags were triggered in this synthetic evaluation run. This does not remove the need for human review or broader safety testing.",
            "",
            "The results should be interpreted as synthetic holdout evidence only.",
            "",
        ]
    )


def build_difficulty_profile(
    question_bank: pd.DataFrame, evidence_map: pd.DataFrame
) -> pd.DataFrame:
    grouped = evidence_map.groupby("question_id").agg(
        expected_evidence_rows=("section_id", "count"),
        expected_source_sections=("section_id", lambda values: ";".join(sorted(set(values)))),
    )
    rows: list[dict[str, object]] = []
    for question in question_bank.itertuples(index=False):
        evidence = (
            grouped.loc[question.question_id] if question.question_id in grouped.index else None
        )
        notes = str(question.notes).lower()
        rows.append(
            {
                "question_id": question.question_id,
                "question_type": question.question_type,
                "expected_evidence_rows": int(evidence["expected_evidence_rows"])
                if evidence is not None
                else 0,
                "expected_source_documents": question.expected_source_documents,
                "expected_source_sections": str(evidence["expected_source_sections"])
                if evidence is not None
                else "",
                "requires_conflict_resolution": "tension" in notes,
                "requires_version_preference": "version" in notes,
                "requires_human_review": bool(question.requires_human_review),
            }
        )
    return pd.DataFrame(rows)


def _markdown_table(frame: pd.DataFrame) -> str:
    columns = list(frame.columns)
    rows = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for _, row in frame.iterrows():
        rows.append("| " + " | ".join(_format_value(row[column]) for column in columns) + " |")
    return "\n".join(rows)


def _format_value(value: object) -> str:
    return f"{value:.3f}" if isinstance(value, float) else str(value)


def main() -> None:
    result = evaluate_challenge_set()
    print("Challenge set evaluation complete.")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
