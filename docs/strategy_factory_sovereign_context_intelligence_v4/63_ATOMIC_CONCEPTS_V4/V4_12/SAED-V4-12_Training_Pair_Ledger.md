---
title: SAED V4-12 — Training Pair Ledger
status: canonical-atomic
version: 1.0.0
created: '2026-07-15'
updated: '2026-07-15'
phase: SAED_V4_12
tags: [saed-v4, v4-12, atomic-contract]
---

# SAED V4-12 — Training Pair Ledger

## Definition

Every input-target exposure is immutable and hash-bound.

## Invariant

The invariant is evaluated against exact upstream hashes, known-time sequence ordering, deterministic candidate identity and the research-only authority boundary. A missing, ambiguous or corrupted value fails closed.

## Negative test

The hostile test mutates the relevant hash, time, token, state, budget or authority field and requires deterministic rejection or quarantine. Silent fallback, implicit coercion and inferred authority are prohibited.

## Evidence

Evidence is provided by the V4-12 Python test suite, closed JSON schemas, golden artifact bundle, delivery hash ledger and static MQL5 mirror where applicable.

## Authority Boundary

This atomic contract cannot grant treatment ranking, treatment selection, risk allocation, runtime activation, order submission, promotion signature or production authorization.
