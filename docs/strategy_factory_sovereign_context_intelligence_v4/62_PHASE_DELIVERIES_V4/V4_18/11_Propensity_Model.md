---
title: SAED V4-18 — Propensity Model
status: implemented-reference
version: 1.0.0
created: '2026-07-16'
updated: '2026-07-16'
capability_tier: research-reference
tags: [saed-v4, v4-18, causal-treatment, policy-value]
---
# SAED V4-18 — Propensity Model

## Purpose

Multitreatment nuisance estimation and clipping. This note is part of the closed implementation dossier for deterministic synthetic treatment-effect and policy-value research.

## Contract

The component consumes immutable, hash-verified V4-17 evidence plus the frozen V4-18 treatment, outcome, identification, estimator, policy and compute contracts. Unknown fields fail schema validation. All rows preserve chronology, cluster identity, known-time semantics, evidence role and lineage. The treatment universe contains Skip, a manual baseline and bounded synthetic candidates; it is finite, frozen and not runtime-selectable.

## Algorithm and evidence

The reference stack uses chronological cluster-aware cross-fitting, multitreatment propensity estimation, overlap and effective-sample-size diagnostics, S-learner and T-learner nuisance surfaces, orthogonal AIPW scores, heterogeneous effect summaries, direct/IPW/DR policy value, influence-function uncertainty, multiplicity-adjusted lower bounds, lower-tail value, negative controls, propensity clipping, hidden-confounder bias, cost and environment stresses. Simpler baselines remain available and every output is content-addressed.

## Failure semantics

Hash mismatch, unknown fields, future training, sibling leakage, support collapse, negative-control failure, unbounded weights, missing exposure accounting or authority escalation resolves to Skip, Abstain, Manual fallback, Reject or Quarantine. No score can override these gates.

## Authority and claim ceiling

SAED V4-18 may rank treatments and policies only inside the deterministic synthetic research scope. It cannot assert a real treatment effect, real policy value, economic uplift or alpha; select a live treatment; allocate risk; sign promotion; compile or activate runtime; access credentials; or send orders. UCEE retains every downstream authority.

## Verification

Reviewers reproduce the golden bundle, validate every closed schema, execute mutation and negative fixtures, inspect overlap and influence diagnostics, verify zero protected evidence exposure and zero hidden-evaluation queries, confirm deterministic hashes, and inspect the static MQL5 mirror. MetaEditor, real-data, protected, prospective, shadow, micro-live and live evidence remain external.

## Related

[[00_MOC_V4_18_Causal_Treatment_And_Policy_Value|V4-18 MOC]] · [[03_Authority_And_UCEE_Boundary|Authority]] · [[12_Overlap_And_Positivity|Overlap]] · [[31_Doubly_Robust_Policy_Value|Policy Value]] · [[44_Policy_Tournament|Tournament]] · [[68_V4_19_Handoff|V4-19 Handoff]]
