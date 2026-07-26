---
tags: [exp0019, faerie-protocol, fp-i08, weekly-context]
status: normative
phase: FP-I08
version: 1.0.0
last_updated: 2026-07-13
language: en
---
# ADR — Missing Weekly Data Fails Closed

## Status
Accepted.

## Decision
No-active and no-data are distinct; incomplete data blocks.

## Consequences
- Contract, Python, MQL5 mirror, schemas, vectors, and tests encode the decision.
- Semantic changes require a new phase version and rebaseline.
