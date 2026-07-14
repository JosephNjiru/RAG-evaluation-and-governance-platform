"""Security policy constants for local RAG checks."""

from __future__ import annotations

MAX_INPUT_CHARS = 4000
REQUEST_SIZE_LIMIT_BYTES = 16_384
LOCAL_CORS_ORIGINS = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8080",
]
HIGH_RISK_FLAGS = {
    "instruction_override",
    "secret_request",
    "unsupported_advice",
    "malformed_input",
    "unbounded_input",
}
