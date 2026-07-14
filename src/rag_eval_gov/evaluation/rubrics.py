"""Rubric loading helpers."""

from __future__ import annotations

from pathlib import Path

from rag_eval_gov.config.load_config import load_config
from rag_eval_gov.config.schemas import RubricConfig


def load_rubrics(path: Path) -> RubricConfig:
    return load_config(path, RubricConfig)
