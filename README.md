# Biobank SAR Toolkit

[![CI](https://github.com/dsugurtuna/biobank-sar-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/dsugurtuna/biobank-sar-toolkit/actions)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Portfolio](https://img.shields.io/badge/Status-Portfolio_Project-purple.svg)]()

Automated Subject Access Request (SAR) processing for genomic biobanks — participant discovery, ID mapping, and compliance reporting.

> **Portfolio disclaimer:** This repository contains sanitised, generalised versions of tooling developed at NIHR BioResource. No real participant data or internal paths are included.

---

## Overview

Under GDPR and data-protection regulations, biobanks must locate and report every trace of a participant's data when a Subject Access Request is received. This toolkit automates that process:

- **Discovery engine** — recursively searches metadata CSVs, manifests, and PLINK `.fam` files to locate participant data.
- **ID mapper** — translates between external IDs, internal pack IDs, national IDs, and clinical aliases.
- **Compliance reporter** — generates standardised CSV and summary reports ready for audit.

## Repository Structure

```text
.
├── src/sar_toolkit/              Python package
│   ├── __init__.py
│   ├── discovery.py              Participant data discovery engine
│   ├── mapper.py                 Multi-system ID mapper
│   └── reporter.py               SAR compliance report generator
├── tests/
│   ├── test_discovery.py
│   ├── test_mapper.py
│   └── test_reporter.py
├── legacy/                       Original shell scripts
│   ├── sar_discovery.sh
│   └── sar_mapping.sh
├── .github/workflows/ci.yml
├── pyproject.toml
├── Dockerfile
└── Makefile
```

## Quick Start

```bash
pip install -e ".[dev]"
```

### Python API

```python
from sar_toolkit import SARDiscoveryEngine, IDMapper, SARReporter
from sar_toolkit.reporter import SARCase

# Discover participant data
engine = SARDiscoveryEngine("/data/biobank")
result = engine.search("P12345")
print(result.is_found, result.file_count)

# Map IDs between systems
mapper = IDMapper(alias_csv="aliases.csv", phenotype_csv="phenotypes.csv")
internal = mapper.to_internal("EXT001")  # -> "INT001"
report = mapper.map_ids(["EXT001", "EXT002"], direction="to_internal")

# Generate compliance report
reporter = SARReporter("output/")
cases = [SARCase("SAR-001", "P12345", "2025-01-15", discovery=result)]
reporter.generate_discovery_report(cases)
reporter.generate_summary(cases)
```

## Testing

```bash
make test   # or: pytest tests/ -v
```

## Jira Provenance

- **45 SAR tickets processed** — automated participant discovery and ID mapping across biobank data holdings.
- **Multi-system ID resolution** — externalID/packID/nationalID/clinicalID translation.
- **GDPR compliance** — standardised reporting for audit and regulatory review.

## Licence

MIT
