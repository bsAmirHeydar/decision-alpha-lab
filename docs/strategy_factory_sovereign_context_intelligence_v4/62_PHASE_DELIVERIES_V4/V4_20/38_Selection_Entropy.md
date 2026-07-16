---
title: SAED V4-20 — Selection Entropy
status: implemented-reference
version: 1.0.0
created: '2026-07-16'
updated: '2026-07-16'
capability_tier: research-reference
tags: [saed-v4, v4-20, decision-focused, treatment-selection]
---
# SAED V4-20 — Selection Entropy

## Purpose

This note defines **Selection Entropy** inside the closed V4-20 decision-focused treatment-selection boundary. The phase converts frozen synthetic treatment evidence into an auditable, deterministic and non-executable research selection artifact. It does not convert a model score into live trading authority.

## Contract

Every input is content-addressed and bound to immutable V4-18 policy-value evidence, immutable V4-19 proof envelopes, a finite treatment universe, known-time context state, explicit support and overlap measurements, frozen utility weights, hard constraints, risk settings, a calibration rule and an exposure budget. Unknown fields, unknown treatments, future-known information, protected evidence, dynamic universe expansion and authority escalation fail closed.

## Engineering behavior

The reference implementation validates treatment admissibility, applies proof and support masks, computes reward after cost, tail, drawdown, turnover and complexity penalties, builds scenario regret, forms a Pareto frontier, ranks candidates with deterministic ties, calibrates reference selection probabilities, constructs a bounded set-valued choice and abstains to Skip when proof, support, margin, entropy or baseline non-inferiority requirements fail. The resulting certificate carries the complete ranking, action mask, upstream hashes, fallback reason and explicit authority denials.

## Failure semantics and evidence

A hard-constraint failure removes the candidate. An empty admissible set exposes only the canonical Skip treatment. A narrow objective margin, excessive entropy, proof mismatch, support failure or baseline non-inferiority failure produces explicit abstention. Acceptance is limited to deterministic synthetic evidence: closed schemas, golden replay, negative and mutation fixtures, complete exposure accounting, baseline preservation and static MQL5 conformance. Real policy value, alpha, runtime parity, production authorization and live readiness remain unclaimed.

## Related

[[00_MOC_V4_20_Decision_Focused_Treatment_Selection|V4-20 MOC]] · [[07_Decision_Problem_Contract|Decision Contract]] · [[20_Action_Mask_Compiler|Action Mask]] · [[30_Pareto_Frontier_Construction|Pareto]] · [[35_Set_Valued_Treatment_Selection|Set-Valued]] · [[45_Selection_Certificate|Certificate]] · [[86_V4_21_Handoff|V4-21 Handoff]]
