"""Minimal core module for Task3."""

from __future__ import annotations

import re

_SEPARATOR_PATTERN = re.compile(r"[\s\-]+")


def normalize_key(raw: str) -> str:
    """Normalize an arbitrary key to a stable snake_case-like identifier."""
    cleaned = raw.strip().lower()
    cleaned = _SEPARATOR_PATTERN.sub("_", cleaned)
    cleaned = cleaned.strip("_")
    if not cleaned:
        raise ValueError("key cannot be empty after normalization")
    return cleaned


def build_task_id(prefix: str, sequence: int) -> str:
    """Build a deterministic task id from a text prefix and positive sequence."""
    if sequence <= 0:
        raise ValueError("sequence must be greater than 0")
    return f"{normalize_key(prefix)}-{sequence:03d}"
