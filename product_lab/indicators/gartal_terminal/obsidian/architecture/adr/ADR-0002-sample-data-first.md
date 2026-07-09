---
type: adr
product: gartal terminal
status: accepted
language: en
adr: 0002
---

# ADR-0002 — Sample Data First

## Decision

Build and validate the full rendering/filter/alert pipeline with sample events before connecting live Forex Factory fetching.

## Rationale

This separates UI and architecture bugs from source/parser bugs.

## Consequence

The product must have `InpUseSampleData=true` mode until source adapter is stable.

## Enforcement

No UI module may depend on live network availability.
