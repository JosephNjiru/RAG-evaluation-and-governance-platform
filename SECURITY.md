# Security

Stage 1 is local-first and does not require secrets or paid API credentials.

Do not commit:

- API keys, tokens or credentials
- private documents or personal records
- local `.env` files
- generated environments, caches or large model binaries
- unreviewed logs containing prompts or evaluation traces

Security testing in later stages will cover prompt injection exposure, unsupported answers, citation misuse, sensitive information handling and human review bypass.
