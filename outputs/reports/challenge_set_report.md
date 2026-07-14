# Challenge set report

The challenge set is a post-improvement holdout set. It is not used to tune retrieval.

The challenge set has a different difficulty profile from the original 60-question benchmark. It should not be treated as a direct replacement for the original multi-hop benchmark. The original 60-question evaluation remains the main baseline comparison.

| question_type | questions | overall_pass_rate | retrieval_hit_rate | mean_retrieval_precision | mean_retrieval_recall | mean_reciprocal_rank | mean_citation_precision | mean_citation_recall | mean_faithfulness | refusal_correct_rate | safety_flag_rate | human_review_match_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| overall | 15 | 0.933 | 1.000 | 0.309 | 1.000 | 1.000 | 0.967 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| adversarial | 2 | 1.000 | n/a | n/a | n/a | n/a | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| factual | 4 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| multi_hop | 7 | 0.857 | 1.000 | 0.371 | 1.000 | 1.000 | 0.929 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| refusal | 2 | 1.000 | n/a | n/a | n/a | n/a | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |

## Difficulty profile summary

| question_type | questions | mean_expected_evidence_rows | human_review_required | conflict_resolution_required | version_preference_required |
| --- | --- | --- | --- | --- | --- |
| adversarial | 2 | 0.000 | 2 | 0 | 0 |
| factual | 4 | 1.000 | 1 | 1 | 3 |
| multi_hop | 7 | 1.857 | 5 | 2 | 0 |
| refusal | 2 | 0.000 | 2 | 0 | 0 |

## Safety interpretation

No unsafe-answer flags were triggered in this synthetic evaluation run. This does not remove the need for human review or broader safety testing.

The results should be interpreted as synthetic holdout evidence only.
