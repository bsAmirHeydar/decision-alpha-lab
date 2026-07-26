---
title: "ADR_005_DUPLICATE_IDENTICAL_IS_IDEMPOTENT — Duplicate Identical Is Idempotent"
status: accepted
phase: FP-I14
---
# Duplicate Identical Is Idempotent

## Decision

Duplicate Identical Is Idempotent is mandatory for FP-I14. The decision preserves deterministic cross-product evidence and prevents the Diagnostic EA from becoming a second strategy implementation.

## Consequences

The implementation uses explicit contracts, closed reason codes, append-only evidence, and fail-closed mismatch handling. Any incompatible change requires a phase-version increment and regenerated acceptance artifacts.
