"""Tests for sar_toolkit.reporter."""

from pathlib import Path

import pytest

from sar_toolkit.discovery import DiscoveryResult, DiscoveryHit
from sar_toolkit.reporter import SARReporter, SARCase


@pytest.fixture()
def sample_cases() -> list:
    found = DiscoveryResult(
        participant_id="P12345",
        hits=[
            DiscoveryHit(
                file_path="/data/manifest.csv",
                line_number=10,
                matched_text="P12345,active",
                source_type="manifest",
            )
        ],
    )
    not_found = DiscoveryResult(participant_id="P99999")
    return [
        SARCase(
            request_id="SAR-001",
            participant_id="P12345",
            request_date="2025-01-15",
            discovery=found,
        ),
        SARCase(
            request_id="SAR-002",
            participant_id="P99999",
            request_date="2025-01-16",
            discovery=not_found,
        ),
    ]


class TestSARReporter:
    def test_discovery_report(self, tmp_path: Path, sample_cases: list) -> None:
        reporter = SARReporter(tmp_path / "reports")
        path = reporter.generate_discovery_report(sample_cases)
        assert path.exists()
        content = path.read_text()
        assert "SAR-001" in content
        assert "Yes" in content
        assert "No" in content

    def test_summary_report(self, tmp_path: Path, sample_cases: list) -> None:
        reporter = SARReporter(tmp_path / "reports")
        path = reporter.generate_summary(sample_cases)
        assert path.exists()
        text = path.read_text()
        assert "Participants with data:    1" in text
        assert "Participants without data: 1" in text
        assert "[FOUND]" in text
        assert "[NOT FOUND]" in text
