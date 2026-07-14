# Evaluation card

## Metrics

The platform evaluates retrieval precision and recall, hit rate, mean reciprocal rank, evidence coverage, citation precision and recall, unsupported citations, faithfulness screening, refusal correctness, safety flags, human review match and rubric scores.

## Score interpretation

Scores are screening signals. They identify likely quality problems and support review, but they do not replace expert judgement.

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

## Multi-hop weakness

The TF-IDF baseline performs poorly on multi-hop evidence assembly. This is retained as a baseline finding and should guide later improvements.

## Faithfulness screening limits

Deterministic checks use lexical overlap and cited evidence support. They can miss paraphrases, implied claims and subtle unsupported statements.

## Refusal scoring

Refusal scoring distinguishes correct refusal, false refusal and missed refusal. Ambiguous questions are treated as acceptable refusals when human review is requested.

## Human review queue

Records enter review when they are high risk, ambiguous, unsupported, adversarial, failed or flagged by safety and governance checks.
