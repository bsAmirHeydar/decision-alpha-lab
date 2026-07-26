---
title: "Test Pyramid, Fixtures, and Acceptance Evidence"
tags: [exp0019, faerie-protocol, implementation-program, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
implementation_program: FP-IMP-001
program_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# Test Pyramid, Fixtures, and Acceptance Evidence

## Test pyramid

### Contract tests

- enum closure;
- ID canonicalization;
- configuration hash partitioning;
- reason-code registry;
- relation registry;
- state-transition legality.

### Module self-tests

- DST/session/week boundaries;
- M1 synchronization and gaps;
- window aggregation;
- reference creation and protected consumption;
- first-sweep classification;
- same-minute dual touch;
- strict same-session confirmation;
- WW neutralization and newest-active selection;
- signal dedup and restart.

### Integration replay

Golden M1 fixtures must cover:

- AL/AN/LN bullish and bearish;
- NA/NL/NN across normal weekdays, weekends, missing calendar days, and rollover;
- WW bullish/bearish, second-symbol neutralization, overlapping WW histories;
- no-active-WW behavior;
- WW-aligned and opposed downstream signals;
- pair-global earliest-Hunt arbitration;
- suppressed signals that remain visible.

### Indicator tests

- expected object inventory from a golden ledger;
- no object collisions across two chart instances;
- clean mode vs audit mode projection;
- timeframe change without detection drift;
- responsive label lanes;
- historical alert suppression;
- panel filter actions do not mutate ledger;
- restart reproduces identical semantic IDs and visual inventory.

### Performance tests

- long-history backfill;
- incremental versus full replay parity;
- steady-state timer latency;
- object update rate and redraw count;
- memory/object-count ceilings;
- multi-chart and multi-instance operation.

### Execution tests

After indicator release:

- quota reservation races;
- SELL spread snapshot and risk parity;
- broker rejection/partial fill/pending/cancel/reconnect;
- paper/live ledger reconciliation.

## Required evidence per accepted phase

- MetaEditor compile logs;
- Strategy Tester journal excerpt;
- golden event hashes;
- object inventory or screenshot only as supplemental evidence;
- performance metrics;
- file index/hashes;
- exact commit and rollback instruction.
