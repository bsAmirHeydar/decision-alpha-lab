# EXP0013 Astro CSV Runtime Diagnostic Guide

This guide explains how the runtime diagnostic separates file-path errors from CSV-content and timestamp-alignment errors.

## Runtime Root

MQL5 does not read files from the repository root.

When an input says:

```text
InpAstroCsvFile = astro\astro_GMT3_M1_2026_to_now_mql.csv
```

MQL resolves it as:

```text
<MetaTrader Data Folder>\MQL5\Files\astro\astro_GMT3_M1_2026_to_now_mql.csv
```

Use MetaTrader:

```text
File -> Open Data Folder
```

Then put the CSV under:

```text
MQL5\Files\astro\
```

The `.xlsx` workbook is human-review only. The runtime reader consumes the `.csv` mirror.

## Diagnostic Stages

### FILE_OPEN_FAILED

Meaning:

```text
Problem is FILE ADDRESS / runtime file access.
```

The EA could not open the file at the resolved runtime path.

Fix:

```text
1. Put the CSV under <MT5 Data Folder>\MQL5\Files\astro\
2. Use only the relative input path: astro\file.csv
3. Do not use lab\... or mql5\Files\... as input
4. Do not use .xlsx as the input file
```

### EMPTY_FILE / HEADER_READ_FAILED

Meaning:

```text
The path is probably correct, but the file is empty or unreadable as text.
```

Fix: regenerate the CSV and copy it again to the MT5 Data Folder.

### BAD_HEADER

Meaning:

```text
File opened, but it is not the expected astro CSV schema.
```

Required columns:

```text
broker_time
utc_time
feature_key
```

This often happens when the input points to the `.xlsx` file or to a wrong CSV.

### NO_VALID_ROWS

Meaning:

```text
The header exists, but no rows could be parsed into valid candle astro rows.
```

Check:

```text
- date format
- delimiter
- empty feature_key
- broker_time / utc_time columns
```

### LOAD_OK but ROW NOT FOUND

Meaning:

```text
The CSV path is correct and the CSV is readable.
The problem is timestamp lookup.
```

The diagnostic panel will show:

```text
requested broker time
requested utc by input offset
csv broker range
csv utc range
nearest before/equal row
nearest after/equal row
exact mode
```

If requested time is outside CSV range, regenerate CSV for the tester/live date range.

If requested time is inside range but exact match fails, check:

```text
- timeframe
- broker GMT offset
- seconds alignment
- whether tester candle open time equals CSV broker_time exactly
```

For visual debugging only, set:

```text
InpRequireExactBarTime = false
```

For final research, restore exact matching after fixing time alignment.
