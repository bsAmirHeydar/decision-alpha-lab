# Phase 03 Validation and Test Plan

## Test 1 — No-trade safety

Attach the expert and confirm:

```text
No orders are opened
No positions are modified
No trade permission exists
No buy/sell labels are generated
```

## Test 2 — High hunt equality

Create or locate a case where current-cycle high equals a previous reference high.

Expected:

```text
high_hunted = true
```

## Test 3 — High hunt break

Create or locate a case where current-cycle high is above a previous reference high.

Expected:

```text
high_hunted = true
```

## Test 4 — Low hunt equality

Create or locate a case where current-cycle low equals a previous reference low.

Expected:

```text
low_hunted = true
```

## Test 5 — Low hunt break

Create or locate a case where current-cycle low is below a previous reference low.

Expected:

```text
low_hunted = true
```

## Test 6 — No close requirement

Confirm that the system flags a hunt even if the current candle has not closed beyond the reference.

Expected:

```text
Wick touch is enough
Close beyond is not checked
```

## Test 7 — Symbol-local comparison

Confirm that SPXUSD is compared only to SPXUSD reference high/low and NDXUSD only to NDXUSD reference high/low.

Expected:

```text
No absolute cross-symbol price comparison exists
```

## Test 8 — Nonstandard CG behavior

Test `cg_3m`, `cg_9m`, `cg_18m`, `cg_72m`, and `cg_150m`.

Expected:

```text
M1 aggregation produces current ranges and hunt states
```

## Test 9 — Missing data safety

Temporarily use a symbol with missing M1 data.

Expected:

```text
current_range_missing or reference_missing
not clean-symbol behavior
not divergence
```

## Test 10 — Display sanity

Enable only one or two CGs and compare chart highs/lows manually.

Expected:

```text
H, L, H+L, and - markers match the visible chart structure
```
