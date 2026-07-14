import json

from rag_eval_gov.security.security_events import SecurityEvent, write_security_events


def test_security_events_write_jsonl(tmp_path) -> None:
    path = tmp_path / "events.jsonl"
    write_security_events(
        [SecurityEvent("test_event", "low", "message", "test", ["flag"])],
        path,
    )
    row = json.loads(path.read_text(encoding="utf-8").strip())
    assert row["event_type"] == "test_event"
    assert row["flags"] == ["flag"]
