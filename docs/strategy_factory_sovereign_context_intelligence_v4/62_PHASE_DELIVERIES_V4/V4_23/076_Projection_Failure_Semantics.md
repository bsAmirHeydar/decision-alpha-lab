---
title: SAED V4-23 — Projection Failure Semantics
status: accepted-reference
version: 1.0.0
phase: SAED_V4_23
evidence_scope: local-deterministic-logged-replay-and-synthetic-veto-reference
claim_ceiling: offline-research-only
tags: [saed-v4, v4-23, offline-policy, research-only]
---
# SAED V4-23 — Projection Failure Semantics

## Purpose
This note defines **Projection Failure Semantics** as a normative component of the V4-23 Offline Policy Research phase. The component exists inside an additive, closed-contract laboratory. It consumes immutable V4-22 lineage and known-time logged trajectories, and it cannot mutate Context truth, Treatment DSL, promotion admission, runtime compilation, portfolio risk or broker execution.

## Contract
All inputs are exact-versioned, content-addressed and validated with unknown fields rejected. Episode, cluster, state, action, reward, behavior probability, mask and timestamp semantics remain explicit. Any absent lineage, future suffix, protected evidence, unsupported action, invalid reward decomposition or authority-bearing flag fails closed.

## Engineering behavior
The deterministic Python reference uses canonical JSON, bounded standard-library numerics and stable tie-breaking. Research trials are individually identified, budgeted and written to immutable ledgers. Candidate policies remain probability distributions over the frozen action space, always retain the safe Skip path, and are projected toward observed support before evaluation.

## Scientific behavior
The laboratory challenges every candidate with behavior support diagnostics, effective sample size, clipped importance weights, reward audits, WIS, PDIS, FQE and doubly-robust estimates. Confidence intervals and estimator disagreement are reported rather than hidden. V4-22 synthetic paths can only veto or falsify; they contribute zero positive edge evidence. The manual baseline is never removed.

## Failure semantics
A contract mismatch rejects the artifact. A support violation blocks the challenger. A projection violation falls back to the manual baseline. OPE instability triggers abstention. Budget exhaustion terminates the research family. Synthetic exploitability or fidelity failure vetoes the candidate. No local result can be waived into promotion, runtime or execution authority.

## Evidence and verification
Required evidence includes input/output hashes, closed-schema validation, golden replay, negative and mutation tests, support and reward reports, OPE intervals, baseline preservation, trial/exposure ledgers, model-risk review and security review. MQL5 evidence in this phase is static only; actual MetaEditor compilation remains `pending_local_windows`.

## Traceability
Parent phase: [[V4_22_Generative_Path_Stress_Lab]]. Current map: [[00_MOC_V4_23_Offline_Policy_Research]]. Next concept: [[OPE_Contract]]. Next phase: [[V4_24_Conformal_OOD_And_Selective_Control]].
