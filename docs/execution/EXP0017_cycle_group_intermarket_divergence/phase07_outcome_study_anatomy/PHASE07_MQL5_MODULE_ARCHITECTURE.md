# Phase 07 MQL5 Module Architecture

## Expert

`EXP0017_CG_Outcome_Study_Anatomy.mq5`

This expert is a study runner. It is not a trader.

## Modules

### `CGO_Types.mqh`

Defines outcome configuration, outcome availability states, outcome rows, and study summary structures.

### `CGO_OutcomeField.mqh`

Calculates entry price estimates, stop distance, forward-window close results, MFE, MAE, stop-hit state, and normalized daily-range metrics.

### `CGO_Ledger.mqh`

Writes the outcome CSV. It uses an in-memory duplicate guard so the same signal outcome is not written repeatedly during a single run.

### `CGO_Display.mqh`

Builds compact summary text for Experts tab or optional chart panel.

### `CGO_Engine.mqh`

Coordinates historical scan, confirmation-field reconstruction, outcome-row construction, and ledger writing.

## Dependency chain

```text
CGT Time Anatomy
  -> CGR Reference Field
    -> CGH Hunt Field
      -> CGC Confirmation Field
        -> CGO Outcome Study
```

Phase 07 must never create a separate definition of time, reference, hunt, divergence, or confirmation.
