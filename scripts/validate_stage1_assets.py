"""Validate Stage 1 assets."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from rag_eval_gov.config.load_config import load_config
from rag_eval_gov.config.schemas import (
    ANSWERABLE_QUESTION_TYPES,
    APPROVED_QUESTION_TYPES,
    APPROVED_RISK_LEVELS,
    CorpusConfig,
    EvidenceMapRecord,
    ProjectConfig,
    QuestionRecord,
    ReferenceAnswerRecord,
    RiskTaxonomyConfig,
    RubricConfig,
)
from rag_eval_gov.corpus.build_corpus import load_corpus

ROOT = Path(__file__).resolve().parents[1]


def read_csv_records(path: Path) -> list[dict]:
    return pd.read_csv(path).fillna("").to_dict(orient="records")


def validate_stage1_assets(root: Path = ROOT) -> dict[str, object]:
    configs = root / "configs"
    data = root / "data/evaluation"
    load_config(configs / "project.yaml", ProjectConfig)
    corpus_config = load_config(configs / "corpus.yaml", CorpusConfig)
    load_config(configs / "evaluation_rubrics.yaml", RubricConfig)
    load_config(configs / "risk_taxonomy.yaml", RiskTaxonomyConfig)

    corpus = load_corpus(root / corpus_config.source_path)
    if (
        not corpus_config.expected_document_count_min
        <= len(corpus)
        <= corpus_config.expected_document_count_max
    ):
        raise ValueError("corpus document count is outside the configured range")

    question_records = [
        QuestionRecord.model_validate(row) for row in read_csv_records(data / "question_bank.csv")
    ]
    reference_records = [
        ReferenceAnswerRecord.model_validate(row)
        for row in read_csv_records(data / "reference_answers.csv")
    ]
    evidence_records = [
        EvidenceMapRecord.model_validate(row) for row in read_csv_records(data / "evidence_map.csv")
    ]

    question_ids = [record.question_id for record in question_records]
    if len(question_ids) != len(set(question_ids)):
        raise ValueError("duplicate question IDs found")
    if len(question_records) < 60:
        raise ValueError("question bank must contain at least 60 questions")

    by_type: dict[str, int] = {}
    for record in question_records:
        if record.question_type not in APPROVED_QUESTION_TYPES:
            raise ValueError(f"unapproved question type: {record.question_type}")
        if record.risk_level not in APPROVED_RISK_LEVELS:
            raise ValueError(f"unapproved risk level: {record.risk_level}")
        by_type[record.question_type] = by_type.get(record.question_type, 0) + 1

    expected_counts = {
        "factual": 20,
        "multi_hop": 10,
        "ambiguous": 10,
        "refusal": 10,
        "adversarial": 10,
    }
    for question_type, minimum in expected_counts.items():
        if by_type.get(question_type, 0) < minimum:
            raise ValueError(f"expected at least {minimum} {question_type} questions")

    answerable_ids = {
        record.question_id
        for record in question_records
        if record.question_type in ANSWERABLE_QUESTION_TYPES
    }
    evidence_question_ids = {record.question_id for record in evidence_records}
    reference_question_ids = {record.question_id for record in reference_records}
    missing_evidence = answerable_ids - evidence_question_ids
    missing_references = answerable_ids - reference_question_ids
    if missing_evidence:
        raise ValueError(f"answerable questions missing evidence: {sorted(missing_evidence)}")
    if missing_references:
        raise ValueError(
            f"answerable questions missing reference answers: {sorted(missing_references)}"
        )

    refusal_ids = {
        record.question_id for record in question_records if record.question_type == "refusal"
    }
    if refusal_ids & evidence_question_ids:
        raise ValueError("refusal questions must not have fabricated supporting evidence")

    adversarial_ids = {
        record.question_id for record in question_records if record.question_type == "adversarial"
    }
    adversarial_subset = {
        QuestionRecord.model_validate(row).question_id
        for row in read_csv_records(data / "adversarial_questions.csv")
    }
    if adversarial_ids != adversarial_subset:
        raise ValueError("adversarial questions are not clearly labelled in the subset file")

    refusal_subset = {
        QuestionRecord.model_validate(row).question_id
        for row in read_csv_records(data / "refusal_questions.csv")
    }
    if refusal_ids != refusal_subset:
        raise ValueError("refusal questions are not clearly labelled in the subset file")

    summary = {
        "corpus_documents": len(corpus),
        "questions": len(question_records),
        "question_counts": by_type,
        "reference_answers": len(reference_records),
        "evidence_rows": len(evidence_records),
        "status": "passed",
    }
    report_path = root / "docs/stage-1-validation-report.md"
    report_path.write_text(
        "\n".join(
            [
                "# Stage 1 validation report",
                "",
                "Validation status: passed.",
                "",
                f"- Corpus documents: {summary['corpus_documents']}",
                f"- Questions: {summary['questions']}",
                f"- Reference answers: {summary['reference_answers']}",
                f"- Evidence rows: {summary['evidence_rows']}",
                f"- Question counts: {summary['question_counts']}",
                "",
                "The validation checked schemas, required fields, duplicate IDs, evidence coverage, refusal evidence absence, adversarial labels and approved risk levels.",
            ]
        ),
        encoding="utf-8",
    )
    return summary


def main() -> None:
    summary = validate_stage1_assets()
    print("Stage 1 validation passed.")
    for key, value in summary.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
