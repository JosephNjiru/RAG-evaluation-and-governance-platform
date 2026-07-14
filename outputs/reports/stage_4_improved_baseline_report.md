# Stage 4 improved baseline report

The original TF-IDF baseline is preserved as Baseline A.

- Baseline A overall pass rate: 0.850
- Baseline A multi-hop pass rate: 0.100
- Improved Baseline E overall pass rate: 0.867
- Improved Baseline E multi-hop pass rate: 0.200

The improved method uses text-only query intent, query decomposition, hybrid lexical scoring and diversified reranking. It does not use the evidence map during retrieval or generation.

The comparison remains a local synthetic-corpus result and does not remove the need for human review.
