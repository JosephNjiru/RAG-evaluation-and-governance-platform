# Stage 2 RAG run report

Stage 2 used a local TF-IDF retriever and deterministic mock answer generator.

- Answer records: 60
- Refusal records: 30
- Records with citations: 30
- Generation modes: {'deterministic_mock': 60}
- Refusals by risk level: {'critical': 10, 'high': 10, 'medium': 10}

The mock generator refuses refusal, ambiguous and adversarial questions by design. Supported factual and multi-hop questions receive citations from retrieved chunks.

Known limitation: TF-IDF is a transparent lexical baseline. It does not capture semantic equivalence beyond observed terms.
