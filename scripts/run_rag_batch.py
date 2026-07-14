"""Run the Stage 2 local RAG batch pipeline."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from rag_eval_gov.pipeline.batch_answer import (
    run_batch_with_retrieval,
    write_answer_records,
    write_retrieval_records,
)

ROOT = Path(__file__).resolve().parents[1]


def run_rag_batch(root: Path = ROOT) -> dict[str, object]:
    index_dir = root / "data/index"
    chunks_path = root / "data/processed/chunks.parquet"
    answers_path = root / "outputs/answers/rag_answers.parquet"
    retrieval_path = root / "outputs/answers/retrieval_results.parquet"

    records, retrieval_records = run_batch_with_retrieval(
        question_bank_path=root / "data/evaluation/question_bank.csv",
        index_dir=index_dir,
        chunks_path=chunks_path,
        top_k=5,
    )
    write_answer_records(records, answers_path)
    write_retrieval_records(retrieval_records, retrieval_path)
    rows = pd.DataFrame([record.model_dump(mode="json") for record in records])

    report_path = root / "outputs/reports/stage_2_rag_run_report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(build_report(rows), encoding="utf-8")

    return {
        "answers": len(records),
        "retrieval_rows": len(retrieval_records),
        "refusals": int(rows["refusal_flag"].sum()),
        "answers_with_citations": int((rows["citations"].map(len) > 0).sum()),
        "report_path": str(report_path),
    }


def build_report(rows: pd.DataFrame) -> str:
    counts_by_mode = rows["generation_mode"].value_counts().to_dict()
    refusals_by_risk = rows.groupby("risk_level")["refusal_flag"].sum().astype(int).to_dict()
    return "\n".join(
        [
            "# Stage 2 RAG run report",
            "",
            "Stage 2 used a local TF-IDF retriever and deterministic mock answer generator.",
            "",
            f"- Answer records: {len(rows)}",
            f"- Refusal records: {int(rows['refusal_flag'].sum())}",
            f"- Records with citations: {int((rows['citations'].map(len) > 0).sum())}",
            f"- Generation modes: {counts_by_mode}",
            f"- Refusals by risk level: {refusals_by_risk}",
            "",
            "The mock generator refuses refusal, ambiguous and adversarial questions by design. Supported factual and multi-hop questions receive citations from retrieved chunks.",
            "",
            "Known limitation: TF-IDF is a transparent lexical baseline. It does not capture semantic equivalence beyond observed terms.",
            "",
        ]
    )


def main() -> None:
    summary = run_rag_batch()
    print("Stage 2 RAG batch run complete.")
    for key, value in summary.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
