---
title: "ADR_001_ONE_CANONICAL_TRACE_CONTRACT — One Canonical Trace Contract"
status: accepted
phase: FP-I14
---
# One Canonical Trace Contract

## Decision

One Canonical Trace Contract is mandatory for FP-I14. The decision preserves deterministic cross-product evidence and prevents the Diagnostic EA from becoming a second strategy implementation.

## Consequences

The implementation uses explicit contracts, closed reason codes, append-only evidence, and fail-closed mismatch handling. Any incompatible change requires a phase-version increment and regenerated acceptance artifacts.
