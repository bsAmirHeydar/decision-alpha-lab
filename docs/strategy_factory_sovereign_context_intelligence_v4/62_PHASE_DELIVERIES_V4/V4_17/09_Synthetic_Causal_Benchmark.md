---
title: SAED V4-17 — Synthetic Causal Benchmark
status: implemented-reference
version: 1.0.0
created: '2026-07-16'
updated: '2026-07-16'
capability_tier: research-reference
tags:
  - saed-v4
  - v4-17
  - causal-mechanism-discovery
---

# SAED V4-17 — Synthetic Causal Benchmark

## Purpose

Watermarked benchmark generation and ground-truth isolation. This note is part of the closed-contract implementation of SAED V4-17. It must be read under the evidence firewall: all generated rows, graphs, interventions, environments, outcomes, scores and stress results are deterministic synthetic reference evidence. They cannot support a real causal, economic, promotion, runtime or production claim.

## Contract

The component consumes only immutable V4-16 evidence through the hash-bound handoff. Variable identity, temporal tier, environment assignment, graph constraints, evidence role, split and authority are explicit. Unknown fields, unknown variables, future-to-past edges, cycles, protected-evidence requests and causal-claim escalation fail closed. Every output carries content-addressed identity and remains non-production.

## Engineering semantics

The implementation preserves a correlation baseline, adds a temporally constrained graph challenger, evaluates conditional associations, regularized structural equations, residual diagnostics, environment invariance, negative controls, hidden-confounder sensitivity, edge reversal, environment permutation and support overlap. Graphical compatibility is not identification. Orthogonal residualization is reported as an association score and is never labeled a treatment effect.

## Evidence and review

Acceptance requires closed schemas, deterministic replay, complete compute and exposure accounting, zero protected evidence exposure, zero hidden-evaluation queries, explicit claim tiering, negative-control evidence, baseline preservation, immutable checkpoints, a narrow V4-18 handoff and independent reproduction. MetaEditor compilation, real-data replication, prospective paper, shadow, micro-live and live evidence remain external and unclaimed.

## Failure behavior

A lineage mismatch or future edge resolves to Reject or Quarantine. Negative-control, invariance or confounding sensitivity failure downgrades the candidate to association-only or Abstain. No failure can silently widen authority. V4-17 cannot rank treatments, select treatments, allocate risk, sign promotion, compile runtime, activate runtime or send orders.

## Related

[[00_MOC_V4_17_Causal_Mechanism_Discovery|V4-17 MOC]] · [[03_Authority_And_UCEE_Boundary|Authority]] · [[24_Hidden_Confounder_Sensitivity|Confounding]] · [[31_Causal_Claim_Tiering|Claim Tiering]] · [[53_Acceptance_Criteria|Acceptance]] · [[60_V4_18_Handoff|V4-18 Handoff]]
