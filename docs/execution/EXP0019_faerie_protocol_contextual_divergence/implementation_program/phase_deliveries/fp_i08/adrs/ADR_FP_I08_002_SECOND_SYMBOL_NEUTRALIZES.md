---
tags: [exp0019, faerie-protocol, fp-i08, weekly-context]
status: normative
phase: FP-I08
version: 1.0.0
last_updated: 2026-07-13
language: en
---
# ADR — Second Symbol Neutralizes

## Status
Accepted.

## Decision
Only the Protected symbol touching the corresponding weekly side neutralizes a confirmed WW.

## Consequences
- Contract, Python, MQL5 mirror, schemas, vectors, and tests encode the decision.
- Semantic changes require a new phase version and rebaseline.
