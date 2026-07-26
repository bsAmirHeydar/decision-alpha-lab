# EXP0013 Astro Time Contract and Panel Fix

## Core rule

When the Python builder is run with:

```powershell
--broker-gmt-offset-hours 3
```

the CSV contains two different time columns:

```text
broker_time = candle time in broker timezone, here GMT+3
utc_time    = broker_time - 3 hours
```

MQL5 lookup must match the chart candle open time directly to `broker_time`.

That means the GMT offset is **not applied to the lookup key**.

The offset input is only used to validate and display the UTC contract:

```text
utc_time = broker_time - InpBrokerGmtOffsetHours
```

So if the CSV was generated with GMT+3, keep:

```text
InpBrokerGmtOffsetHours = 3
```

Do **not** set it to zero. Setting it to zero would make the UTC validation wrong.

## Runtime path rule

MQL5 reads CSV files from the MT5 runtime file roots, not from the Git project root.

The loader now tries both normal and common file roots:

```text
<Terminal Data Folder>\MQL5\Files\...
<MetaQuotes Common Data Folder>\Files\...
```

It also tries these filename layouts:

```text
astro_GMT3_M1_2026_to_now_mql.csv
astro\astro_GMT3_M1_2026_to_now_mql.csv
```

## Panel fix

Blank separator lines are no longer drawn as default `Label` objects. The panel skips empty lines and draws only meaningful lines, so the chart should not show stray `Label` text anymore.

## Meaning of the displayed times

If the panel says:

```text
Broker: 2026.01.02 10:50
UTC:    2026.01.02 07:50
```

and `InpBrokerGmtOffsetHours = 3`, then the contract is correct:

```text
10:50 - 3 hours = 07:50 UTC
```

The market candle is matched by `Broker`, not by `UTC`.
