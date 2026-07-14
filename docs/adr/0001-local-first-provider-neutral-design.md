# ADR 0001: Local-first provider-neutral design

## Status

Accepted.

## Decision

The default system runs locally with deterministic generation and local retrieval. Paid model providers are not required.

## Reason

Local execution keeps costs, secrets and provider drift out of the baseline. Optional providers can be added later behind interfaces.
