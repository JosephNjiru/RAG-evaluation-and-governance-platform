# Evaluation limitations

TF-IDF is a lexical baseline. It is transparent and useful for first-pass retrieval, but it can miss semantic matches that do not share terms with the query.

Mock generation is controlled and deterministic. It is useful for testing evaluation plumbing, refusal handling and citation support, but it is not a live model.

Deterministic faithfulness checks are not perfect. Token overlap can miss paraphrases and can over-credit answers that share words without fully supporting the claim.

The corpus is synthetic. Results on this corpus are not field performance claims.

Human review remains necessary for high-risk outputs, ambiguous questions, safety-sensitive cases and any use beyond local evaluation.
