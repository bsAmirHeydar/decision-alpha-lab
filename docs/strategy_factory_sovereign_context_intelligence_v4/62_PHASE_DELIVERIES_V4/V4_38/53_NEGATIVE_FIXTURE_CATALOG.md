---
title: SAED V4-38 53 Negative Fixture Catalog
status: accepted-reference
phase: SAED_V4_38
tags: [saed-v4, v4-38, immutable-runtime, research-only]
---
# SAED V4-38 — 53 Negative Fixture Catalog

## Purpose

This note defines the **research-only** V4-38 contract for 53 negative fixture catalog. The design is additive, immutable, deterministic, closed-schema and fail-closed. It cannot grant order, capital, production or live-trading authority.

## Contract

- Every material input is content-addressed and bound into the immutable runtime bundle.
- Unknown fields, missing required fields, future-known inputs and silent coercions are rejected.
- Python reference evidence, MQL5 static evidence, MetaEditor compilation evidence and terminal replay evidence remain distinct.
- A synthetic emulator pass is never promoted into an actual MetaEditor or terminal parity claim.
- Any mismatch preserves the baseline, emits abstention and requires independent escalation.

## Required evidence

1. Closed schema and golden example.
2. Deterministic replay and mutation resistance.
3. Hash, manifest and lineage receipt.
4. Explicit authority boundary.
5. External-evidence status when the claim depends on Windows, MetaEditor or MT5 Terminal.

## Acceptance

Acceptance in SAED V4-38 means the immutable reference implementation is internally reproducible. Production authorization remains false until actual external qualification is attached and the later deployment phases approve activation.
