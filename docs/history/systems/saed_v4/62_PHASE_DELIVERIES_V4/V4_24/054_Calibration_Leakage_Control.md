---
title: SAED V4-24 — Calibration Leakage Control
status: accepted-reference
version: 1.0.0
phase: SAED_V4_24
evidence_scope: local-deterministic-calibration-selective-control-reference
claim_ceiling: research-only-no-production-authority
tags: [saed-v4, v4-24, conformal, ood, selective-control]
---
# SAED V4-24 — Calibration Leakage Control

## Purpose
**Calibration Leakage Control** is a normative element of the V4-24 Conformal OOD and Selective Control phase. It makes calibration uncertainty and selective-control governance explicit, versioned, content-addressed and independently reproducible above the immutable V4-23 offline-policy research handoff. It does not create a production decision right or alter UCEE authority.

## Contract
Inputs are exact-versioned and closed to unknown fields. Every research record carries stable identity, cluster, regime, role, decision time, feature-known time, outcome-observed time, frozen feature vector, policy identity, action mask, behavior probability, candidate probability, support score, predicted value and retrospective outcome. Missing lineage, future-suffix access, protected evidence, non-finite numerics, invalid probability domains, cluster-role leakage or authority-bearing flags reject the artifact.

## Engineering implementation
The Python reference is deterministic and standard-library bounded. Canonical JSON and SHA-256 identities bind configuration, calibration data, conformal quantiles, OOD statistics, selective decisions, coverage-risk frontiers, abstention policy, drift report, ledgers, certificate and handoff. Stable sorting and explicit tie-breaking prevent platform-dependent decisions. Every fit, evaluation, frontier point and bootstrap draw consumes an approved research budget.

## Scientific implementation
One-sided split conformal calibration converts downside residuals into finite-sample lower value bounds. Mondrian regime groups are used only when their minimum sample gate is satisfied; otherwise pooled calibration is used. OOD combines robust MAD-scaled deviation, local nearest-neighbor distance and support deficit, then assigns an empirical p-value. Selective control accepts a candidate only when action-mask, conformal lower-bound, OOD, support and missingness gates pass. Realized outcomes are excluded from decision artifacts and used only for retrospective coverage-risk evidence.

## Failure semantics
Every failure is fail-closed. A failed or absent gate selects `skip` and records a machine-readable reason. Undercoverage, exchangeability breakdown, low support, excessive missingness, OOD detection, drift breach, budget exhaustion, schema mismatch, hash mismatch or replay mismatch blocks the research candidate. Local waivers cannot create promotion, runtime compilation, capital allocation, order submission or online mutation authority.

## Verification evidence
Verification requires positive, negative and mutation tests, closed-schema validation, exact golden replay, future-outcome mutation invariance, zero hidden-evaluation queries, zero protected-evidence exposure, complete trial/exposure/budget ledgers, model-risk review, security review and static MQL5 boundary checks. MetaEditor compilation remains `pending_local_windows`; runtime parity, prospective coverage and broker qualification are not claimed.

## Traceability
Parent phase: [[V4_23_Offline_Policy_Research]]. Current map: [[00_MOC_V4_24_Conformal_OOD_And_Selective_Control]]. Next concept: [[Outcome_Mutation_Invariance]]. Next phase: [[V4_25_Continual_Meta_And_Transfer]]. Sequence: 054/180.
