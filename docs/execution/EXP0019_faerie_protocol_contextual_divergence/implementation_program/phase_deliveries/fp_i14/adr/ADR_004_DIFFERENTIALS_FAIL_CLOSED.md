---
title: "ADR_004_DIFFERENTIALS_FAIL_CLOSED — Differentials Fail Closed"
status: accepted
phase: FP-I14
---
# Differentials Fail Closed

## Decision

Differentials Fail Closed is mandatory for FP-I14. The decision preserves deterministic cross-product evidence and prevents the Diagnostic EA from becoming a second strategy implementation.

## Consequences

The implementation uses explicit contracts, closed reason codes, append-only evidence, and fail-closed mismatch handling. Any incompatible change requires a phase-version increment and regenerated acceptance artifacts.
