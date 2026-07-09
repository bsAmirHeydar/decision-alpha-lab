---
type: adr
product: gartal terminal
status: accepted
language: en
adr: 0001
---

# ADR-0001 — Source Adapter Boundary

## Decision

Keep source fetching isolated inside `GartalNewsCalendarClient.mqh` and keep parsing inside `GartalNewsParser.mqh`.

## Rationale

Forex Factory direct parsing can break if page markup changes. If fetching, parsing, rendering, and alerts are mixed together, the entire product becomes fragile.

## Consequence

The renderer never receives raw HTML. It only receives canonical `GT_NewsEvent` records.

## Enforcement

Any code that calls `WebRequest` outside the source client is rejected.
