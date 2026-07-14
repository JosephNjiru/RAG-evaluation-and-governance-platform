# Security and privacy notes

## Default security posture

The project runs locally and does not require API keys. The corpus is synthetic and public-safe.

## Risks tested

- Prompt injection attempts.
- Unsupported answer generation.
- Citation misuse.
- Sensitive information exposure.
- Human review bypass.
- Misuse of evaluation scores.

## Controls

- `.env.example` is used for example variables only.
- `.gitignore` and `.dockerignore` exclude local environments, caches, secrets and large model files.
- Quality scan checks secret-like assignments and private planning language.
- Incident response playbook documents response steps for major failure types.
- Local input, context and output security checks flag prompt injection, secret requests, unsafe escalation advice and citation issues.
- API defaults include schema validation, request-size limits, local-only CORS and safe error responses.
- Docker defaults run the API process as a non-root user.

## Privacy boundary

Do not add private documents, real personal information or confidential source text to the public corpus.

## Limitations

The security checks are deterministic screening controls. They do not replace a full security assessment for live systems.
