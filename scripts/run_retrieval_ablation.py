"""Run retrieval ablation experiments for Stage 4."""
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
from rag_eval_gov.pipeline.batch_answer import write_answer_records, write_retrieval_records
from rag_eval_gov.retrieval.retrieval_experiment import (
    default_run_config,
    generate_answers_for_retrieval,
    load_default_questions,
    run_retrieval_method,
    write_run_manifest,
)
from scripts.build_vector_index import build_vector_index
from scripts.run_rag_batch import run_rag_batch
from scripts.validate_stage1_assets import validate_stage1_assets

METHODS = [
    ("baseline_a_tfidf", "Baseline A: TF-IDF lexical retrieval"),
    ("baseline_b_metadata_weighted_tfidf", "Baseline B: metadata-weighted TF-IDF"),
    ("baseline_c_bm25", "Baseline C: BM25 lexical retrieval"),
    ("baseline_d_hybrid", "Baseline D: hybrid lexical retrieval"),
    (
        "baseline_e_decomposition_diversified",
        "Baseline E: multi-hop decomposition plus diversified reranking",
    ),
]


def run_retrieval_ablation(root: Path = ROOT) -> dict[str, object]:
    validate_stage1_assets(root)
    if not (root / "data/processed/chunks.parquet").exists():
        build_vector_index(root)
    if not (root / "outputs/answers/rag_answers.parquet").exists():
        run_rag_batch(root)

    question_bank = pd.read_csv(root / "data/evaluation/question_bank.csv").fillna("")
    reference_answers = pd.read_csv(root / "data/evaluation/reference_answers.csv").fillna("")
    evidence_map = pd.read_csv(root / "data/evaluation/evidence_map.csv").fillna("")
    questions = load_default_questions(root)
    output_rows: list[pd.DataFrame] = []
    summary_rows: list[pd.DataFrame] = []
    run_configs = []

    for method, label in METHODS:
        retrieval_rows = run_retrieval_method(
            method,
            questions,
            chunks_path=root / "data/processed/chunks.parquet",
            index_dir=root / "data/index",
            top_k=5,
        )
        answers = generate_answers_for_retrieval(questions, retrieval_rows)
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
        results.insert(0, "baseline_label", label)
        results.insert(0, "retrieval_method", method)
        output_rows.append(results)
        summary = build_summary_table(results)
        summary.insert(0, "baseline_label", label)
        summary.insert(0, "retrieval_method", method)
        summary_rows.append(summary)
        run_configs.append(
            default_run_config(
                run_id=method,
                run_label=label,
                retrieval_method=method,
                top_k=5,
                decomposition=method == "baseline_e_decomposition_diversified",
                reranking="diversified"
                if method == "baseline_e_decomposition_diversified"
                else "score_rank",
            )
        )

        if method == "baseline_e_decomposition_diversified":
            write_answer_records(answers, root / "outputs/answers/improved_rag_answers.parquet")
            write_retrieval_records(
                retrieval_rows,
                root / "outputs/answers/improved_retrieval_results.parquet",
            )

    results_table = pd.concat(output_rows, ignore_index=True)
    summary_table = pd.concat(summary_rows, ignore_index=True)
    evaluation_dir = root / "outputs/evaluation"
    report_dir = root / "outputs/reports"
    evaluation_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)
    results_table.to_csv(evaluation_dir / "retrieval_ablation_results.csv", index=False)
    summary_table.to_csv(evaluation_dir / "retrieval_ablation_by_question_type.csv", index=False)
    write_run_manifest(run_configs, evaluation_dir / "run_manifest.csv")
    report_text = build_ablation_report(summary_table)
    (report_dir / "retrieval_ablation_report.md").write_text(report_text, encoding="utf-8")
    (report_dir / "baseline_comparison_report.md").write_text(report_text, encoding="utf-8")
    return {
        "methods": len(METHODS),
        "rows": len(results_table),
        "summary_rows": len(summary_table),
    }


def build_ablation_report(summary: pd.DataFrame) -> str:
    lines = [
        "# Retrieval ablation report",
        "",
        "Baseline A is preserved as the original TF-IDF lexical retrieval result.",
        "",
        _markdown_table(
            summary[
                [
                    "baseline_label",
                    "question_type",
                    "questions",
                    "overall_pass_rate",
                    "mean_retrieval_recall",
                    "mean_reciprocal_rank",
                    "mean_citation_precision",
                    "mean_citation_recall",
                ]
            ].fillna("n/a")
        ),
        "",
        "## Interpretation",
        "",
        "The ablation keeps the weak original multi-hop result visible. Improved retrieval methods are compared separately and should not be read as replacing Baseline A.",
        "",
        "Human review remains necessary because retrieval improvements do not prove that every answer claim is complete, current or policy-safe.",
        "",
    ]
    return "\n".join(lines)


def _markdown_table(frame: pd.DataFrame) -> str:
    columns = list(frame.columns)
    rows = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for _, row in frame.iterrows():
        values = []
        for column in columns:
            value = row[column]
            if isinstance(value, float):
                values.append(f"{value:.3f}")
            else:
                values.append(str(value))
        rows.append("| " + " | ".join(values) + " |")
    return "\n".join(rows)


def main() -> None:
    result = run_retrieval_ablation()
    print("Retrieval ablation complete.")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
