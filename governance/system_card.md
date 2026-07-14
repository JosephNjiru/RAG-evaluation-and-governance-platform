# System card

## System purpose

The RAG Evaluation and Governance Platform evaluates retrieval-augmented generation behaviour over a synthetic corpus. It measures retrieval quality, citation support, deterministic faithfulness signals, refusal behaviour, safety checks, human review needs and governance readiness.

## Intended use

- Build a local RAG evaluation baseline.
- Demonstrate source traceability from corpus sections to answer citations.
- Identify weak retrieval, missing citations, unsupported answers and review needs.
- Support governance artefacts for audit and release review.

## Non-intended use

- Final judgement of a live AI system without additional validation.
- Legal, medical, financial or safety-critical decision support.
- Evaluation of private corpora without privacy review.
- Benchmark claims across providers or model families.

## Inputs and outputs

Inputs are synthetic Markdown documents, question records, reference answers, evidence rows, rubrics and risk taxonomy files. Outputs include answer records, retrieval rows, evaluation results, summary tables, reports, dashboard files and review queues.

## Evaluation method

The platform uses TF-IDF retrieval, deterministic mock generation, evidence-map comparison, citation metrics, rule-based faithfulness screening, refusal checks, safety checks and rubric scoring.

## Key results

- Questions evaluated: 60
- Overall pass rate: 0.850
- Factual pass rate: 1.000
- Multi-hop pass rate: 0.100
- Citation precision: 0.900
- Citation recall: 0.900
- Faithfulness score: 0.985
- Human review match rate: 1.000
- Safety flag rate: 0.000

## Limitations

The corpus is synthetic. TF-IDF is lexical. The generator is deterministic. The multi-hop score is weak. Faithfulness checks are screening checks, not final human judgement.

## Human review role

Human review is required for high-risk, ambiguous, unsupported, adversarial, failed or disputed records.
