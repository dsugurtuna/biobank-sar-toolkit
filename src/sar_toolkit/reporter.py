"""SAR report generator — produces standardised compliance reports."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from .discovery import DiscoveryResult
from .mapper import IDMapper, MappingReport


@dataclass
class SARCase:
    """A Subject Access Request case."""

    request_id: str
    participant_id: str
    request_date: str
    discovery: Optional[DiscoveryResult] = None
    mapping: Optional[MappingReport] = None


class SARReporter:
    """Generate standardised SAR compliance reports.

    Parameters
    ----------
    output_dir : str or Path
        Directory to write reports to.
    """

    def __init__(self, output_dir: str | Path) -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_discovery_report(
        self,
        cases: List[SARCase],
        filename: str = "sar_discovery_report.csv",
    ) -> Path:
        """Write a CSV discovery report listing all hits for each case."""
        out_path = self.output_dir / filename
        with open(out_path, "w", newline="") as fh:
            writer = csv.writer(fh)
            writer.writerow([
                "request_id",
                "participant_id",
                "request_date",
                "data_found",
                "file_count",
                "source_types",
                "hit_files",
            ])
            for case in cases:
                found = case.discovery.is_found if case.discovery else False
                file_count = case.discovery.file_count if case.discovery else 0
                sources = (
                    ", ".join(sorted(case.discovery.source_types))
                    if case.discovery
                    else ""
                )
                hit_files = (
                    "; ".join(sorted({h.file_path for h in case.discovery.hits}))
                    if case.discovery
                    else ""
                )
                writer.writerow([
                    case.request_id,
                    case.participant_id,
                    case.request_date,
                    "Yes" if found else "No",
                    file_count,
                    sources,
                    hit_files,
                ])
        return out_path

    def generate_summary(
        self,
        cases: List[SARCase],
        filename: str = "sar_summary.txt",
    ) -> Path:
        """Write a human-readable summary."""
        out_path = self.output_dir / filename
        total = len(cases)
        found = sum(
            1 for c in cases if c.discovery and c.discovery.is_found
        )
        lines = [
            "Subject Access Request — Summary Report",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "=" * 50,
            f"Total requests processed:  {total}",
            f"Participants with data:    {found}",
            f"Participants without data: {total - found}",
            "",
        ]
        for case in cases:
            status = "FOUND" if (case.discovery and case.discovery.is_found) else "NOT FOUND"
            lines.append(f"  {case.request_id}  {case.participant_id}  [{status}]")
        out_path.write_text("\n".join(lines) + "\n")
        return out_path
