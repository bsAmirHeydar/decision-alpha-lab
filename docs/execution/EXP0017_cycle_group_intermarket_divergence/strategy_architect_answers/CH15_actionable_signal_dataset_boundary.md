# CH15 — Actionable Signal Dataset Boundary

## Core boundary

The primary dataset for EXP0017 should include only confirmed, valid, tradeable divergences.

This means the report is not a record of every market curiosity. It is the statistical population of signals that the strategy would actually allow.

## What enters the primary sample

A signal enters the main statistical sample when:

1. it belongs to a valid cycle group;
2. it uses a same-day reference;
3. one symbol hunts the reference;
4. the other symbol remains clean;
5. the confirmation candle closes;
6. the divergence remains valid at that close;
7. the signal has trade permission;
8. the signal has an identifiable direction;
9. the clean symbol is known;
10. the cycle-group type is recorded.

## What does not enter the primary sample

The following do not enter the primary report at this stage:

- raw intrabar hunt without confirmation;
- possible divergence before candle close;
- double-hunt invalidation before confirmation;
- visual asymmetry that never becomes tradeable;
- emotional quality judgment;
- unconfirmed idea;
- manual opinion about quality;
- previous-day reference behavior;
- events outside the current strategy boundary.

## Why this matters

If unconfirmed events are mixed with confirmed signals, the statistics become polluted.

The goal is to measure the real trading doctrine, not every pre-signal shadow.

## Optional secondary archives

Later, the strategy may create secondary archives for:

- failed pre-confirmation divergences;
- raw hunts without clean-symbol confirmation;
- near misses;
- almost double-hunt cases;
- events that would become valid under alternative confirmation rules.

But these are not primary Chapter 15 samples.

## Dataset purity principle

The primary sample should answer one question:

> What happens after the strategy receives a confirmed signal that it is allowed to trade?

Everything else belongs to a different research layer.
