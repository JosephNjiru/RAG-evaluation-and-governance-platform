# Security architecture

The security layer adds local checks around the RAG path.

## Control points

1. Input security checks user questions for override attempts, secret requests, unsupported high-stakes advice, malformed input and large input.
2. Context security treats retrieved text as untrusted evidence and checks for instruction-like content.
3. Prompt construction separates trusted system instructions from untrusted retrieved evidence.
4. Output security validates citations, secret-like strings, excessive confidence and unsafe escalation advice.
5. Secret scanning checks public text artefacts and generated reports.
6. API hardening adds request-size limits, local-only CORS, schema validation and safe error responses.
7. Docker hardening runs the service as a non-root user and avoids copying local environments or `.env` files.

## Boundary

These controls are local security assurance checks. They do not replace a full security review for live deployment.
