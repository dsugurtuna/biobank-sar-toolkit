# Subject Access Request (SAR) Helper Scripts

This repository contains shell scripts designed to assist Data Managers and Bioinformaticians in handling Subject Access Requests (SAR) within a research or biobank environment. 

These scripts automate the process of locating participant data across complex directory structures, metadata manifests, and genotype file headers (PLINK `.fam` files).

## Scripts Overview

### 1. `locate_participant_data.sh`
**Purpose:** Discovery.  
This script searches for specific Participant IDs (or their aliases) across a defined set of metadata directories and genotype datasets.

**Features:**
- **Multi-ID Search:** Searches for multiple IDs (e.g., internal ID, external ID, legacy ID) simultaneously.
- **Tiered Search:** 
    1. First checks metadata/manifest CSVs for quick hits.
    2. If no match is found, performs a deep search within PLINK `.fam` files in specified genotype directories.
- **Path Awareness:** Checks if directories exist before searching to avoid errors.

### 2. `generate_id_summary.sh`
**Purpose:** Reporting & Mapping.  
Once a participant is identified, this script extracts and standardizes their ID mappings from various source manifests (e.g., Alias logs, Phenotype dumps).

**Features:**
- **ID Standardization:** Renames internal column values (e.g., "Pack ID" -> "GFX_ID") for cleaner reporting.
- **Data Extraction:** Uses `awk` to parse CSVs and extract specific linked IDs (like Kit IDs or Secondary IDs).
- **Formatted Output:** Generates a tab-separated summary file suitable for review.

## Usage

### Prerequisites
- Bash shell (Linux/macOS)
- Standard Unix tools: `grep`, `awk`, `find`, `sort`, `xargs`

### Configuration
**These scripts are templates.** You **must** edit the configuration sections at the top of each script to match your environment.

1. **Open `locate_participant_data.sh`**:
   - Update `BASE_DATA_DIR` to point to your main data storage.
   - Update `METADATA_LOCATIONS` and `GENO_DIRS` arrays to match your folder structure.
   - Set the `ID1_PRIMARY`, `ID1_ALIAS`, etc., variables to the IDs you are searching for.

2. **Open `generate_id_summary.sh`**:
   - Update `ALIAS_FILE` and `PHENO_FILE` paths.
   - Adjust the `awk` column indices (`$1`, `$2`, etc.) to match your CSV schema.

### Running the Scripts

```bash
# Make scripts executable
chmod +x locate_participant_data.sh generate_id_summary.sh

# Run the discovery script
./locate_participant_data.sh

# Run the summary generation script
./generate_id_summary.sh
```

## Disclaimer
These scripts are provided as educational examples and templates. They were originally developed for use in a specific high-performance computing (HPC) environment and have been anonymized for public sharing. Ensure you validate the logic against your own data governance policies before use.
