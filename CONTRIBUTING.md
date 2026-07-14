# Contributing

This project values clear evidence, reproducibility and plain language.

Before opening a change:

1. Build Stage 1 assets.
2. Run the validation script.
3. Run tests and ruff checks.
4. Check that no secrets, private documents or local cache folders are included.
5. Keep claims tied to generated outputs or cited sources.

Avoid adding paid API requirements to default tests. Optional provider adapters can be proposed later, but local deterministic checks must remain available.
