---
title: Phase 55 — NDS Hook 86.4 Cycle R1 Execution
status: implemented_opt_in
version: 1.1.0
updated: 2026-07-16
---
# Phase 55 — NDS Hook 86.4 Cycle R1 Execution

## Architectural decision

Phase 55 adds a profile adapter, not a structure detector:

```text
existing Hook Phase02 sequence
→ existing family validity and confirmed Terminal
→ canonical x_count = 3 or 4
→ existing Phase03 Y-axis records
→ existing Phase04 50% X closure and origin-return death
→ closed-bar first-arrival proof at 86.4 after closure
→ existing Hook trade execution stack
```

## Single-source guarantees

- Node counting remains owned by Hook Phase02.
- Phase02 terminal availability remains owned by `FP_HookP02SequenceCycleClosed`.
- Y references remain owned by Hook Phase03.
- X closure and origin-return death remain owned by Hook Phase04.
- Crown, Origin, Terminal, family, and validity remain sequence fields.
- The new bridge owns only exact evidence binding and closed-bar first-arrival observation; it does not own structure.
- Existing risk, broker, persistence, exposure, cancellation, and audit modules remain authoritative.

## Executable behavior

For positive Hooks, submit Buy Limit at normalized 86.4 retracement. For negative Hooks, submit Sell Limit. Place Stop behind `death_boundary_price`, falling back to Origin, through existing buffer and broker-distance rules. Attach a target at one normalized risk distance. The fixed-R profile never invokes the Phase 52 F123 market-close path.

## Identity

Phase 55 uses stable sequence-level identity. The current Terminal time is excluded from its setup key, so x3→x4 cannot create a second attempt or reprice. Phase 52 retains its historical Terminal-time key.

## Safety

The exact ratio, node window, confirmed-Terminal gate, untouched-level gate, and 1R reward are locked. Central decision and send inputs remain false by default. Static implementation does not constitute MetaEditor, broker, or live release evidence.

## Detailed package

- [[../nds_entry_architecture/phase55_hook_864_cycle_r1_execution/README|Phase 55 detailed execution package]]
- [[../obsidian_hook/03_architecture/Phase 55 NDS Hook 86.4 Cycle R1 Execution|Obsidian architecture note]]


## v1.1 no-trade correction

The dedicated tester defaults to PARITY plus `InpBTTradeProfile=HOOK_864_CYCLE_R1` and emits a full Phase02→Phase04→first-arrival→execution funnel. `seq.retracement_ratio` is audit-only and no longer substitutes for actual post-closure price travel.
