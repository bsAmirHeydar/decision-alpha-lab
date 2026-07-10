---
title: Phase 52 Same Direction F123 Exit
status: implemented
version: 1.0.0
updated: 2026-07-10
---
# Phase 52 Same-Direction F123 Exit

## Exit thesis

After the limit fills, the strategy does not use a fixed profit target. It waits until the market forms a complete canonical F1 → F2 → F3 chain in the position direction.

```text
BUY position  → wait for bullish F1, bullish F2, bullish F3
SELL position → wait for bearish F1, bearish F2, bearish F3
```

## Required evidence

A candidate exit F3 must satisfy all of the following:

```text
level = F3
same direction as broker position
visible_main = true
f3_terminal_complete = true
status ∈ {COMPLETED, LOCKED}
explicit visible F1 in the same sequence
explicit visible F2 in the same sequence
F1 is authorized to spawn F2
F2 is authorized to spawn F3
```

With the default strict setting:

```text
F1 origin time > broker position open time
F2 origin time > broker position open time
F3 completion time > broker position open time
```

Thus an F3 that was already developing before entry cannot close the new trade merely because it completed afterward.

## Exit selection

If more than one qualifying F3 is present in reconstructed history, the earliest qualifying post-entry completion is selected.

## Close action

The position is closed by ticket at market after the canonical closed-bar reconstruction exposes the qualifying F3. A successful trade-server return is followed by a local position-existence check; the report is marked closed only when the ticket no longer remains open.

## Timing semantics

The F engine is closed-bar authoritative. Consequently, the structural exit is issued on the first engine run after the F3 becomes canonical, not on an unconfirmed intrabar shape.
