---
title: "Duplicate Prevention"
phase: 08
status: canonical
---
# Duplicate Prevention

Duplicate template identities are rejected at compile time. Duplicate candidate IDs are rejected at runtime. Event-level deduplication remains owned by anatomy. Candidate deduplication ensures two policies cannot create hidden duplicate exposure merely because they used different code paths.

## Operational rules

- All identifiers and versions are explicit.
- Inputs are immutable and causal.
- Work and memory are bounded.
- Failure is explicit and fail-closed.
- No previous strategy is integrated in this phase.
- Every future extension must preserve deterministic candidate identity.
