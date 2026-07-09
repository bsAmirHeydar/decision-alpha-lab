# Phase 06 Hotfix003 — Validation Plan

## Test 1 — comments off

Attach the expert and confirm that the chart does not show the large `Comment()` panel.

Expected:

```text
No top-left multi-line comment panel.
Visual objects may still appear.
```

## Test 2 — both charts receive drawings

Open both symbol charts manually or allow the EA to open them.

Expected:

```text
SPXUSD chart receives SPXUSD symbol-local objects.
NDXUSD chart receives NDXUSD symbol-local objects.
```

## Test 3 — confirmed SELL divergence

Expected hunter chart:

```text
reference high -> current high
```

Expected clean chart:

```text
reference high -> current high that did not hunt
```

## Test 4 — confirmed BUY divergence

Expected hunter chart:

```text
reference low -> current low
```

Expected clean chart:

```text
reference low -> current low that did not hunt
```

## Test 5 — invalidated double hunt

Expected:

```text
both symbol charts can receive invalidated visual packages
status label = INVALIDATED
color = invalidated color
```

## Test 6 — scale correctness

Because each chart receives only its own symbol-local price objects, no cross-symbol price scale distortion should appear in normal dual mode.

## Test 7 — no trading

Expected:

```text
no orders
no positions
no stop placement
no target placement
no position management
```
