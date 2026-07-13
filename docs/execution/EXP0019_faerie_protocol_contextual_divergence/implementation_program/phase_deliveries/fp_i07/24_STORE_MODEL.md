---
title: "FP-I07 — Indexed pending/result/signal/event stores"
tags: [exp0019, faerie-protocol, fp-i07, confirmation, obsidian]
status: implemented
phase: FP-I07
version: 1.0.0
last_updated: 2026-07-13
language: en
---
# Indexed pending/result/signal/event stores

## Purpose

Indexed pending/result/signal/event stores. This note is normative for FP-I07 and is implemented by the Python package `fp_i07_confirmation`, the MQL5 mirror under `I07`, the closed JSON schemas, and the phase tests.

## Frozen invariants

- M1 facts and Hunter/Protected roles come unchanged from FP-I06.
- The host timeframe is resolved once at initialization and is identity-bearing.
- Only the first eligible fully closed host bar can finalize a candidate.
- The confirmation close must be strictly earlier than the owning A/L/N session end.
- Causal source evidence must be complete through the target close.
- Every candidate produces at most one terminal result.
- A confirmed signal is immutable evidence; later revisions do not retract it.
- FP-I07 has no WW, quota, drawing, order, broker, position, or network authority.

## Deterministic implementation

The phase uses immutable contracts, canonical serialization, SHA-256 semantic identities, a closed outcome registry, an append-only lifecycle event, indexed pending/result stores, and fail-closed handling for missing bars, missing M1 coverage, missed close processing, illegal transitions, and checkpoint mismatch.

## Evidence

- `FP_I07_CONTRACT_REGISTRY.v1.json`
- `FP_I07_CONFIRMATION_REASON_REGISTRY.v1.json`
- `FP_I07_GOLDEN_CONFIRMATION_VECTORS.v1.json`
- `FP_I07_ACCEPTANCE_EVIDENCE.json`
- `EXP0019_FP_I07_QA_REPORT.json`

## Navigation

- [[00_FP_I07_DELIVERY_MOC|FP-I07 Delivery MOC]]
- [[../../phases/FP_I07_HOST-CANDLE_CONFIRMATION_STRICT_SESSION_DEADLINE_INVALIDATION_AND_LIFECYCLE|Program Phase Specification]]
- [[../fp_i06/40_HANDOFF_TO_FP_I07|FP-I06 Handoff]]
