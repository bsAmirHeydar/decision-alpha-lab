# Phase 06 Hotfix009 — Non-Host Frontier Synchronization

## Observed defect

The expert was attached to one configured symbol chart, while Phase 06 also created symbol-local objects on the second chart. The host chart showed the corrected extreme-frontier behavior, but the non-host chart could retain lines whose local reference was stale or whose object belonged to a previous build.

The defect was not in `CopyRates` ownership or in the pair calculation. Both symbols were already read centrally. The divergence appeared at the state-to-render boundary.

## Root cause A — local frontier state was discarded

`SCGCExtremeFrontierEligibility` contains four independent facts for the selected side:

```text
symbol_a_high_frontier
symbol_b_high_frontier
symbol_a_low_frontier
symbol_b_low_frontier
```

Before Hotfix009, the final signal retained only the pair-level decision. The visual layer received symbol-local prices but not symbol-local frontier authority.

That created an invalid implicit assumption:

```text
pair accepted => every local chart leg is safe to draw
```

The assumption is unsafe whenever permissive pair mode is loaded, especially from an older `.set` file, or whenever a future caller creates a pair-level signal using an OR rule.

## Root cause B — foreign-chart deletion was not verified

The visual engine can create and delete objects on another open chart by chart ID. Deletion is queued. The previous cleanup performed one delete pass and treated queue acceptance as completed deletion.

The non-host chart therefore had no postcondition proving:

```text
owned object count after cleanup == 0
```

## New invariant

A price object may be drawn on a symbol chart only when all of these are true:

```text
signal is drawable
chart symbol is one of the configured symbols
symbol-local price data exists
that exact symbol reference is frontier-valid
```

Pair-level signal permission and chart-local drawing permission are now separate explicit decisions.

## Cleanup postcondition

For every configured chart that already exists:

```text
repeat bounded delete pass
synchronize through object query
stop when no EXP0017_P06_ object remains
```

If objects still remain after four passes, the expert emits a journal warning with chart ID, symbol, and remaining count.

## Scope

Modified:

- `CGC_Types.mqh`
- `CGC_ConfirmationField.mqh`
- `CGV_Drawing.mqh`
- `EXP0017_CG_Visual_Ledger_Anatomy.mq5`

Not modified:

- time anatomy
- reference aggregation
- hunt semantics
- protected-reference lifecycle rules
- signal IDs
- CSV schema
- order execution
- outcome/statistical/model phases
