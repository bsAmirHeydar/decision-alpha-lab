# EXP0015 CME Live Provider Patch

This patch adds a CME-compatible provider layer for EXP0015.

## Implemented provider modes

```text
databento_historical
  One-shot historical download for offline research.

databento_live
  Persistent live Databento stream for licensed CME/Globex data.

databento_historical_poll
  Near-live incremental historical polling. Default cadence: 300 seconds.

yahoo_delayed
  Delayed development fallback without CME credentials.
```

## Historical polling

The historical poller is intended for closed-bar monitoring and operational simplicity. It does not request the entire history repeatedly. It reads the latest stored bar, requests a small overlapping range, merges by timestamp, and atomically rewrites the canonical DAL CSV files.

Default command:

```powershell
python .\tools\cme_bridge\dal_cme_live_prices.py databento_historical_poll `
  --interval-seconds 300 `
  --overlap-minutes 10 `
  --bootstrap-minutes 180 `
  --end-delay-seconds 90
```

See `tools/cme_bridge/README.md` for the full operational guide.
