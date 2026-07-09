# 01 — Source Adapter Contract

The indicator must not depend on one fragile source path. Source acquisition is a strategy:

```text
GT_FETCH_LOCAL_FILE
GT_FETCH_WEBREQUEST
GT_FETCH_AUTO
```

## Local File Bridge

Default live mode. The indicator reads:

```text
MQL5/Files/GartalTerminal/ff_calendar_thisweek.xml
```

This file is written by `GartalNewsDownloaderEA.mq5`.

## Unsafe WebRequest Attempt

Kept for diagnostics only. It is explicitly disabled by default through:

```text
InpAllowIndicatorWebRequest = false
```

If enabled and the terminal blocks the call, runtime diagnostics must explain that the EA bridge is the production path.

## Cache

`InpLocalCacheFile` stores the last successfully parsed raw source.
