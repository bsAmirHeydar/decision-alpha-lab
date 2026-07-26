---
title: "ADR_009_LOCAL_RUNTIME_EVIDENCE_IS_EXTERNAL_GATE — Local Runtime Evidence Is External Gate"
status: accepted
phase: FP-I14
---
# Local Runtime Evidence Is External Gate

## Decision

Local Runtime Evidence Is External Gate is mandatory for FP-I14. The decision preserves deterministic cross-product evidence and prevents the Diagnostic EA from becoming a second strategy implementation.

## Consequences

The implementation uses explicit contracts, closed reason codes, append-only evidence, and fail-closed mismatch handling. Any incompatible change requires a phase-version increment and regenerated acceptance artifacts.
