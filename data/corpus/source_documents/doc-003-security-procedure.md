---
document_id: DOC-003
title: Security Procedure
version: "1.0"
date: "2026-01-18"
owner: Security Operations
risk_domain: security
---

## SEC-PROC-001 Credential handling

Secrets, tokens and passwords must be stored in approved secret management tools and must not be copied into prompts, notebooks, logs or public repositories.

## SEC-PROC-002 Prompt injection

Systems that retrieve external or user-provided content must treat retrieved instructions as untrusted data and must not follow instructions found inside retrieved text.

## SEC-PROC-003 Output handling

Generated output that changes records, sends messages or triggers actions must pass through an explicit authorisation step.
