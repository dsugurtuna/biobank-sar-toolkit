#!/bin/bash

# ==============================================================================
# Script Name: generate_id_summary.sh
# Description: Retrieves and standardizes participant ID mappings from alias 
#              and phenotype manifests. Useful for Subject Access Requests (SAR).
# Usage:       ./generate_id_summary.sh
# ==============================================================================

# --- Configuration: Define Files and IDs ---
# Update these paths to point to your actual data manifests
ALIAS_FILE="/path/to/your/data/manifest/id_maps/aliases_dump.csv"
PHENO_FILE="/path/to/your/data/sampleid/phenotype_dump.csv"
OUT_FILE="./id_summary.txt"

# IDs to search for (Example placeholders)
ID1="PARTICIPANT_ID_1"
ID2="PARTICIPANT_ID_2"

echo "Starting ID summary generation for: $ID1, $ID2"

# --- Process Alias File ---
# Description: Extracts relevant lines, parses quoted CSV fields, removes quotes, 
# and standardizes ID types (e.g., renaming specific internal ID headers).
#
# AWK Logic:
# -F'","' : Sets delimiter to "," to handle quoted CSVs.
# $1, $2, $3 : Refers to columns in the CSV. Adjust indices based on your file structure.
# gsub    : Removes remaining quotes.

echo "Processing Alias File..."
grep -E "$ID1|$ID2" "$ALIAS_FILE" | awk -F'","' '
BEGIN { OFS="\t"; print "Source\tParticipantID\tID_Type\tLinked_ID" }
{
    gsub(/"/, "", $1); 
    gsub(/"/, "", $3); 
    
    # Standardize ID Names (Customize these rules for your dataset)
    if ($2 ~ /Pack ID - TYPE_A/) { $2 = "GFX_ID (Pack)" } 
    else if ($2 ~ /External ID/) { $2 = "External_ID (Alias)" } 
    else if ($2 ~ /National ID/) { $2 = "National_ID" } 
    
    print "AliasesDump\t" $1 "\t" $2 "\t" $3
}' > "$OUT_FILE" 

# --- Process Phenotype Dump File ---
# Description: Extracts lines anchored to the start of the line (to match primary IDs),
# and extracts specific linked IDs (e.g., secondary IDs, kit IDs).

echo "Processing Phenotype File..."
grep -E "^$ID1,|^$ID2," "$PHENO_FILE" | awk -F',' '
BEGIN { OFS="\t" }
{
    # Example extraction logic (Adjust column numbers $3, $9 etc. for your schema)
    secondary_id = $3; 
    sub(/.*:/, "", secondary_id); # Remove prefixes if present
    
    kit_id = $9;

    print "PhenoDump\t" $1 "\tKit_ID\t" kit_id
    print "PhenoDump\t" $1 "\tSecondary_ID\t" secondary_id
}' >> "$OUT_FILE" 

# --- Sort and Final Message ---
# Sort the output file for readability
sort -u "$OUT_FILE" -o "$OUT_FILE" 

echo "-------------------------------------------------------"
echo "Clean summary of ID mappings saved to: $OUT_FILE"
echo "View with: column -t -s \$'\t' $OUT_FILE | less -S"
echo "-------------------------------------------------------"
