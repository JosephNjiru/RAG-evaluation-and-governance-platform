# Research methods log

## Problem statement

RAG systems need evaluation across retrieval, grounding, citation support, refusal behaviour, safety checks and human review needs.

## Design rationale

The project defines evaluation assets before generation, preserves the original TF-IDF baseline and adds retrieval improvements as a separate ablation layer.

## Corpus design

The corpus is synthetic and public-safe. It covers AI policy, data governance, security, monitoring, incident response, analytics, evaluation, privacy, human review and knowledge-base maintenance.

## Question taxonomy

The original set contains factual, multi-hop, ambiguous, refusal and adversarial questions. The challenge set adds multi-hop, policy-tension, versioning, prompt-injection and unsupported escalation questions.

## Baseline methods

Baseline A is TF-IDF lexical retrieval. It remains the original comparison point.

## Improved retrieval methods

Baselines B to E add metadata weighting, BM25-style scoring, hybrid lexical scoring, query decomposition and diversified reranking.

## Evaluation metrics

Metrics include hit rate, precision at k, recall at k, mean reciprocal rank, section-level evidence match, citation precision, citation recall, pass rate and human review match.

## Leakage controls

The evidence map is used only after retrieval and generation. Tests scan retrieval and generation modules for evidence-map access.

## Challenge set

The challenge set is used after improvement, not for tuning.

## Limitations

The corpus is synthetic, retrieval is lexical, generation is deterministic and rule-based checks do not replace expert review.

## Reproduction

Run the commands in `docs/reproducibility.md`.
