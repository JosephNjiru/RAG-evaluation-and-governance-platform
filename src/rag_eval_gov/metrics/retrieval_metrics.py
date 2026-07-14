"""Retrieval metrics grounded in the evidence map."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class ExpectedEvidence:
    document_ids: set[str]
    section_keys: set[str]


def section_key(document_id: str, section_id: str) -> str:
    return f"{document_id}:{section_id}"


def build_expected_evidence(evidence_map: pd.DataFrame) -> dict[str, ExpectedEvidence]:
    expected: dict[str, ExpectedEvidence] = {}
    for question_id, group in evidence_map.groupby("question_id"):
        expected[question_id] = ExpectedEvidence(
            document_ids=set(group["document_id"].astype(str)),
            section_keys={
                section_key(row.document_id, row.section_id)
                for row in group[["document_id", "section_id"]].itertuples(index=False)
            },
        )
    return expected


def evaluate_retrieval(
    question_bank: pd.DataFrame,
    evidence_map: pd.DataFrame,
    retrieval_results: pd.DataFrame,
    k: int = 5,
) -> pd.DataFrame:
    """Evaluate top-k retrieval against expected evidence sections."""

    expected = build_expected_evidence(evidence_map)
    rows: list[dict[str, object]] = []
    for question in question_bank.itertuples(index=False):
        question_id = str(question.question_id)
        retrieved = retrieval_results[retrieval_results["query_id"] == question_id].sort_values(
            "rank"
        )
        retrieved_top = retrieved.head(k)
        expected_item = expected.get(question_id, ExpectedEvidence(set(), set()))
        retrieved_doc_ids = list(retrieved_top["document_id"].astype(str))
        retrieved_section_keys = [
            section_key(row.document_id, row.section_id)
            for row in retrieved_top[["document_id", "section_id"]].itertuples(index=False)
        ]
        matched_sections = [
            item for item in retrieved_section_keys if item in expected_item.section_keys
        ]
        first_match_rank = _first_match_rank(retrieved_top, expected_item.section_keys)
        denominator = max(len(retrieved_top), 1)
        expected_count = len(expected_item.section_keys)
        precision_at_k = len(set(matched_sections)) / denominator
        recall_at_k = len(set(matched_sections)) / expected_count if expected_count > 0 else None
        rows.append(
            {
                "question_id": question_id,
                "question_type": question.question_type,
                "expected_document_ids": sorted(expected_item.document_ids),
                "expected_section_ids": sorted(expected_item.section_keys),
                "retrieved_document_ids": retrieved_doc_ids,
                "retrieved_section_ids": retrieved_section_keys,
                "retrieval_precision_at_k": precision_at_k,
                "retrieval_recall_at_k": recall_at_k,
                "mean_reciprocal_rank": 1 / first_match_rank if first_match_rank else 0.0,
                "hit_rate": first_match_rank is not None,
                "evidence_coverage": recall_at_k,
                "top_k_source_document_match": bool(
                    set(retrieved_doc_ids) & expected_item.document_ids
                ),
                "section_level_evidence_match": len(set(matched_sections)),
                "retrieval_pass": expected_count == 0
                or len(set(matched_sections)) == expected_count,
            }
        )
    return pd.DataFrame(rows)


def _first_match_rank(retrieved: pd.DataFrame, expected_sections: set[str]) -> int | None:
    for row in retrieved.itertuples(index=False):
        if section_key(row.document_id, row.section_id) in expected_sections:
            return int(row.rank)
    return None


def retrieval_summary(retrieval_metrics: pd.DataFrame) -> dict[str, float]:
    answerable = retrieval_metrics[retrieval_metrics["expected_section_ids"].map(len) > 0]
    if answerable.empty:
        return {
            "mean_precision_at_k": 0.0,
            "mean_recall_at_k": 0.0,
            "mean_reciprocal_rank": 0.0,
            "hit_rate": 0.0,
        }
    return {
        "mean_precision_at_k": float(answerable["retrieval_precision_at_k"].mean()),
        "mean_recall_at_k": float(answerable["retrieval_recall_at_k"].mean()),
        "mean_reciprocal_rank": float(answerable["mean_reciprocal_rank"].mean()),
        "hit_rate": float(answerable["hit_rate"].mean()),
    }
