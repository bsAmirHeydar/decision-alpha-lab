# EXP0013 Astro CSV Runtime Path Fix

## Important distinction

MQL5 does not read the `.xlsx` workbook at runtime.

The workbook is only for human review. The Expert Advisor reads the CSV mirror.

Human review file:

```text
lab/03_experiments/EXP0013_astro_feature_store/output/gmt3_2026_to_now/astro_GMT3_M1_2026_to_now_review.xlsx
```

MQL runtime CSV source inside the repo:

```text
lab/03_experiments/EXP0013_astro_feature_store/output/gmt3_2026_to_now/astro_GMT3_M1_2026_to_now_mql.csv
```

MQL runtime CSV destination inside the actual MetaTrader data folder:

```text
<MT5 Data Folder>/MQL5/Files/astro/astro_GMT3_M1_2026_to_now_mql.csv
```

The input must be the relative path from `MQL5/Files`:

```text
astro\astro_GMT3_M1_2026_to_now_mql.csv
```

Do not use the repo path as the Expert input.

---

## Quick PowerShell check from repository root

```powershell
$Src = "lab\03_experiments\EXP0013_astro_feature_store\output\gmt3_2026_to_now\astro_GMT3_M1_2026_to_now_mql.csv"

Test-Path $Src
Get-Item $Src | Select-Object FullName, Length, LastWriteTime
Get-Content $Src -TotalCount 2
```

The first line must be a readable CSV header containing fields such as:

```text
broker_time,utc_time,unix_utc,jd_ut,...
```

If the first bytes look like `PK`, the file is an XLSX/ZIP workbook and is not the runtime CSV.

---

## Copy the runtime CSV into MetaTrader

Open MetaTrader:

```text
File > Open Data Folder
```

Copy the displayed folder path and paste it into `$Mt5DataFolder` below.

```powershell
$Src = "lab\03_experiments\EXP0013_astro_feature_store\output\gmt3_2026_to_now\astro_GMT3_M1_2026_to_now_mql.csv"
$Mt5DataFolder = "PASTE_MT5_DATA_FOLDER_HERE"
$DstDir = Join-Path $Mt5DataFolder "MQL5\Files\astro"

New-Item -ItemType Directory -Force $DstDir | Out-Null
Copy-Item -Force $Src (Join-Path $DstDir "astro_GMT3_M1_2026_to_now_mql.csv")

Get-Item (Join-Path $DstDir "astro_GMT3_M1_2026_to_now_mql.csv") | Select-Object FullName, Length, LastWriteTime
```

---

## Expert inputs

Use these inputs:

```text
InpAstroCsvFile         = astro\astro_GMT3_M1_2026_to_now_mql.csv
InpBrokerGmtOffsetHours = 3.0
InpReadTimeframe        = PERIOD_M1
InpRequireExactBarTime  = true
```

For Strategy Tester, the Expert now includes:

```mql5
#property tester_file "astro\\astro_GMT3_M1_2026_to_now_mql.csv"
```

This property is literal and compile-time. The CSV must exist under `MQL5/Files/astro/` before running the test.

---

## Date-range rule

The generated file starts at:

```text
2026-01-01 00:00:00 broker time GMT+3
```

Do not run the visual tester before this date unless you generate a wider CSV.

If the test date is outside the CSV range, the EA loads but shows:

```text
ROW NOT FOUND
```

This is a date-range or timeframe alignment issue, not an ephemeris issue.
