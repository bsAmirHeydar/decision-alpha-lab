---
title: "ADR_012_TRACE_TRUNCATION_IS_NEGATIVE_CONTROL — Trace Truncation Is Negative Control"
status: accepted
phase: FP-I14
---
# Trace Truncation Is Negative Control

## Decision

Trace Truncation Is Negative Control is mandatory for FP-I14. The decision preserves deterministic cross-product evidence and prevents the Diagnostic EA from becoming a second strategy implementation.

## Consequences

The implementation uses explicit contracts, closed reason codes, append-only evidence, and fail-closed mismatch handling. Any incompatible change requires a phase-version increment and regenerated acceptance artifacts.
