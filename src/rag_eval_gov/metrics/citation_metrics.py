"""Citation metrics grounded in the evidence map."""

from __future__ import annotations

import re
from collections.abc import Iterable

import pandas as pd

from rag_eval_gov.metrics.retrieval_metrics import build_expected_evidence

CITATION_PATTERN = re.compile(r"\[([^:\]]+):([^\]]+)\]")


def parse_citation_labels(citations: object) -> set[str]:
    if citations is None:
        return set()
    labels = citations if isinstance(citations, Iterable) and not isinstance(citations, str) else []
    parsed: set[str] = set()
    for label in labels:
        match = CITATION_PATTERN.fullmatch(str(label))
        if match:
            parsed.add(f"{match.group(1)}:{match.group(2)}")
    return parsed


def evaluate_citations(answers: pd.DataFrame, evidence_map: pd.DataFrame) -> pd.DataFrame:
    expected = build_expected_evidence(evidence_map)
    rows: list[dict[str, object]] = []
    for answer in answers.itertuples(index=False):
        expected_sections = expected.get(answer.question_id)
        expected_set = expected_sections.section_keys if expected_sections else set()
        cited_set = parse_citation_labels(answer.citations)
        supported = cited_set & expected_set
        unsupported = cited_set - expected_set
        missing = expected_set - cited_set
        precision = (
            len(supported) / len(cited_set) if cited_set else (1.0 if not expected_set else 0.0)
        )
        recall = (
            len(supported) / len(expected_set) if expected_set else (1.0 if not cited_set else 0.0)
        )
        rows.append(
            {
                "question_id": answer.question_id,
                "citation_labels": sorted(cited_set),
                "expected_citation_labels": sorted(expected_set),
                "citation_precision": precision,
                "citation_recall": recall,
                "supported_citation_count": len(supported),
                "unsupported_citation_count": len(unsupported),
                "missing_citation_count": len(missing),
                "citation_overclaim_flag": len(unsupported) > 0,
                "citation_pass": not unsupported and not missing,
            }
        )
    return pd.DataFrame(rows)


def citation_summary(citation_metrics: pd.DataFrame) -> dict[str, float]:
    return {
        "mean_citation_precision": float(citation_metrics["citation_precision"].mean()),
        "mean_citation_recall": float(citation_metrics["citation_recall"].mean()),
        "unsupported_citation_count": float(citation_metrics["unsupported_citation_count"].sum()),
        "missing_citation_count": float(citation_metrics["missing_citation_count"].sum()),
    }
