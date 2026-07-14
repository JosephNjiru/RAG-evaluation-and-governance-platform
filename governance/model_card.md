# Model card

## Model description

The default answer service is a deterministic mock generator. It is not an LLM. It answers from retrieved evidence or refuses when the question type or evidence state requires refusal.

## Retrieval model

Retrieval uses a local TF-IDF baseline over section-linked chunks. The index includes title, section heading, risk domain and section text for lexical matching.

## Generation behaviour

- Factual questions use the top retrieved evidence chunk.
- Multi-hop questions use the top two retrieved chunks.
- Ambiguous, refusal and adversarial questions refuse by design.
- Citations are formatted as source section labels.

## Strengths

- Deterministic and repeatable.
- No paid APIs or keys.
- Easy to inspect.
- Useful for CI and evaluation tests.

## Limitations

The generator is deliberately simple. It does not reason like a language model and should not be treated as a substitute for live model evaluation.
