---
title: "Golden Candidate Fixtures"
phase: 08
status: canonical
---
# Golden Candidate Fixtures

A golden fixture contains one anatomy event, one immutable feature snapshot, one context frame, one compiled policy registry, one matrix and exact candidate IDs and geometry. Every real policy bug must become a fixture before the fix is accepted.

## Operational rules

- All identifiers and versions are explicit.
- Inputs are immutable and causal.
- Work and memory are bounded.
- Failure is explicit and fail-closed.
- No previous strategy is integrated in this phase.
- Every future extension must preserve deterministic candidate identity.
