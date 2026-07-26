# Pure Astro Entry Excel Report

Builds a fast batch Excel report from an astro feature CSV without running MT5 ticks.

Output workbook sheets:

- `RunSummary`: run metadata and counts
- `EntryWindows`: one row per complete `enter_long` / `enter_short` window
- `EntryBars`: every bar belonging to those full entry windows
- `ExitEvents`: first exit warning and resolved paper-exit event per entry window

Default output location for the PowerShell helper:

`%APPDATA%\MetaQuotes\Terminal\Common\Files\astro\reports\nas100_pure_entry_windows.xlsx`

Quick command from the project root:

```powershell
$COMMON = "$env:APPDATA\MetaQuotes\Terminal\Common\Files"
python .\tools\astro_validation\astro_pure_entry_excel.py `
  --csv "$COMMON\astro_nas100_mql.csv" `
  --out-xlsx "$COMMON\astro\reports\nas100_pure_entry_windows.xlsx" `
  --family PURE `
  --also-csv
```

Or use the helper:

```powershell
.\tools\astro_validation\build_pure_entry_excel_common.ps1 `
  -CsvName "astro_nas100_mql.csv" `
  -OutName "nas100_pure_entry_windows.xlsx" `
  -Family PURE `
  -AlsoCsv `
  -OpenAfter
```
