"""Evidence map loading and validation."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from rag_eval_gov.config.schemas import EvidenceMapRecord


def load_evidence_map(path: Path) -> list[EvidenceMapRecord]:
    records = pd.read_csv(path).fillna("").to_dict(orient="records")
    return [EvidenceMapRecord.model_validate(record) for record in records]
