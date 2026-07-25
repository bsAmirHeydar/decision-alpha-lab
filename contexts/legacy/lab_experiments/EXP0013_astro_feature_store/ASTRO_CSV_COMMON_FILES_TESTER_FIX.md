# EXP0013 Astro CSV — Strategy Tester Common Files Fix

## Why the CSV can exist in `MQL5\Files` but still fail in Strategy Tester

MetaTrader has different runtime file roots:

```text
Live chart:
<Terminal Data Folder>\MQL5\Files\

Strategy Tester:
<Tester Agent Data Folder>\MQL5\Files\

Common files:
<MetaQuotes Common Data Folder>\Files\
```

If the CSV is placed under the live terminal `MQL5\Files`, the visual tester may still fail with `FILE_OPEN_FAILED` because the EA is running inside a tester agent sandbox.

This patch makes the reader try both:

```text
Normal Files root
Common Files root using FILE_COMMON
```

## Recommended stable setup

Put the CSV here:

```text
C:\Users\<USER>\AppData\Roaming\MetaQuotes\Terminal\Common\Files\astro_GMT3_M1_2026_to_now_mql.csv
```

Then set the EA input to:

```text
InpAstroCsvFile = astro_GMT3_M1_2026_to_now_mql.csv
InpBrokerGmtOffsetHours = 3
```

The reader will first try the normal runtime `Files` root and then the Common `Files` root.

## Diagnosis meanings

`FILE_OPEN_FAILED` means the file was not opened at all. This is a path/runtime sandbox issue, not a CSV parsing issue.

`BAD_HEADER` means the file was opened, but required columns such as `broker_time`, `utc_time`, or `feature_key` are missing.

`NO_VALID_ROWS` means the header was found, but rows could not be parsed.

`ROW NOT FOUND` / lookup failure means the CSV was loaded but the current candle time was not found in the loaded date range.
