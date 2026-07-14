from pathlib import Path

import pandas as pd

from scripts.build_vector_index import build_vector_index
from scripts.run_rag_batch import run_rag_batch

ROOT = Path(__file__).resolve().parents[1]


def test_stage2_batch_rag_outputs_schema_valid_records() -> None:
    build_summary = build_vector_index(ROOT)
    run_summary = run_rag_batch(ROOT)
    answers_path = ROOT / "outputs/answers/rag_answers.parquet"
    rows = pd.read_parquet(answers_path)

    assert build_summary["chunks"] >= 10
    assert run_summary["answers"] == 60
    assert len(rows) == 60
    required_columns = {
        "question_id",
        "question_text",
        "answer_text",
        "retrieved_context_ids",
        "citations",
        "refusal_flag",
        "confidence_label",
        "risk_level",
        "requires_human_review",
        "generation_mode",
        "timestamp",
    }
    assert required_columns <= set(rows.columns)
    assert rows.loc[rows["question_id"].str.startswith("QR-"), "refusal_flag"].all()
    answerable = rows[rows["question_id"].str.startswith(("QF-", "QM-"))]
    assert (answerable["citations"].map(len) > 0).all()
