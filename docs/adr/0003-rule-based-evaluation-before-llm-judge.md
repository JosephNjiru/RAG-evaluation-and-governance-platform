# ADR 0003: Rule-based evaluation before LLM judge

## Status

Accepted.

## Decision

Stage 3 uses deterministic rule-based judging by default. LLM judge support is only an optional interface.

## Reason

Rule-based checks are auditable, repeatable and free of provider cost. LLM judges require calibration and bias checks before use.
