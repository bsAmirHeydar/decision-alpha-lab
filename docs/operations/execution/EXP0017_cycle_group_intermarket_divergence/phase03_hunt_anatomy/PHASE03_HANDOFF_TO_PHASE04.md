# Phase 03 Handoff to Phase 04

Phase 04 should consume the raw hunt field and build the first divergence anatomy layer.

## Phase 03 outputs available to Phase 04

```text
current-cycle high/low per symbol
reference high/low per symbol
high_hunted flag per symbol
low_hunted flag per symbol
one-symbol high hunt flag
one-symbol low hunt flag
both-symbol high hunt flag
both-symbol low hunt flag
missing data state
```

## Phase 04 responsibility

Phase 04 should decide whether the raw hunt asymmetry forms a divergence candidate:

```text
one-symbol high hunt -> sell divergence candidate
one-symbol low hunt  -> buy divergence candidate
```

## Phase 04 must still avoid trading

The next phase should still remain an anatomy layer. It should build divergence candidates, not execute trades.

## Phase 04 must keep missing data strict

Missing reference or missing current-cycle range must prevent divergence candidate construction.
