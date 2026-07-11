---
title: "Trade Candidate Identity"
phase: 08
status: canonical
---
# Trade Candidate Identity

Candidate identity binds the template hash, event, snapshot, context frame, strategy version, runtime generation, creation time, all three geometry hashes and source lineage. Identical ordered inputs produce the same candidate ID. Any parameter or geometry change creates a distinct candidate.

## Operational rules

- All identifiers and versions are explicit.
- Inputs are immutable and causal.
- Work and memory are bounded.
- Failure is explicit and fail-closed.
- No previous strategy is integrated in this phase.
- Every future extension must preserve deterministic candidate identity.
