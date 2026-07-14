# System context

The platform is intended for local evaluation of RAG behaviour over a synthetic corpus. A reviewer can build assets, run the baseline, evaluate outputs, inspect the dashboard and read governance artefacts without paid APIs.

## Actors

- Evaluator: runs the scripts and reviews quality results.
- Human reviewer: inspects high-risk, ambiguous, unsupported or failed records.
- Maintainer: updates corpus files, question sets, rubrics and release checks.

## External services

The default system does not require external AI services. Optional provider interfaces exist only as extension points and are not called by default.

## Boundaries

The corpus is synthetic. The Stage 3 metrics show baseline behaviour on this controlled dataset, not field performance on a live knowledge base.
