# Research audit trail

## Research problem

RAG systems need evaluation beyond answer fluency. Retrieval quality, answer faithfulness, citation support, refusal behaviour, safety handling and human review needs can fail independently.

## Evaluation design

The project starts with a corpus, question taxonomy, reference answers, evidence map and rubrics before building the RAG baseline. This makes the evaluation target explicit.

## Corpus design

The corpus contains synthetic Markdown documents about organisational AI policy, data governance, security, monitoring, incident response, evaluation, analytics and privacy handling.

## Question taxonomy

The question bank includes factual, multi-hop, ambiguous, refusal and adversarial questions. Answerable questions are mapped to evidence. Unsupported questions are expected to refuse or request review.

## Metric families

Metrics cover retrieval, citation support, deterministic faithfulness screening, refusal behaviour, safety checks, human review match and rubric scores.

## Baseline system

The baseline uses section-aware chunks, a TF-IDF vector index and a deterministic mock generator. It is intended to be transparent and reproducible.

## Stage 3 results

- Questions evaluated: 60
- Overall pass rate: 0.850
- Factual pass rate: 1.000
- Multi-hop pass rate: 0.100
- Citation precision: 0.900
- Citation recall: 0.900
- Faithfulness score: 0.985
- Human review match rate: 1.000
- Safety flag rate: 0.000
- Current full validation suite: 54 tests passed.

No unsafe-answer flags were triggered in this synthetic evaluation run. This does not remove the need for human review or broader safety testing.

## Error pattern

The TF-IDF baseline performs strongly on factual questions but poorly on multi-hop evidence assembly. The evaluation engine exposes this weakness through question-type breakdowns, retrieval evidence and citation metrics.

Stage 4 improved the multi-hop pass rate from 0.100 to 0.200 on the original 60-question benchmark. The challenge set multi-hop pass rate is higher at 0.857, but that set has a different difficulty profile and is not a replacement for the original multi-hop benchmark.

## Limitations

The corpus is synthetic, the generator is deterministic, TF-IDF is lexical and rule-based faithfulness checks are screening checks.

## Reproducibility commands

Run the commands in `docs/reproducibility.md` to rebuild the index, answer records, evaluation outputs and dashboard.

## Future article potential

The project could support a future research article about auditable RAG evaluation design. This repository does not contain an article draft and does not claim publication.
