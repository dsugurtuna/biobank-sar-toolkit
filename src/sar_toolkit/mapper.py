"""ID mapping module — translates between identifier systems.

Handles mapping between external IDs, internal pack IDs, national IDs, and
clinical aliases used in biobank datasets.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class IDMapping:
    """A single mapping between two identifier spaces."""

    source_id: str
    target_id: str
    id_type: str  # "external", "pack", "national", "clinical"


@dataclass
class MappingReport:
    """Summary of an ID mapping operation."""

    total_input: int = 0
    matched: int = 0
    unmatched: int = 0
    mappings: List[IDMapping] = field(default_factory=list)

    @property
    def match_rate(self) -> float:
        if self.total_input == 0:
            return 0.0
        return self.matched / self.total_input


class IDMapper:
    """Map between biobank identifier systems.

    Loads alias files and phenotype metadata to build bidirectional mappings,
    then translates participant IDs between systems.

    Parameters
    ----------
    alias_csv : str or Path, optional
        Path to an alias CSV mapping external to internal IDs.
    phenotype_csv : str or Path, optional
        Path to a phenotype CSV containing clinical metadata and IDs.
    """

    def __init__(
        self,
        alias_csv: Optional[str | Path] = None,
        phenotype_csv: Optional[str | Path] = None,
    ) -> None:
        self._ext_to_int: Dict[str, str] = {}
        self._int_to_ext: Dict[str, str] = {}
        self._phenotype_data: Dict[str, Dict[str, str]] = {}

        if alias_csv:
            self.load_aliases(alias_csv)
        if phenotype_csv:
            self.load_phenotypes(phenotype_csv)

    def load_aliases(
        self,
        csv_path: str | Path,
        external_col: str = "external_id",
        internal_col: str = "internal_id",
    ) -> int:
        """Load alias mappings from a CSV file.

        Returns the number of mappings loaded.
        """
        count = 0
        with open(csv_path, newline="") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                ext = row.get(external_col, "").strip()
                internal = row.get(internal_col, "").strip()
                if ext and internal:
                    self._ext_to_int[ext] = internal
                    self._int_to_ext[internal] = ext
                    count += 1
        return count

    def load_phenotypes(
        self,
        csv_path: str | Path,
        id_col: str = "participant_id",
    ) -> int:
        """Load phenotype data from CSV. Returns the number of records loaded."""
        count = 0
        with open(csv_path, newline="") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                pid = row.get(id_col, "").strip()
                if pid:
                    self._phenotype_data[pid] = dict(row)
                    count += 1
        return count

    def to_internal(self, external_id: str) -> Optional[str]:
        """Map an external ID to an internal ID."""
        return self._ext_to_int.get(external_id)

    def to_external(self, internal_id: str) -> Optional[str]:
        """Map an internal ID to an external ID."""
        return self._int_to_ext.get(internal_id)

    def get_phenotype(self, participant_id: str) -> Optional[Dict[str, str]]:
        """Retrieve phenotype data for a participant."""
        return self._phenotype_data.get(participant_id)

    def map_ids(
        self,
        ids: List[str],
        direction: str = "to_internal",
    ) -> MappingReport:
        """Map a batch of IDs and return a report.

        Parameters
        ----------
        ids : list of str
            IDs to translate.
        direction : str
            Either ``"to_internal"`` or ``"to_external"``.
        """
        report = MappingReport(total_input=len(ids))
        lookup = self._ext_to_int if direction == "to_internal" else self._int_to_ext
        id_type = "internal" if direction == "to_internal" else "external"

        for source_id in ids:
            target = lookup.get(source_id)
            if target:
                report.matched += 1
                report.mappings.append(
                    IDMapping(source_id=source_id, target_id=target, id_type=id_type)
                )
            else:
                report.unmatched += 1

        return report
