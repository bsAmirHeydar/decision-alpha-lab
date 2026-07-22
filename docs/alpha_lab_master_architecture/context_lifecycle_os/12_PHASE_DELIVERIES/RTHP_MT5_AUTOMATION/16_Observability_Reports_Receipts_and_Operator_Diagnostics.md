---
title: RTHP MT5 Automation — Observability, Reports, Receipts, and Operator Diagnostics
status: roadmap-approved-for-implementation
version: 1.0.0
updated: 2026-07-22
tags: [rthp, observability, reports, diagnostics]
---

# Observability, Reports, Receipts, and Operator Diagnostics

## Required reports

- terminal discovery report;
- terminal health report;
- symbol-resolution report;
- symbol metadata snapshots;
- history acquisition receipt ledger;
- per-symbol coverage report;
- common-range report;
- M1 quality report;
- cross-symbol alignment report;
- source-binding manifest;
- RTHP materialization report;
- train preflight report;
- run completion report;
- immutable hash ledger.

## Operator summary

The final console output should state:

```text
Terminal: resolved / blocked
Symbols: resolved / ambiguous
M1 source: pass / pass-with-declared-gaps / blocked
Common history: start → end
RTHP occurrences: count
Mature labels: count
Batch: frozen / blocked
Train: completed / blocked
Run verification: pass / fail
```

## Diagnostics

Errors must include:

- stable reason code;
- affected stage;
- affected symbol/time range;
- terminal error code when available;
- retryability classification;
- operator remediation;
- evidence path.

Raw secrets or account credentials must never appear.
