---
title: RTHP MT5 Automation — Historical Acquisition, Paging, Coverage, and Retry
status: roadmap-approved-for-implementation
version: 1.0.0
updated: 2026-07-22
tags: [rthp, mt5, history, paging, retry]
---

# Historical Acquisition, Paging, Coverage, and Retry

## Acquisition method

Use the official MetaTrader 5 bar-history interface for `TIMEFRAME_M1` with UTC date ranges. Returned columns are normalized into the canonical M1 schema.

## History availability constraint

The terminal only returns history available to the terminal/chart environment. Therefore, a successful API call is not sufficient evidence of complete coverage.

## Deterministic paging

- Request bounded UTC chunks.
- Use small overlap windows between adjacent chunks.
- Deduplicate by `(broker_symbol, bar_open_time_utc_ms)`.
- Verify overlapping records are byte-equivalent after normalization.
- Persist a receipt for every request, response count, first time, last time, retry, and terminal error.

## Automatic common-range discovery

When the operator supplies only symbols:

1. determine the latest fully closed M1 bar available for both symbols;
2. search backward to discover the earliest reliable common history;
3. apply the default research-profile maximum lookback;
4. enforce a minimum common-history requirement;
5. freeze the resolved range in the run manifest.

## Retry policy

Retries are allowed only for classified transient terminal/history errors. Retry count, delay, and final error must be recorded. Schema errors, symbol ambiguity, history truncation, and unexplained coverage gaps are not retried indefinitely.

## Resume

Completed chunk receipts and hashes allow restart from the last verified boundary without redownloading accepted chunks.
