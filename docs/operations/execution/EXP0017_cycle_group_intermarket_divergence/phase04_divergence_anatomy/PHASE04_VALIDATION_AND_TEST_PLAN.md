# Phase 04 Validation And Test Plan

## Test 1 — No one-sided hunt

When neither symbol hunts a reference side, no divergence candidate should appear.

## Test 2 — Symbol A high hunt only

Expected:

```text
SELL candidate
hunter = Symbol A
clean = Symbol B
side = HIGH
```

## Test 3 — Symbol B high hunt only

Expected:

```text
SELL candidate
hunter = Symbol B
clean = Symbol A
side = HIGH
```

## Test 4 — Symbol A low hunt only

Expected:

```text
BUY candidate
hunter = Symbol A
clean = Symbol B
side = LOW
```

## Test 5 — Symbol B low hunt only

Expected:

```text
BUY candidate
hunter = Symbol B
clean = Symbol A
side = LOW
```

## Test 6 — Both symbols high hunt

Expected:

```text
no SELL divergence candidate
symmetric_high_no_divergence_count increments
```

## Test 7 — Both symbols low hunt

Expected:

```text
no BUY divergence candidate
symmetric_low_no_divergence_count increments
```

## Test 8 — Mixed high/low behavior

If high-side and low-side one-sided conditions are both present, both candidates must be shown independently.

## Test 9 — Missing M1 data

Missing data must not be treated as clean behavior. No candidate should be created from incomplete data.
