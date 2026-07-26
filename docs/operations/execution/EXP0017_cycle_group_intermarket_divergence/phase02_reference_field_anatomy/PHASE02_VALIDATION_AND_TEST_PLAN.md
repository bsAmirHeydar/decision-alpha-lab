# Phase 02 Validation and Test Plan

## Test 1 — Symbol selection

Attach the expert and confirm both symbols are selected:

```text
SPXUSD
NDXUSD
```

If the broker uses different names, change inputs.

## Test 2 — M1 history availability

The chart panel should show non-zero M1 bars for recent reference cycles.

If `bars=0`, load M1 history for both symbols.

## Test 3 — `cg_30m` reference windows

At any time inside the trading day, compare the displayed recent `cg_30m` reference windows against the expected 18:00 NY aligned calendar.

Example:

```text
18:00-18:29
18:30-18:59
19:00-19:29
```

## Test 4 — current-cycle exclusion

The displayed references must stop at the last completed cycle before the current cycle.

The current cycle must not appear as a reference.

## Test 5 — non-standard CGs

Enable only one of these groups at a time:

```text
cg_3m
cg_9m
cg_18m
cg_72m
cg_150m
```

Confirm that M1 aggregation still builds valid high/low references.

## Test 6 — partial final cycle

Near the end of the 18:00-17:00 NY trading day, confirm that partial last-cycle behavior still follows the Phase 01 calendar contract.

## Test 7 — no-trade safety

Confirm that the expert never sends orders, never calculates risk, and never prints trade commands.

Phase 02 is a reference-field observer only.
