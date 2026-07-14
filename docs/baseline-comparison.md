# Baseline comparison

## Original baseline

Baseline A is the original TF-IDF lexical retrieval baseline. It is preserved in the Stage 3 outputs and remains visible in the ablation report.

Original Stage 3 result:

- Overall pass rate: 0.850
- Factual pass rate: 1.000
- Multi-hop pass rate: 0.100
- Citation precision: 0.900
- Citation recall: 0.900

## Improved retrieval layer

Stage 4 adds metadata weighting, BM25-style lexical retrieval, hybrid scoring, query decomposition and diversified reranking. The improved layer is reported separately as Baseline E.

Run `python -m uv run python scripts/run_retrieval_ablation.py` to regenerate the comparison.

## What improved

The current Baseline E result raised overall pass rate from 0.850 to 0.867 and multi-hop pass rate from 0.100 to 0.200. This is a modest improvement, not a solved multi-hop retrieval problem.

## What remains weak

The improved methods are still lexical. They may miss paraphrases, implied relationships and source conflicts that require judgement.

The challenge set currently passes at 0.933 overall on 15 synthetic holdout questions, with a multi-hop pass rate of 0.857. That set has a different difficulty profile from the original 60-question benchmark and should not be treated as a direct replacement for the original multi-hop benchmark. The original 60-question evaluation remains the main baseline comparison.

## Governance implication

Weak multi-hop evidence assembly is a governance signal. It should route records to review, guide retrieval improvements and prevent overstated claims about RAG quality.

## Human review

Improvement does not remove human review. High-risk, ambiguous, unsupported, adversarial and failed records still need human judgement.
