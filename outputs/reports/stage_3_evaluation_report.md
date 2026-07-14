# Stage 3 evaluation report

Stage 3 evaluates the local TF-IDF RAG baseline with deterministic rule-based checks.

## Overall scorecard

- Questions evaluated: 60
- Overall pass rate: 0.850
- Retrieval hit rate: 1.000
- Mean citation precision: 0.900
- Mean citation recall: 0.900
- Mean faithfulness score: 0.985
- Human review match rate: 1.000
- Safety note: no unsafe-answer flags were triggered in this synthetic evaluation run. This does not remove the need for human review or broader safety testing.

## Results by question type

| question_type | questions | overall_pass_rate | retrieval_hit_rate | mean_retrieval_precision | mean_retrieval_recall | mean_reciprocal_rank | mean_citation_precision | mean_citation_recall | mean_faithfulness | refusal_correct_rate | safety_flag_rate | human_review_match_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| adversarial | 10 | 1.000 | n/a | n/a | n/a | n/a | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| ambiguous | 10 | 1.000 | n/a | n/a | n/a | n/a | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| factual | 20 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| multi_hop | 10 | 0.100 | 1.000 | 0.300 | 0.750 | 0.683 | 0.400 | 0.400 | 0.909 | 1.000 | 0.000 | 1.000 |
| refusal | 10 | 1.000 | n/a | n/a | n/a | n/a | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |

## Notable error patterns

- retrieval did not cover all expected evidence; citation support did not match expected evidence: 5
- citation support did not match expected evidence: 4

## Human review queue

- Queue size: 40
- Queue rule: expected human review, safety flag or failed overall rule-based check.

## Limitations

- TF-IDF is a lexical retrieval baseline.
- Mock generation is deterministic and controlled.
- Deterministic faithfulness checks are useful for screening but are not a substitute for expert review.
- Synthetic corpus results are not field performance claims.
- A zero safety flag rate in this synthetic run does not mean the system has no safety risk.

## Recommended Stage 4 improvements

- Add governance artefacts that reference the evaluation outputs.
- Add Docker and continuous checks without requiring paid APIs.
- Add architecture diagrams and release checks.
