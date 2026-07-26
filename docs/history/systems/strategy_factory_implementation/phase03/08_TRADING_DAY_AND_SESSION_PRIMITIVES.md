---
title: "Trading Day and Session Primitives"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Trading day

Calendar date and trading day are not interchangeable. `TradingDayId` applies:

1. a selected timezone;
2. a local rollover minute;
3. a date identity after the rollover shift.

This supports broker day, UTC day, New York trading day, and future custom trading calendars.

## Sessions

Sessions are data-driven definitions containing:

- session ID;
- enabled flag;
- timezone kind;
- fixed offset where applicable;
- start and end minute;
- weekday mask.

Intervals use half-open semantics. Cross-midnight sessions are supported. Equal start and end represent an intentional full-day session.

## Ownership

The session schedule class resolves membership; it does not define trading doctrine. A strategy may later choose which session IDs matter, but it may not calculate session time independently.

## Ambiguity policy

Overlapping sessions are permitted only when their order and intended precedence are documented. The current resolver returns the first match. Production manifests must therefore use deterministic ordering and tests.

## Future extension

Holiday and early-close calendars are deferred. They will be implemented as schedule providers, not hard-coded conditions inside anatomy plugins.
