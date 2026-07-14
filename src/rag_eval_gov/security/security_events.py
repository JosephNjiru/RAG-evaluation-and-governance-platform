"""Security event models and JSONL writer."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class SecurityEvent:
    """One local security event."""

    event_type: str
    severity: str
    message: str
    source: str
    flags: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


def write_security_events(events: list[SecurityEvent], path: Path) -> None:
    """Write security events as JSONL."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for event in events:
            handle.write(json.dumps(asdict(event), sort_keys=True) + "\n")
