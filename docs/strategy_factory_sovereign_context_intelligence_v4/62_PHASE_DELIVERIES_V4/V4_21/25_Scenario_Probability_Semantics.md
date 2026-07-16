---
title: "V4-21 — Scenario Probability Semantics"
status: implemented-reference
version: 1.0.0
phase: SAED_V4_21
evidence_class: local-deterministic-synthetic-reference
authority_class: research-only-nonproduction
tags: [saed-v4, robust-optimization, regret, governance]
---
# V4-21 — Scenario Probability Semantics

## Purpose
This note specifies **Scenario Probability Semantics** as a closed-contract component of the V4-21 robust-optimization and regret-analysis reference implementation. The component is deterministic, content-addressed, independently reproducible, and bounded by explicit compute and evidence budgets.

## Contract
Inputs must be known-time safe, hash-bound to immutable V4-20 artifacts, free of protected final evidence, and valid under closed schemas with zero unknown fields. Outputs must preserve canonical identifiers, complete provenance, budget accounting, baseline visibility, and explicit failure reasons.

## Engineering invariants
- No future suffix may influence scenario construction, ambiguity calibration, allocation enumeration, objective scoring, regret computation, or certificate generation.
- The manual baseline and `SKIP` remain present and evaluable in every allocation universe.
- Ambiguity radius, objective, regret limits, and baseline thresholds are frozen before evaluation.
- Every bounded search step is counted; hidden evaluation queries and protected-evidence exposures remain exactly zero.
- Any contract, support, budget, integrity, or authority failure is fail-closed.

## Failure behavior
The component rejects unknown fields, mismatched upstream hashes, non-finite values, unbounded search, data-dependent ambiguity tuning, runtime-executable flags, and authority escalation. When no robust allocation remains or robust separation is insufficient, the output abstains and resolves to the canonical skip allocation.

## Evidence and non-claims
Evidence is local, deterministic, and synthetic. It does not establish real policy value, real alpha, live treatment selection, live risk allocation, runtime parity, MetaEditor compilation, broker behavior, prospective performance, production authorization, or execution authority.

## Relationship
[[24_Scenario_Identity_and_Hashing|Previous: Scenario Identity and Hashing]] · [[26_Ambiguity_Set_Contract|Next: Ambiguity Set Contract]]
