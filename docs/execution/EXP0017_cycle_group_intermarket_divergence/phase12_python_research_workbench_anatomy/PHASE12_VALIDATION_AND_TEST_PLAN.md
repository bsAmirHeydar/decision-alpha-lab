# Phase 12 Validation and Test Plan

## MQL5 bridge validation

1. Run Phase 12 bridge expert.
2. Confirm `EXP0017_Phase12_File_Inventory.csv` is created.
3. Confirm all expected input files are marked available or missing explicitly.
4. Confirm `EXP0017_Phase12_Research_Manifest.json` is created.
5. Confirm the generated Python run plan points to the Phase 12 workbench script.

## Python validation

1. Run the PowerShell script or direct Python command.
2. Confirm output directory is created.
3. Confirm data audit CSV is created.
4. Confirm OOS leaderboard CSV is created.
5. Confirm bucket stability CSV is created.
6. Confirm HTML and markdown reports are created.

## Research validation

A bucket is not considered stable only because it has positive average R. It must be checked across fold count, positive fold rate, sample count, stop rate, and drift notes.
