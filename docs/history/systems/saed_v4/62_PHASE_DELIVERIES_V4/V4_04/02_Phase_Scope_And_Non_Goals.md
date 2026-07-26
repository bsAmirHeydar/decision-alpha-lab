---
title: Phase Scope and Non-Goals
status: implemented
version: 1.0.0
phase: V4-04
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production-context-plane
tags: [saed-v4, v4-04, multimodal-view-platform]
---
# Phase Scope and Non-Goals

## Purpose

Exact capability boundary and prohibited claims.

## Navigation

- Previous: [[01_Executive_Intent]]
- Phase home: [[00_MOC_V4_04_Multimodal_View_Platform]]
- Next: [[03_Reference_Architecture]]

## Institutional invariant

A V4-04 View is a deterministic, exact-version and point-in-time-correct representation of approved source truth. It may summarize or transform visible evidence, but it cannot create canonical truth, silently invent missing data, fit adaptive statistics, train a model, select a Treatment, allocate risk, activate runtime or send an order.

## Canonical inputs

```text
Exact Twin Manifest or Snapshot
+ exact Event-State Projection
+ exact static metadata
+ optional read-only execution economics
+ optional externally approved Treatment descriptor
+ known_as_of
+ event_as_of
+ Evidence Role
```

All inputs are hash-bound and role-bound. Sources outside the temporal boundary or Evidence Role are unavailable rather than coerced into the View.

## Canonical outputs

```text
View Specification
→ Feature Values
→ Missingness Mask
→ Freshness State
→ Quality State
→ Support Assessment
→ Lineage Root
→ Immutable View Hash
```

When multiple Views are assembled, the package additionally carries cross-view compatibility, required-view completeness, package-level missingness and quality vectors, an aggregate lineage root and an integrity receipt.

## Failure posture

The implementation fails closed for forbidden authority, exact-version rebind, temporal leakage, cross-role source mixing, source conflicts, prohibited missing values, invalid static normalization, type mismatch, category mismatch, vector mismatch, unsupported required features, incompatible temporal boundaries and replay or integrity mismatch.

## Design details

1. **Truth separation.** UCEE and the Context Twin remain authorities for canonical Context truth. V4-04 produces derived representations only.
2. **View separation.** Price, structure, time, higher-timeframe, intermarket, liquidity, session, execution, ancestry and Treatment descriptors remain independently versioned.
3. **Missingness visibility.** Every feature carries a mask, missing flag, stale flag, quality score, source keys, source hashes and reason codes.
4. **Static normalization only.** Any normalization statistics must be frozen, exact-version and backed by an artifact hash. Adaptive fitting belongs to later training phases.
5. **No learned fusion.** The multimodal package aligns Views and emits vectors; V4-04 does not learn cross-view attention, embeddings or gates.
6. **No Treatment authority.** The Treatment Descriptor View can represent a descriptor already approved by another authority. It cannot generate or rank candidates.
7. **Reproducibility.** Identical source truth and boundaries produce the same View and package hashes regardless of input ordering or operational request ID.

## Operational evidence

Required evidence includes closed-schema validation, exact-version registry tests, point-in-time tests, Evidence Role isolation, missingness tests, no-forward-fill tests, normalization tests, transform tests, support tests, package compatibility, replay, integrity, semantic diff, MQL5 static checks, Obsidian link validation and clean-baseline patch verification.

## Claims not made

This phase does not claim a learned representation, alpha, causal effect, Treatment value, runtime parity, MetaEditor compile, production authorization or live execution. It creates the governed input plane required by V4-05 and later learning phases.
