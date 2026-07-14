---
title: "ADR_002_THREE_PRODUCT_CONSENSUS — Three Product Consensus"
status: accepted
phase: FP-I14
---
# Three Product Consensus

## Decision

Three Product Consensus is mandatory for FP-I14. The decision preserves deterministic cross-product evidence and prevents the Diagnostic EA from becoming a second strategy implementation.

## Consequences

The implementation uses explicit contracts, closed reason codes, append-only evidence, and fail-closed mismatch handling. Any incompatible change requires a phase-version increment and regenerated acceptance artifacts.
