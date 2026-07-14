# Source-conflict and versioning

RAG systems can retrieve sources that appear to be in tension. The project includes challenge questions for policy tension, versioning and stale-information handling.

## Preference rules

- Prefer newer content when version and date metadata clearly support it.
- Prefer a specific policy over general guidance.
- Prefer governance approval rules when escalation or restricted access is involved.
- Route unresolved tension to human review.

## Current limitation

The deterministic generator does not perform expert conflict resolution. The challenge set checks whether retrieval brings the right evidence into view, but human review remains necessary for final interpretation.
