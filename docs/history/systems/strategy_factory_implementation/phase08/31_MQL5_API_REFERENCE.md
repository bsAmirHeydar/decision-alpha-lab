---
title: "MQL5 API Reference"
phase: 08
status: canonical
---
# MQL5 API Reference

Primary APIs are CSF08PolicyRegistry.RegisterEntry/RegisterStop/RegisterExit/Compile, CSF08CandidateMatrixPlan.Add/Compile, CSF08CandidateEngine.Initialize/BuildMatrix/PopCandidate and the typed entry, stop and exit policy interfaces.

## Operational rules

- All identifiers and versions are explicit.
- Inputs are immutable and causal.
- Work and memory are bounded.
- Failure is explicit and fail-closed.
- No previous strategy is integrated in this phase.
- Every future extension must preserve deterministic candidate identity.
