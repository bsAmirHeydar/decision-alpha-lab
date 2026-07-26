---
title: "ADR_007_EXPORT_IS_APPEND_ONLY — Export Is Append Only"
status: accepted
phase: FP-I14
---
# Export Is Append Only

## Decision

Export Is Append Only is mandatory for FP-I14. The decision preserves deterministic cross-product evidence and prevents the Diagnostic EA from becoming a second strategy implementation.

## Consequences

The implementation uses explicit contracts, closed reason codes, append-only evidence, and fail-closed mismatch handling. Any incompatible change requires a phase-version increment and regenerated acceptance artifacts.
