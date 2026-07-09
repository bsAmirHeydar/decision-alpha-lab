---
type: adr
product: gartal terminal
status: accepted
language: en
adr: 0003
---

# ADR-0003 — Dashboard Runtime Config

## Decision

Dashboard controls mutate runtime filter state, not static MT5 `input` variables.

## Rationale

MT5 inputs are not intended for live interactive toggling. The dashboard must be a runtime control center.

## Consequence

There are two config layers:

1. startup defaults from indicator inputs;
2. runtime dashboard state.

## Enforcement

Dashboard click handler returns filter-state changes and triggers rerender.
