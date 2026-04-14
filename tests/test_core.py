"""Tests for the minimal core module."""

import pytest

from src.core import build_task_id, normalize_key


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("  Hello World  ", "hello_world"),
        ("A-B-C", "a_b_c"),
        ("multi   space---value", "multi_space_value"),
    ],
)
def test_normalize_key_success(raw: str, expected: str) -> None:
    assert normalize_key(raw) == expected


@pytest.mark.parametrize("raw", ["", "   ", "---", " - - "])
def test_normalize_key_rejects_empty_result(raw: str) -> None:
    with pytest.raises(ValueError, match="cannot be empty"):
        normalize_key(raw)


def test_build_task_id_success() -> None:
    assert build_task_id("Feature Alpha", 7) == "feature_alpha-007"


@pytest.mark.parametrize("sequence", [0, -1, -10])
def test_build_task_id_rejects_non_positive_sequence(sequence: int) -> None:
    with pytest.raises(ValueError, match="greater than 0"):
        build_task_id("x", sequence)
