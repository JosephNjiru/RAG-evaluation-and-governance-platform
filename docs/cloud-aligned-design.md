# Cloud-aligned design

The platform uses patterns that can map to a managed environment later while remaining local-first now.

## Aligned patterns

- Configuration is separated from code.
- Data assets and generated outputs have stable paths.
- The API exposes health, answer, evaluation summary and human review queue endpoints.
- Docker Compose describes service boundaries.
- CI runs validation, tests, formatting checks and release scans.
- Optional provider interfaces can be extended without changing default local execution.

## Boundary

This repository does not claim deployment to any cloud platform. The design keeps cloud migration paths visible without making a cloud dependency mandatory.
