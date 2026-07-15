---
title: SAED V4-10 Atomic — Known-Time Predicate
status: implemented-reference
version: 1.0.0
created: '2026-07-15'
updated: '2026-07-15'
tags:
  - saed-v4
  - v4-10
  - atomic-concept
---

# SAED V4-10 Atomic — Known-Time Predicate

## Definition

A predicate over a feature whose event and availability times are at or before the decision boundary.

## Invariant

The concept is deterministic, versioned, closed-contract and non-authoritative. It cannot silently acquire model-training, treatment-ranking, capital-allocation, runtime-activation or order-sending capability.

## Failure mode

Unknown identity, time ambiguity, missing lineage, outcome leakage, semantic drift or authority escalation causes immediate rejection and blocks downstream handoff.

## Evidence

Evidence is limited to reference implementation, closed-schema validation, deterministic replay and static MQL5 conformance unless an external receipt is explicitly attached.
