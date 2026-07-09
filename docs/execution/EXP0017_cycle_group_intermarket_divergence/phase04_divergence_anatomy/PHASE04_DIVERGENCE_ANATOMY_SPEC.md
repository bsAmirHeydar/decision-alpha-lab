# Phase 04 Divergence Anatomy Specification

## Purpose

Phase 04 turns the raw hunt field into a raw divergence field.

The robot can now answer:

```text
Did exactly one symbol hunt the high reference?
Did exactly one symbol hunt the low reference?
Which symbol is the hunter?
Which symbol is clean?
Is the raw divergence BUY or SELL?
```

## Inherited contracts

Phase 04 inherits these contracts without modification:

```text
Phase 01: New York 18:00 -> 17:00 trading day
Phase 02: all completed previous same-day CG cycles are reference candidates
Phase 03: hunt is touch/break/equality with high/low only
```

Phase 04 must not recreate time, reference, or hunt logic. It consumes Phase 03 hunt states.

## Sell divergence candidate

A sell divergence candidate exists when exactly one symbol hunts its own high reference and the other symbol does not hunt its own high reference.

```text
Symbol A high hunted, Symbol B high not hunted => SELL divergence candidate, hunter=A, clean=B
Symbol B high hunted, Symbol A high not hunted => SELL divergence candidate, hunter=B, clean=A
```

The future trade candidate is the clean symbol, but Phase 04 does not create trade permission.

## Buy divergence candidate

A buy divergence candidate exists when exactly one symbol hunts its own low reference and the other symbol does not hunt its own low reference.

```text
Symbol A low hunted, Symbol B low not hunted => BUY divergence candidate, hunter=A, clean=B
Symbol B low hunted, Symbol A low not hunted => BUY divergence candidate, hunter=B, clean=A
```

The future trade candidate is the clean symbol, but Phase 04 does not execute.

## Symmetric hunt is not divergence

If both symbols hunt the high side, the high-side relationship is not sell divergence.

If both symbols hunt the low side, the low-side relationship is not buy divergence.

In Phase 04 this is recorded as:

```text
symmetric_high_hunt_no_divergence
symmetric_low_hunt_no_divergence
```

This is not yet the later confirmed-signal invalidation layer. It is only a raw divergence classification rule.

## Mixed-direction candidates are allowed

If the same reference relationship produces both a high-side one-sided hunt and a low-side one-sided hunt, Phase 04 records both independently.

No direction suppresses the other before statistics and before the later conflict-governance layer.
