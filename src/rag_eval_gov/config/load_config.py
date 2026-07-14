"""Load YAML configuration files."""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel


def load_yaml(path: Path) -> dict:
    """Load a YAML file as a dictionary."""

    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected a mapping in {path}")
    return data


def load_config[T: BaseModel](path: Path, schema: type[T]) -> T:
    """Load and validate a YAML configuration file."""

    return schema.model_validate(load_yaml(path))
