---
title: "ADR_011_BUFFER_AND_VISUALS_ARE_COMPARED — Buffer And Visuals Are Compared"
status: accepted
phase: FP-I14
---
# Buffer And Visuals Are Compared

## Decision

Buffer And Visuals Are Compared is mandatory for FP-I14. The decision preserves deterministic cross-product evidence and prevents the Diagnostic EA from becoming a second strategy implementation.

## Consequences

The implementation uses explicit contracts, closed reason codes, append-only evidence, and fail-closed mismatch handling. Any incompatible change requires a phase-version increment and regenerated acceptance artifacts.
