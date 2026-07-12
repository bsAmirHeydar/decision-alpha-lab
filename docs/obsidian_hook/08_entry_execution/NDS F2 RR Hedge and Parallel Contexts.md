---
title: NDS F2 RR Hedge and Parallel Contexts
aliases:
  - F2 Reward Risk Filter
  - F2 Hedge Context Policy
status: implemented
phase: F2 waist-break Point2
---

# NDS F2 RR Hedge and Parallel Contexts

## Canonical links

- [[NDS F2 Waist-Break Point2 Limit Setup]]
- [[NDS F2 Waist Limit Backtest]]
- [[NDS_ENTRY_EXECUTION_MOC]]

## Reward/Risk gate

```text
RR = abs(Target - Entry) / abs(Entry - Stop)
```

Defaults:

```text
Use filter = true
Minimum RR = 1.0
```

A setup below the threshold is repriced by moving only its limit farther behind the F2 Waist toward the fixed F1-waist Stop. If a valid executable limit cannot provide the threshold, it is rejected.

## Context identity

A context is the exact F2 body version, including direction, scale, parent F1 waist, F2 origin, F2 waist and F2 Leg2 endpoint. The deterministic setup hash is the deduplication authority.

## Parallel policies

```text
Opposite-direction hedge = enabled by default
Same-direction independent contexts = enabled by default
```

The same context remains one-attempt-only.

## MT5 account-mode boundary

Independent same-symbol positions require a hedging account. Netting/exchange accounts block a second managed exposure because separate Stop and Target ownership cannot be preserved.

## Optional cap

```text
MaxConcurrentManagedExposures = 0
```

Zero means no strategy-level numerical cap.


## Near-duplicate stop-space arbitration

```text
Overlap % = shared stop-corridor length / narrower corridor length × 100
```

Defaults:

```text
Use overlap deduplication = true
Threshold = 80%
Winner = wider same-direction corridor
```

The threshold is an input and may be set to 70%. Opposite-direction hedge contexts are not merged.

- same-bar duplicates are resolved before sending;
- wider pending replaces narrower pending;
- an already-filled position is not replaced.
