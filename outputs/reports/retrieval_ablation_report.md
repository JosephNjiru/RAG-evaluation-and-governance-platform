# Retrieval ablation report

Baseline A is preserved as the original TF-IDF lexical retrieval result.

| baseline_label | question_type | questions | overall_pass_rate | mean_retrieval_recall | mean_reciprocal_rank | mean_citation_precision | mean_citation_recall |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline A: TF-IDF lexical retrieval | overall | 60 | 0.850 | 0.917 | 0.894 | 0.900 | 0.900 |
| Baseline A: TF-IDF lexical retrieval | adversarial | 10 | 1.000 | n/a | n/a | 1.000 | 1.000 |
| Baseline A: TF-IDF lexical retrieval | ambiguous | 10 | 1.000 | n/a | n/a | 1.000 | 1.000 |
| Baseline A: TF-IDF lexical retrieval | factual | 20 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Baseline A: TF-IDF lexical retrieval | multi_hop | 10 | 0.100 | 0.750 | 0.683 | 0.400 | 0.400 |
| Baseline A: TF-IDF lexical retrieval | refusal | 10 | 1.000 | n/a | n/a | 1.000 | 1.000 |
| Baseline B: metadata-weighted TF-IDF | overall | 60 | 0.850 | 0.917 | 0.892 | 0.892 | 0.892 |
| Baseline B: metadata-weighted TF-IDF | adversarial | 10 | 1.000 | n/a | n/a | 1.000 | 1.000 |
| Baseline B: metadata-weighted TF-IDF | ambiguous | 10 | 1.000 | n/a | n/a | 1.000 | 1.000 |
| Baseline B: metadata-weighted TF-IDF | factual | 20 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Baseline B: metadata-weighted TF-IDF | multi_hop | 10 | 0.100 | 0.750 | 0.675 | 0.350 | 0.350 |
| Baseline B: metadata-weighted TF-IDF | refusal | 10 | 1.000 | n/a | n/a | 1.000 | 1.000 |
| Baseline C: BM25 lexical retrieval | overall | 60 | 0.833 | 0.900 | 0.900 | 0.892 | 0.892 |
| Baseline C: BM25 lexical retrieval | adversarial | 10 | 1.000 | n/a | n/a | 1.000 | 1.000 |
| Baseline C: BM25 lexical retrieval | ambiguous | 10 | 1.000 | n/a | n/a | 1.000 | 1.000 |
| Baseline C: BM25 lexical retrieval | factual | 20 | 0.950 | 1.000 | 0.975 | 0.950 | 0.950 |
| Baseline C: BM25 lexical retrieval | multi_hop | 10 | 0.100 | 0.700 | 0.750 | 0.450 | 0.450 |
| Baseline C: BM25 lexical retrieval | refusal | 10 | 1.000 | n/a | n/a | 1.000 | 1.000 |
| Baseline D: hybrid lexical retrieval | overall | 60 | 0.850 | 0.883 | 0.897 | 0.900 | 0.900 |
| Baseline D: hybrid lexical retrieval | adversarial | 10 | 1.000 | n/a | n/a | 1.000 | 1.000 |
| Baseline D: hybrid lexical retrieval | ambiguous | 10 | 1.000 | n/a | n/a | 1.000 | 1.000 |
| Baseline D: hybrid lexical retrieval | factual | 20 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Baseline D: hybrid lexical retrieval | multi_hop | 10 | 0.100 | 0.650 | 0.692 | 0.400 | 0.400 |
| Baseline D: hybrid lexical retrieval | refusal | 10 | 1.000 | n/a | n/a | 1.000 | 1.000 |
| Baseline E: multi-hop decomposition plus diversified reranking | overall | 60 | 0.867 | 0.917 | 0.906 | 0.917 | 0.917 |
| Baseline E: multi-hop decomposition plus diversified reranking | adversarial | 10 | 1.000 | n/a | n/a | 1.000 | 1.000 |
| Baseline E: multi-hop decomposition plus diversified reranking | ambiguous | 10 | 1.000 | n/a | n/a | 1.000 | 1.000 |
| Baseline E: multi-hop decomposition plus diversified reranking | factual | 20 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Baseline E: multi-hop decomposition plus diversified reranking | multi_hop | 10 | 0.200 | 0.750 | 0.717 | 0.500 | 0.500 |
| Baseline E: multi-hop decomposition plus diversified reranking | refusal | 10 | 1.000 | n/a | n/a | 1.000 | 1.000 |

## Interpretation

The ablation keeps the weak original multi-hop result visible. Improved retrieval methods are compared separately and should not be read as replacing Baseline A.

Human review remains necessary because retrieval improvements do not prove that every answer claim is complete, current or policy-safe.
