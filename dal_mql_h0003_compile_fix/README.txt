DAL MQL H0003 compile fix

This is an MQL-side emergency patch for the compile error:

wrong parameters count, 3 passed, but 4 requires
DAL_M0003Reports.mqh line 233 / 488
DAL_M0001RandomFractionK(const int,const int,const int,const int)

What it does:
- Finds DAL_M0003Reports.mqh under your MQL project.
- Finds old 3-argument calls to DAL_M0001RandomFractionK(...).
- Converts them to 4-argument calls by adding a deterministic salt.
- Creates .bak_YYYYMMDD_HHMMSS backups before editing.
- Deletes the patch folder after applying unless -NoCleanup is passed.

Run from the folder where decision-alpha-lab exists:

Expand-Archive .\dal_mql_h0003_compile_fix.zip -DestinationPath .
powershell -ExecutionPolicy Bypass -File .\dal_mql_h0003_compile_fix\apply_patch.ps1 .\decision-alpha-lab

If your MQL files are directly in the current folder, run:

powershell -ExecutionPolicy Bypass -File .\dal_mql_h0003_compile_fix\apply_patch.ps1 .
