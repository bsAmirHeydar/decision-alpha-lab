---
title: "ADR_006_CHECKPOINT_IS_CACHE — Checkpoint Is Cache"
status: accepted
phase: FP-I14
---
# Checkpoint Is Cache

## Decision

Checkpoint Is Cache is mandatory for FP-I14. The decision preserves deterministic cross-product evidence and prevents the Diagnostic EA from becoming a second strategy implementation.

## Consequences

The implementation uses explicit contracts, closed reason codes, append-only evidence, and fail-closed mismatch handling. Any incompatible change requires a phase-version increment and regenerated acceptance artifacts.
