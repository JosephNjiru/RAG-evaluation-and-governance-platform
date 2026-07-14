# Security test plan

## Local commands

```bash
python -m uv run python scripts/run_security_checks.py
python -m uv run python scripts/security_smoke_test.py
python -m uv run pytest
python -m uv run ruff check .
python -m uv run ruff format --check .
```

## Test coverage

- Input security checks direct prompt injection, secret requests, unsupported advice and malformed input.
- Context security checks retrieved text with malicious instructions.
- Output security checks missing citations, citations outside retrieved context, secret-like output and overconfidence.
- Secret scanner checks likely secrets and sensitive data patterns.
- API smoke test checks normal input, prompt injection input, secret request input and malformed evaluation payloads.

## Optional dependency scan

If `pip-audit` is available, run:

```bash
python -m uv run pip-audit
```

This command is optional and is not required for the default local test suite.
