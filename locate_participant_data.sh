#!/bin/bash

# ==============================================================================
# Script Name: locate_participant_data.sh
# Description: Searches for participant IDs across metadata manifests and 
#              genotype file headers (.fam).
# Usage:       ./locate_participant_data.sh
# ==============================================================================

# --- Configuration ---
BASE_DATA_DIR="/path/to/your/biobank/processed_data"

# Define IDs to search for (Primary and Secondary/Alias IDs)
ID1_PRIMARY="PARTICIPANT_001"
ID1_ALIAS="ALIAS_001"
ID2_PRIMARY="PARTICIPANT_002"
ID2_ALIAS="ALIAS_002"

# Combine all IDs into a single grep pattern
SEARCH_PATTERN="$ID1_PRIMARY|$ID1_ALIAS|$ID2_PRIMARY|$ID2_ALIAS"

echo "========================================================"
echo "Subject Access Request: Data Discovery Tool"
echo "Searching for IDs: $SEARCH_PATTERN"
echo "Base Directory: $BASE_DATA_DIR"
echo "========================================================"

# --- Part 1: Search Metadata & Manifests ---
# Searches text-based logs, mapping files, and sample tables.

echo "--- Searching potential Manifest/Mapping locations ---"

# List of subdirectories or files to search within the Base Directory
# (Customize these paths based on your project structure)
METADATA_LOCATIONS=(
    "Metadata/ID_mapping/"
    "Metadata/sample_tables/"
    "Metadata/mappings/"
    "Metadata/Manifest_Legacy.csv"
)

MANIFEST_FOUND=1 # Flag: 1 = Not Found, 0 = Found

for LOC in "${METADATA_LOCATIONS[@]}"; do
    TARGET="$BASE_DATA_DIR/$LOC"
    if [ -e "$TARGET" ]; then
        echo "[Searching in $LOC]"
        # grep flags: -r (recursive), -H (print filename), -E (extended regex)
        grep -r -H -E "$SEARCH_PATTERN" "$TARGET" 2>/dev/null
        if [ $? -eq 0 ]; then
            MANIFEST_FOUND=0
        fi
    else
        echo "[Skipping - Path not found: $LOC]"
    fi
done

# Check if any manifest search found a match
if [ $MANIFEST_FOUND -eq 0 ]; then
  echo
  echo "--- Match FOUND in Manifest/Mapping files above! ---"
  echo "Review the output to see the filename and line containing the ID."
  echo "This might give you the Sample ID or Batch needed."
  exit 0 # Stop the script here if we found a manifest hit
fi

echo
echo "--- No hits in primary manifest locations. ---"
echo "--- Now searching for .fam files within Genotype directories ---"

# --- Part 2: Search Genotype Data (.fam files) ---
# PLINK .fam files contain family/sample IDs. This searches them directly.

# Define genotype directories to search within
GENO_DIRS=(
  "$BASE_DATA_DIR/Genotypes_Release_1"
  "$BASE_DATA_DIR/Genotypes_Release_2"
  "$BASE_DATA_DIR/PLINK_Data"
  "$BASE_DATA_DIR/Affymetrix_Data"
)

FOUND_IN_FAM=1 # Default to not found

for DIR in "${GENO_DIRS[@]}"; do
  if [ -d "$DIR" ]; then
    echo "[Searching .fam files in $DIR/]"
    # Use find to locate .fam files, then grep inside them
    find "$DIR" -name "*.fam" -type f -print0 2>/dev/null | \
      xargs -0 -I {} grep -H -m 1 -E "$SEARCH_PATTERN" {} 2>/dev/null
    
    # Check if grep found anything in this directory
    if [ $? -eq 0 ]; then
      FOUND_IN_FAM=0 # Mark as found
    fi
  else
    echo "[Directory not found: $DIR]"
  fi
done

echo
if [ $FOUND_IN_FAM -eq 0 ]; then
  echo "--- Match FOUND in .fam file(s) above! ---"
  echo "The output shows the .fam file(s) containing one of the IDs."
  echo "Use the path(s) listed to identify the PLINK dataset(s) needed for extraction."
else
  echo "--- No Match Found in targeted .fam file search either. ---"
  echo "Could not locate these IDs in common manifest files or genotype directories."
  echo "Recommendation: Contact the Data Management team for manual lookup."
fi
