"""Tests for sar_toolkit.discovery."""

from pathlib import Path

import pytest

from sar_toolkit.discovery import SARDiscoveryEngine


@pytest.fixture()
def data_tree(tmp_path: Path) -> Path:
    """Create a test directory with manifest and .fam files."""
    manifest = tmp_path / "manifests"
    manifest.mkdir()
    (manifest / "batch_001.csv").write_text(
        "sample_id,barcode,status\n"
        "P12345,BC001,active\n"
        "P67890,BC002,active\n"
    )
    geno = tmp_path / "genotypes" / "batch_001"
    geno.mkdir(parents=True)
    (geno / "data.fam").write_text(
        "P12345 P12345 0 0 1 -9\n"
        "P99999 P99999 0 0 2 -9\n"
    )
    return tmp_path


class TestSARDiscoveryEngine:
    def test_found_in_manifest(self, data_tree: Path) -> None:
        engine = SARDiscoveryEngine(data_tree)
        result = engine.search("P12345")
        assert result.is_found
        assert "manifest" in result.source_types

    def test_found_in_fam(self, data_tree: Path) -> None:
        engine = SARDiscoveryEngine(data_tree)
        result = engine.search("P99999")
        assert result.is_found
        assert "fam" in result.source_types

    def test_not_found(self, data_tree: Path) -> None:
        engine = SARDiscoveryEngine(data_tree)
        result = engine.search("NONEXISTENT")
        assert not result.is_found
        assert result.file_count == 0

    def test_found_in_both(self, data_tree: Path) -> None:
        engine = SARDiscoveryEngine(data_tree)
        result = engine.search("P12345")
        assert "manifest" in result.source_types
        assert "fam" in result.source_types

    def test_batch_search(self, data_tree: Path) -> None:
        engine = SARDiscoveryEngine(data_tree)
        results = engine.search_batch(["P12345", "NONEXISTENT"])
        assert results[0].is_found
        assert not results[1].is_found
