# EXP0013 Astro CSV Runtime Path and Panel Diagnostics

This note explains the two separate failure classes used by the EXP0013 visual tester demos.

## 1. File path / runtime access failure

If the panel shows:

```text
stage: FILE_OPEN_FAILED
loaded: false
DIAGNOSIS: Problem is FILE ADDRESS / runtime file access.
```

then the Expert Advisor did not even open the CSV. The problem is not astrology parsing and not timestamp alignment.

The input:

```text
astro\astro_GMT3_M1_2026_to_now_mql.csv
```

is resolved from the MetaTrader runtime Files root:

```text
<Terminal Data Folder>\MQL5\Files\astro\astro_GMT3_M1_2026_to_now_mql.csv
```

In Strategy Tester, the diagnostic may show an Agent path such as:

```text
...\Tester\<hash>\Agent-127.0.0.1-3000\MQL5\Files\astro\...
```

That means the tester agent did not receive the file. Put the CSV in the terminal data folder under `MQL5\Files\astro` before running the tester. The `#property tester_file` line can only package the file if it exists in the terminal `MQL5\Files` tree at test launch time.

## 2. CSV content failure

If the panel shows:

```text
stage: BAD_HEADER
stage: NO_VALID_ROWS
```

then the file was opened, but its contents are not in the expected runtime CSV format. MQL5 reads `.csv`, not `.xlsx`. Required columns are:

```text
broker_time, utc_time, feature_key
```

## 3. Timestamp lookup failure

If the panel shows:

```text
loaded: true rows=...
ROW NOT FOUND
```

then the CSV was loaded correctly, but the current candle open time was not found in the CSV rows. Check:

- tester date is inside CSV date range
- `InpBrokerGmtOffsetHours` matches the generated file
- timeframe matches the generated interval
- `InpRequireExactBarTime` can be set to false for visual debugging

## Panel layout fix

The demos default to object-label panels and clear the terminal `Comment()` output. This prevents chart OHLC text, Comment text, and object labels from being drawn on top of each other.
