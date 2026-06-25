# EXP0013 Astro CSV Runtime Path Fix

This patch makes the Astro CSV reader accept both common runtime layouts:

```text
<MT5 Data Folder>\MQL5\Files\astro_GMT3_M1_2026_to_now_mql.csv
```

and:

```text
<MT5 Data Folder>\MQL5\Files\astro\astro_GMT3_M1_2026_to_now_mql.csv
```

The input may be either:

```text
astro_GMT3_M1_2026_to_now_mql.csv
```

or:

```text
astro\astro_GMT3_M1_2026_to_now_mql.csv
```

The loader now tries three paths in order:

1. the exact input path
2. the root `MQL5\Files` file name
3. the canonical `MQL5\Files\astro` file name

For Strategy Tester, both tester files are declared:

```mql5
#property tester_file "astro_GMT3_M1_2026_to_now_mql.csv"
#property tester_file "astro\\astro_GMT3_M1_2026_to_now_mql.csv"
```

This means the tester can copy the CSV whether it was placed directly in `Files` or inside `Files\astro`.

If the panel still says `FILE_OPEN_FAILED`, the CSV is not in the active terminal data folder used by that MetaTrader instance, or the tester agent has not refreshed. Restart the tester or remove/re-run the test so it copies the declared tester file again.
