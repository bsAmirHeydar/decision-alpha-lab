---
phase: FP-I05
experiment: EXP0019
context_id: FP-CONTEXT-001
status: normative
phase_version: 1.0.0
language: en
last_updated: 2026-07-13
---
# Hunter Touch Is Non-Consuming

## Decision

A hunter observation changes FRESH to HUNTER_SEEN but preserves hunt eligibility. Only a protected touch consumes the reference.

## Consequences

- Identity and cache behavior remain deterministic.
- Failure evidence remains explicit.
- Any alternative requires a versioned policy and migration evidence.

## Verification

The Python tests, MQL5 self-test/static checks and conformance vectors exercise the accepted and rejected paths.
