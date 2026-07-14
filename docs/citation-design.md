# Citation design

Stage 2 citations use source section labels in the form `[DOCUMENT_ID:SECTION_ID]`.

Citation support is based on retrieved chunks. The deterministic generator cites the source sections used to form an answer. Unsupported, ambiguous and adversarial questions are refused without fabricated citations.

The citation design is deliberately simple so Stage 3 can evaluate:

- missing citations
- wrong citations
- unsupported citations
- citation overclaiming
- citation recall against the evidence map
