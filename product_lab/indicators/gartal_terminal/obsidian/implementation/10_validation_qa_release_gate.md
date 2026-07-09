---
type: implementation-phase
phase: 10
product: gartal terminal
status: planned
language: en
---

# Phase 10 — Validation, QA & Release Gate

## Objective

Create the release gate that decides whether `gartal terminal` is safe enough for beta users and later for paid customers.

## QA Categories

| Category | Purpose |
|---|---|
| Compile QA | no MQL5 errors/warnings caused by product modules |
| Source QA | fetch, parse, cache, and failure handling |
| Time QA | broker GMT correctness and date rollover |
| UI QA | dashboard readability, object cleanup, layout stability |
| Timeline QA | correct event placement and label collision handling |
| Alert QA | stage timing, dedupe, channels, user toggles |
| Performance QA | object count, redraw frequency, CPU impact |
| Packaging QA | release output, docs, license status |

## Test Matrix

| Test | Expected Result |
|---|---|
| Sample mode on empty chart | dashboard and sample events render |
| WebRequest blocked | clear dashboard warning appears |
| Cache available, source down | cached data appears with age warning |
| Manual GMT +03:00 | event lines shift to broker time correctly |
| Auto GMT enabled | diagnostic offset appears |
| EURUSD chart | EUR + USD auto-filter works |
| XAUUSD chart | USD macro events show by default |
| High-impact only | low/medium/holiday rows hidden |
| Multiple same-time events | labels stack or compress cleanly |
| Alert 15m before | fires once only |
| Timeframe change | old objects are cleaned and redrawn |
| Indicator removal | all `GT_` objects are deleted |

## Beta Release Gate

The product can move to beta only if:

- [ ] compile passes
- [ ] sample mode is stable
- [ ] dashboard filters work from UI
- [ ] timeline renders future events
- [ ] alert dedupe works
- [ ] cache/failure diagnostics work
- [ ] broker GMT manual override works
- [ ] release package is clean
- [ ] customer quick-start exists

## Commercial Release Gate

The product can move to paid release only if:

- [ ] live source adapter is stable across multiple news days
- [ ] parser fixtures cover multiple calendar payload shapes
- [ ] customer WebRequest setup is documented
- [ ] license state is implemented or intentionally deferred
- [ ] no known crash path remains
- [ ] support FAQ covers common failures
- [ ] versioned release artifact is reproducible

## QA Logging

Create a QA note per build:

```text
qa/YYYY-MM-DD_gartal_terminal_v0.2.0_beta_check.md
```

Each QA note should include:

- build version
- terminal build
- broker/server
- symbol
- timeframe
- source mode
- broker GMT mode
- visible event count
- observed failures
- screenshots
- release decision

## Next

- [[11_next_build_sprints|Phase 11 — Next Build Sprints]]
