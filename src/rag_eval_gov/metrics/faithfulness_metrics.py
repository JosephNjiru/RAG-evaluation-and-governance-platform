"""Deterministic faithfulness checks."""

from __future__ import annotations

import re

import pandas as pd

from rag_eval_gov.metrics.citation_metrics import parse_citation_labels
from rag_eval_gov.metrics.retrieval_metrics import section_key

TOKEN_PATTERN = re.compile(r"[a-z0-9]+")
SENTENCE_PATTERN = re.compile(r"(?<=[.!?])\s+")


def token_set(text: str) -> set[str]:
    return set(TOKEN_PATTERN.findall(text.lower()))


def overlap_score(left: str, right: str) -> float:
    left_tokens = token_set(left)
    if not left_tokens:
        return 0.0
    right_tokens = token_set(right)
    return len(left_tokens & right_tokens) / len(left_tokens)


def evaluate_faithfulness(
    answers: pd.DataFrame,
    evidence_map: pd.DataFrame,
    reference_answers: pd.DataFrame,
) -> pd.DataFrame:
    evidence_lookup = {
        section_key(row.document_id, row.section_id): row.evidence_text
        for row in evidence_map.itertuples(index=False)
    }
    reference_lookup = {
        row.question_id: row.reference_answer for row in reference_answers.itertuples(index=False)
    }
    rows: list[dict[str, object]] = []
    for answer in answers.itertuples(index=False):
        cited_keys = parse_citation_labels(answer.citations)
        cited_text = " ".join(evidence_lookup.get(key, "") for key in cited_keys)
        answer_text = str(answer.answer_text)
        answer_body = answer_text.removeprefix("Based on the retrieved evidence: ").strip()
        sentence_scores = [
            overlap_score(sentence, cited_text)
            for sentence in SENTENCE_PATTERN.split(answer_body)
            if sentence.strip()
        ]
        cited_overlap = overlap_score(answer_body, cited_text)
        reference_overlap = overlap_score(
            answer_body,
            str(reference_lookup.get(answer.question_id, "")),
        )
        unsupported_claim_flag = not bool(answer.refusal_flag) and (
            not cited_keys or cited_overlap < 0.45
        )
        refusal_consistent = bool(answer.refusal_flag) and not cited_keys
        faithfulness_score = 1.0 if refusal_consistent else max(cited_overlap, reference_overlap)
        rows.append(
            {
                "question_id": answer.question_id,
                "cited_evidence_overlap": cited_overlap,
                "answer_sentence_support": min(sentence_scores) if sentence_scores else 0.0,
                "reference_answer_overlap": reference_overlap,
                "unsupported_claim_flag": unsupported_claim_flag,
                "refusal_consistency": refusal_consistent,
                "faithfulness_score": faithfulness_score,
                "faithfulness_pass": faithfulness_score >= 0.5 and not unsupported_claim_flag,
            }
        )
    return pd.DataFrame(rows)
