---
title: "Self-Test and Fixture Reference"
---

# Self-Test and Fixture Reference

The MQL5 self-test is intentionally independent from broker execution.

## Fixture Clock

Returns a fixed UTC millisecond value. This prevents wall-clock nondeterminism.

## Fixture Anatomy Provider

Creates one valid canonical event with:

- strategy `fixture_strategy`;
- NQ as primary symbol;
- ES as reference symbol;
- LONG direction;
- explicit event, known and confirmation times;
- deterministic cluster and source identities.

It emits exactly once after a tick.

## Fixture Feature Provider

Builds one valid snapshot containing `fixture_strength = 0.75`. Its known time is inherited from the event and its snapshot time is the confirmation time.

## Fixture Sink

Counts events and snapshots without file I/O.

## Assertions

The self-test verifies configuration, bus sequencing, runtime initialization, READY/RUNNING/STOPPED states, one event, one snapshot, sink counts and absence of live authority.

A local compile or execution failure must be converted into a regression fixture or code correction before Phase 03 begins.
