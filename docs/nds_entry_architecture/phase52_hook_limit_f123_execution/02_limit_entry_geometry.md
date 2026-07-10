---
title: Phase 52 Limit Entry Geometry
status: implemented
version: 1.0.0
updated: 2026-07-10
---
# Phase 52 Limit Entry Geometry

## Entry anchor

The limit price is the Hook raw terminal price already carried by `FP_HookPhase02Sequence.resolve_price`.

```text
Positive Hook terminal = lowest valid terminal valley
Negative Hook terminal = highest valid terminal peak
```

Therefore:

```text
Positive Hook → Buy Limit at resolve_price
Negative Hook → Sell Limit at resolve_price
```

The engine rounds the price to the symbol trade tick size and verifies that the pending price is on the correct side of the current market by at least the broker minimum placement distance.

## Structural death and stop

The structural death anchor is:

```text
death_boundary_price when available
otherwise origin_price
```

The protective stop is placed beyond that boundary:

```text
buffer = stop_buffer_points × point
       + stop_spread_multiplier × current spread
```

- bullish setup: stop below death/origin;
- bearish setup: stop above death/origin.

If the broker minimum stop distance is larger, the stop is moved farther away from entry, never inward across the death boundary.

## Target

No fixed take-profit is attached:

```text
TP = 0
```

The planned exit is structural: a completed same-direction post-entry F123 chain.

## Broker capability gates

Before sending, the engine checks:

- terminal, MQL program, and account trade permission;
- symbol trade mode and directional permission;
- support for limit orders;
- support for stop-loss orders;
- valid symbol tick, volume, quote, and stop specifications.

A rejected geometry remains an audited blocked setup; it is not converted into a market order.
