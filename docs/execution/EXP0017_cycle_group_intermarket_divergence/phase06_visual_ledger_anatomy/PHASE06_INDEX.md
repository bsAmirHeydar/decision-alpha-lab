# EXP0017 Phase 06 — Visual Language & Signal Audit Ledger

Phase 06 turns the closed-candle final states from Phase 05 into two audit outputs:

1. **Visual language on the chart**: lines, confirmation markers, reference-cycle anchors, and labels.
2. **Raw signal audit ledger**: a CSV record of confirmed tradeable states and invalidated double-hunt states.

Phase 06 is still not a trading phase. It does not place orders, size risk, set targets, close positions, classify performance, or rank cycle groups.

## Phase 06 purpose

The strategy now has enough anatomy to explain what it sees. Phase 06 makes that seeing auditable.

The robot should not merely print that a signal exists. It should draw why the state exists and persist the state so later phases can study outcomes without losing the original event.

## Added implementation

- `EXP0017_CG_Visual_Ledger_Anatomy.mq5`
- `CGV_Types.mqh`
- `CGV_Drawing.mqh`
- `CGV_Ledger.mqh`
- `CGV_Display.mqh`
- `CGV_Engine.mqh`

## Phase boundary

Phase 06 consumes confirmed/invalidation states from Phase 05. It does not redefine them.

A Phase 06 ledger row is not a trade result. It is only an event record.
