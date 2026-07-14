# Threats to validity

## Synthetic corpus

The corpus is public-safe and synthetic. It does not represent the full ambiguity, scale or messiness of a live organisational knowledge base.

## Deterministic mock generator

The mock generator is useful for controlled evaluation, but it does not represent the behaviour of a deployed language model.

## TF-IDF lexical retrieval

TF-IDF is transparent and reproducible, but it relies on term overlap. It can miss semantic matches and performs poorly on the current multi-hop questions.

## Multi-hop evidence assembly

The baseline often fails to assemble all required evidence for multi-hop questions. This is reported as a baseline finding.

## Metric validity limits

Deterministic metrics are auditable but limited. They can miss paraphrase support, implied claims and subtle citation misuse.

## Rule-based judge limits

The rule-based judge applies fixed rules. It is consistent, but it cannot replace expert review for high-risk outputs.

## Future LLM judge risks

An optional LLM judge would need calibration against human annotations. Risks include bias, inconsistency, model version changes, cost and overconfidence.

## Generalisability

Stage 3 results are valid for this synthetic corpus and local baseline only. They should not be interpreted as field performance on other corpora or generators.
