---
title: "ADR_008_NO_TRADE_APIS_IN_DIAGNOSTIC_EA — No Trade Apis In Diagnostic Ea"
status: accepted
phase: FP-I14
---
# No Trade Apis In Diagnostic Ea

## Decision

No Trade Apis In Diagnostic Ea is mandatory for FP-I14. The decision preserves deterministic cross-product evidence and prevents the Diagnostic EA from becoming a second strategy implementation.

## Consequences

The implementation uses explicit contracts, closed reason codes, append-only evidence, and fail-closed mismatch handling. Any incompatible change requires a phase-version increment and regenerated acceptance artifacts.
