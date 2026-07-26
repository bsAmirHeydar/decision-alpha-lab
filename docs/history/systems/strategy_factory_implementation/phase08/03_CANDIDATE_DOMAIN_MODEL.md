---
title: "Candidate Domain Model"
phase: 08
status: canonical
---
# Candidate Domain Model

The domain is decomposed into PolicyDescriptor, PolicyParameters, CandidateTemplate, EntryPlan, StopPlan, ExitPlan and TradeCandidate. This prevents one monolithic setup function from silently combining market interpretation, execution geometry and risk. Each record is versioned, hashable and independently testable.

## Operational rules

- All identifiers and versions are explicit.
- Inputs are immutable and causal.
- Work and memory are bounded.
- Failure is explicit and fail-closed.
- No previous strategy is integrated in this phase.
- Every future extension must preserve deterministic candidate identity.
