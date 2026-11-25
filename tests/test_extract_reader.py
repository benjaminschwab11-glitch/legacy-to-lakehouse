"""Tests for the delimited account extract reader."""

import logging
from pathlib import Path

import pytest

from legacy_to_lakehouse.ingestion.extract_reader import count_by_tenant, iter_rows


@pytest.fixture
def sample_path() -> Path:
    return Path(__file__).parent / "fixtures" / "accounts_sample.csv"


def test_count_by_tenant(sample_path):
    # Arrange
    rows = iter_rows(sample_path)

    # Act
    counts = count_by_tenant(rows)

    # Assert
    assert counts == {"acme": 3, "globex": 2}


def test_bad_row_skipped_and_logged(sample_path, caplog):
    # Arrange
    with caplog.at_level(logging.WARNING):
        # Act
        rows = list(iter_rows(sample_path))

    # Assert
    assert len(rows) == 5
    bad_row_warnings = [
        r for r in caplog.records if "line 6" in r.getMessage() and "N/A" in r.getMessage()
    ]
    assert len(bad_row_warnings) == 1


def test_generator_single_pass(sample_path):
    # Arrange
    rows = iter_rows(sample_path)

    # Act
    first_pass = list(rows)
    second_pass = list(rows)

    # Assert
    assert len(first_pass) == 5
    assert second_pass == []
