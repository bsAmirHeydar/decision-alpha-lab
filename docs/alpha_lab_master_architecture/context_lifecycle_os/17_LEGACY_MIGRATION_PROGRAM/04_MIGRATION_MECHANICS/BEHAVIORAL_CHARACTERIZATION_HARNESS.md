---
title: "Behavioral Characterization Harness"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Behavioral Characterization Harness

The harness captures legacy behavior before refactor.

## Trace fields

- stable trace ID;
- source identity and version;
- environment and compile build;
- symbol, timeframe and session;
- event time and availability time;
- bar index and closed/current-bar status;
- state before and after;
- emitted Context/Setup/Treatment event;
- reason codes;
- drawing specification;
- execution request intent without broker submission;
- error or incomplete-data result.

Golden cases cover positive, negative, no-trade, invalidation, expiry, restart, history expansion, missing bars, DST, session boundary, multi-chart, duplicate tick, symbol change and timeframe change.
