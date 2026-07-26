---
title: "Exact Registry Version"
tags: [atomic-concept, uce-i16]
status: canonical
doc_version: 1.0.0
---
# Exact Registry Version

## Definition
Exact Registry Version is a first-class governance and runtime concept in the UCE-I16 onboarding factory. It is represented by an explicit machine-readable field or artifact and cannot be inferred from comments or naming conventions.

## Invariant
The concept participates in canonical serialization, deterministic identity, executable validation, negative testing and evidence retention. Absence or ambiguity fails closed.

## Operational consequence
A context package cannot advance to migration or downstream portfolio eligibility when this concept is missing, contradictory or unverified.

## Related artifacts
- `strategy_factory_onboarding_v3`
- `onboarding_*.schema.json`
- `UCEI16_*.mqh`
- UCE-I16 acceptance evidence
