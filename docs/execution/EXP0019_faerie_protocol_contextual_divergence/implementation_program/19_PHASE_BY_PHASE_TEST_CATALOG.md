---
title: "Phase-by-Phase Test Catalog"
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
# Phase-by-Phase Test Catalog

## Minimum test groups

| Phase | Mandatory tests |
|---|---|
| I00 | source hash, manifest closure, clean baseline |
| I01 | old-context regression, adapter version mismatch, no duplicate core |
| I02 | enum closure, canonical IDs, semantic/projection hash split |
| I03 | DST transitions, session boundaries, NY week boundaries |
| I04 | two-symbol alignment, gap/late history, cursor/revision |
| I05 | A/L/N/W aggregation, calendar-day gaps, reference lifecycle |
| I06 | six relations both directions, same-M1 dual touch, dedup |
| I07 | strict same-session close, host TF resolution, invalidation |
| I08 | WW both directions, neutralization, overlap/newest-active |
| I09 | ledger chain, first-signal arbitration, restart/checkpoint |
| I10 | indicator lifecycle, input validation, instance isolation, no trade imports |
| I11 | visual inventory, immutable confirmed drawing, dirty update |
| I12 | filters, panel, alerts, historical alert suppression, export |
| I13 | full/incremental parity, restart, timeframe invariance, performance |
| I14 | Indicator/EA differential event hashes |
| I15 | quota races, spread/risk geometry, paper reconciliation |
| I16 | authorization, broker outcomes, kill switch, micro-live rollback |

## Fixture naming

```text
FP_<PHASE>_<FEATURE>_<CASE>_<VERSION>
```

Examples:

- `FP_I03_DST_SPRING_FORWARD_V1`
- `FP_I06_AL_BULLISH_SINGLE_HUNT_V1`
- `FP_I07_CONFIRM_CLOSE_AFTER_SESSION_REJECT_V1`
- `FP_I08_WW_SECOND_SYMBOL_NEUTRALIZE_V1`
- `FP_I13_MULTI_INSTANCE_OBJECT_ISOLATION_V1`

## Golden fixture immutability

Golden outputs are regenerated only after a reviewed semantic change, version increment, and documented migration. A test failure is not fixed by blindly accepting new golden files.
