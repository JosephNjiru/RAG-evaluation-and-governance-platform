"""Smoke test the local FastAPI service without starting a network server."""
# ruff: noqa: E402

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient

from rag_eval_gov.api.main import app


def smoke_test_api() -> dict[str, object]:
    """Exercise the Stage 4 API endpoints against local assets."""

    client = TestClient(app)
    health = client.get("/health")
    health.raise_for_status()
    summary = client.get("/summary")
    summary.raise_for_status()
    answer = client.post(
        "/question",
        json={
            "question_id": "api_smoke_test",
            "question_text": "What review is required for high risk AI decisions?",
            "question_type": "factual",
            "risk_level": "medium",
            "requires_human_review": False,
        },
    )
    answer.raise_for_status()
    evaluation = client.post("/evaluate", json={"question_id": "QF-001"})
    evaluation.raise_for_status()
    queue = client.get("/human-review-queue")
    queue.raise_for_status()
    return {
        "health": health.json()["status"],
        "questions": summary.json()["questions"],
        "answer_refusal": answer.json()["refusal_flag"],
        "evaluation_question_id": evaluation.json()["question_id"],
        "human_review_queue": len(queue.json()),
    }


def main() -> None:
    result = smoke_test_api()
    print("API smoke test passed.")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
