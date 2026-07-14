---
document_id: DOC-007
title: RAG Evaluation Procedure
version: "1.0"
date: "2026-01-26"
owner: Evaluation Lead
risk_domain: evaluation
---

## EVAL-PROC-001 Retrieval assessment

Retrieval is assessed with question-level evidence expectations, top-k hit rate, reciprocal rank and coverage by question type.

## EVAL-PROC-002 Faithfulness assessment

An answer is faithful only when its material claims are supported by cited evidence and no external facts are added.

## EVAL-PROC-003 Refusal assessment

A refusal is correct when the corpus does not support the requested answer and the response explains the evidence gap without inventing facts.
