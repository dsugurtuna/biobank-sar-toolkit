"""SAR discovery engine — locates participant data across manifests and PLINK files.

Scans metadata CSVs, manifests, and PLINK .fam files to identify where a
given participant ID appears within a genomic data lake.
"""

from __future__ import annotations

import csv
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set


@dataclass
class DiscoveryHit:
    """A single location where a participant ID was found."""

    file_path: str
    line_number: int
    matched_text: str
    source_type: str  # "manifest", "fam", "metadata"


@dataclass
class DiscoveryResult:
    """Aggregated discovery result for a single participant."""

    participant_id: str
    hits: List[DiscoveryHit] = field(default_factory=list)

    @property
    def is_found(self) -> bool:
        return len(self.hits) > 0

    @property
    def source_types(self) -> Set[str]:
        return {h.source_type for h in self.hits}

    @property
    def file_count(self) -> int:
        return len({h.file_path for h in self.hits})


class SARDiscoveryEngine:
    """Search for participant presence across manifests and genotype files.

    Parameters
    ----------
    root_dir : str or Path
        Root directory to search.
    manifest_patterns : list of str
        Glob patterns for manifest/metadata files. Defaults to common CSV/TSV
        patterns.
    """

    DEFAULT_MANIFEST_PATTERNS = ["**/*.csv", "**/*.tsv", "**/*.txt"]
    FAM_PATTERN = "**/*.fam"

    def __init__(
        self,
        root_dir: str | Path,
        manifest_patterns: Optional[List[str]] = None,
    ) -> None:
        self.root_dir = Path(root_dir)
        self.manifest_patterns = manifest_patterns or self.DEFAULT_MANIFEST_PATTERNS

    def _search_file(
        self,
        file_path: Path,
        participant_id: str,
        source_type: str,
    ) -> List[DiscoveryHit]:
        """Search a single file for a participant ID."""
        hits: List[DiscoveryHit] = []
        try:
            with open(file_path, errors="replace") as fh:
                for line_no, line in enumerate(fh, start=1):
                    if participant_id in line:
                        hits.append(
                            DiscoveryHit(
                                file_path=str(file_path),
                                line_number=line_no,
                                matched_text=line.strip()[:200],
                                source_type=source_type,
                            )
                        )
        except (PermissionError, OSError):
            pass
        return hits

    def search(self, participant_id: str) -> DiscoveryResult:
        """Search all manifests and .fam files for a participant ID.

        Parameters
        ----------
        participant_id : str
            The identifier to search for.

        Returns
        -------
        DiscoveryResult
        """
        result = DiscoveryResult(participant_id=participant_id)

        # Search manifests
        manifest_files: Set[Path] = set()
        for pattern in self.manifest_patterns:
            manifest_files.update(self.root_dir.glob(pattern))

        for mf in sorted(manifest_files):
            result.hits.extend(
                self._search_file(mf, participant_id, "manifest")
            )

        # Search .fam files
        for fam in sorted(self.root_dir.glob(self.FAM_PATTERN)):
            result.hits.extend(
                self._search_file(fam, participant_id, "fam")
            )

        return result

    def search_batch(self, participant_ids: List[str]) -> List[DiscoveryResult]:
        """Search for multiple participants."""
        return [self.search(pid) for pid in participant_ids]
