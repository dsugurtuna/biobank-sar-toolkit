"""Tests for sar_toolkit.mapper."""

from pathlib import Path

import pytest

from sar_toolkit.mapper import IDMapper, MappingReport


@pytest.fixture()
def alias_csv(tmp_path: Path) -> Path:
    p = tmp_path / "aliases.csv"
    p.write_text(
        "external_id,internal_id\n"
        "EXT001,INT001\n"
        "EXT002,INT002\n"
        "EXT003,INT003\n"
    )
    return p


@pytest.fixture()
def phenotype_csv(tmp_path: Path) -> Path:
    p = tmp_path / "phenotypes.csv"
    p.write_text(
        "participant_id,age,gender\n"
        "INT001,45,F\n"
        "INT002,52,M\n"
    )
    return p


class TestIDMapper:
    def test_load_aliases(self, alias_csv: Path) -> None:
        mapper = IDMapper(alias_csv=alias_csv)
        assert mapper.to_internal("EXT001") == "INT001"
        assert mapper.to_external("INT002") == "EXT002"

    def test_unknown_id_returns_none(self, alias_csv: Path) -> None:
        mapper = IDMapper(alias_csv=alias_csv)
        assert mapper.to_internal("UNKNOWN") is None

    def test_load_phenotypes(self, alias_csv: Path, phenotype_csv: Path) -> None:
        mapper = IDMapper(alias_csv=alias_csv, phenotype_csv=phenotype_csv)
        pheno = mapper.get_phenotype("INT001")
        assert pheno is not None
        assert pheno["age"] == "45"

    def test_map_ids_to_internal(self, alias_csv: Path) -> None:
        mapper = IDMapper(alias_csv=alias_csv)
        report = mapper.map_ids(["EXT001", "EXT002", "UNKNOWN"], direction="to_internal")
        assert report.total_input == 3
        assert report.matched == 2
        assert report.unmatched == 1
        assert report.match_rate == pytest.approx(2 / 3)

    def test_map_ids_to_external(self, alias_csv: Path) -> None:
        mapper = IDMapper(alias_csv=alias_csv)
        report = mapper.map_ids(["INT001"], direction="to_external")
        assert report.matched == 1
        assert report.mappings[0].target_id == "EXT001"
