# Biobank SAR Toolkit 🧬

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Bash](https://img.shields.io/badge/Language-Bash-blue.svg)](https://www.gnu.org/software/bash/)
[![Bioinformatics](https://img.shields.io/badge/Domain-Bioinformatics-green.svg)]()

**Professional Subject Access Request (SAR) Automation for Biobanks & Research Cohorts.**

The **Biobank SAR Toolkit** is a suite of open-source shell scripts designed to streamline the data discovery and reporting process for Subject Access Requests (SAR) under GDPR and other data protection regulations. 

Tailored for high-performance computing (HPC) environments, it automates the tedious task of locating participant data across complex directory structures, metadata manifests, and genotype datasets (PLINK).

---

## 🚀 Key Features

*   **🔍 Deep Discovery**: Recursively searches metadata CSVs, sample manifests, and PLINK `.fam` headers to locate every trace of a participant.
*   **🔗 Intelligent Mapping**: Automatically resolves internal IDs to external aliases, kit IDs, and secondary identifiers.
*   **🛡️ Privacy-First**: Generates sanitized, audit-ready reports suitable for compliance documentation.
*   **⚡ HPC Ready**: Lightweight Bash scripts optimized for Linux/Unix environments common in bioinformatics.

## 📂 Toolkit Contents

| Script | Function |
| :--- | :--- |
| `sar_discovery.sh` | **The Search Engine.** Scans file systems and manifests to find where a participant's data lives. |
| `sar_mapping.sh` | **The Reporter.** Extracts and standardizes ID mappings into a clean, readable summary. |

## 🛠️ Installation & Usage

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_ORG/biobank-sar-toolkit.git
cd biobank-sar-toolkit
chmod +x *.sh
```

### 2. Configure Your Environment
These scripts are **templates**. You must adapt them to your specific directory structure.

*   **Edit `sar_discovery.sh`**: Set `BASE_DATA_DIR` to your storage root. Update `METADATA_LOCATIONS` to point to your manifest folders.
*   **Edit `sar_mapping.sh`**: Set paths to your master alias and phenotype files.

### 3. Run a Search
```bash
# Search for a participant
./sar_discovery.sh
```

### 4. Generate a Report
```bash
# Create a summary of ID mappings
./sar_mapping.sh
```

## 🤝 Contributing
Contributions are welcome! Whether it's adding support for VCF files, improving regex matching, or documentation fixes. See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📄 License
This project is licensed under the [MIT License](LICENSE) - see the file for details.

---
*Developed for the bioinformatics community to ensure efficient, compliant, and transparent data management.*
