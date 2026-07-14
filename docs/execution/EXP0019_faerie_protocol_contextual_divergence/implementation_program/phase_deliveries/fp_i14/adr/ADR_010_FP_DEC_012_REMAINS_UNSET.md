---
title: "ADR_010_FP_DEC_012_REMAINS_UNSET — Fp Dec 012 Remains Unset"
status: accepted
phase: FP-I14
---
# Fp Dec 012 Remains Unset

## Decision

Fp Dec 012 Remains Unset is mandatory for FP-I14. The decision preserves deterministic cross-product evidence and prevents the Diagnostic EA from becoming a second strategy implementation.

## Consequences

The implementation uses explicit contracts, closed reason codes, append-only evidence, and fail-closed mismatch handling. Any incompatible change requires a phase-version increment and regenerated acceptance artifacts.
