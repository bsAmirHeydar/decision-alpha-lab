---
title: "ADR_003_PRODUCT_FIELD_EXCLUDED_FROM_SEMANTIC_HASH — Product Field Excluded From Semantic Hash"
status: accepted
phase: FP-I14
---
# Product Field Excluded From Semantic Hash

## Decision

Product Field Excluded From Semantic Hash is mandatory for FP-I14. The decision preserves deterministic cross-product evidence and prevents the Diagnostic EA from becoming a second strategy implementation.

## Consequences

The implementation uses explicit contracts, closed reason codes, append-only evidence, and fail-closed mismatch handling. Any incompatible change requires a phase-version increment and regenerated acceptance artifacts.
