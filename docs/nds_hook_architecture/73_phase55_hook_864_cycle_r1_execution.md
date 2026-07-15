---
title: Phase 55 — NDS Hook 86.4 Cycle R1 Execution
status: implemented_opt_in
version: 1.0.0
updated: 2026-07-15
---
# Phase 55 — NDS Hook 86.4 Cycle R1 Execution

## Architectural decision

Phase 55 adds a profile adapter, not a structure detector:

```text
existing Hook Phase02 sequence
→ existing family validity
→ canonical cycle closure and confirmed Terminal
→ canonical x_count = 3 or 4
→ untouched crown-to-origin 86.4 level
→ existing Hook trade execution stack
```

## Single-source guarantees

- Node counting remains owned by Hook Phase02.
- Cycle closure remains owned by `FP_HookP02SequenceCycleClosed`.
- Crown, Origin, Terminal, Death, family, and validity remain sequence fields.
- The new module owns only profile validation and Entry projection.
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
