---
tags: [exp0019, faerie-protocol, fp-i08, weekly-context]
status: normative
phase: FP-I08
version: 1.0.0
last_updated: 2026-07-13
language: en
---
# ADR — Reuse FP-I06 and FP-I07

## Status
Accepted.

## Decision
WW reuses generic M1 hunt/candidate and closed-host confirmation engines; it does not fork them.

## Consequences
- Contract, Python, MQL5 mirror, schemas, vectors, and tests encode the decision.
- Semantic changes require a new phase version and rebaseline.
