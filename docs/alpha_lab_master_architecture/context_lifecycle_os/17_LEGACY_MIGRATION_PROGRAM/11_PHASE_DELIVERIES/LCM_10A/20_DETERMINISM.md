---
title: "LCM-10A — Determinism and Identity"
status: accepted-reference
version: 1.0.0
updated: 2026-07-20
phase_id: LCM-10A
claim_ceiling: LCM_10A_REFERENCE_ONLY
---
# Determinism and Identity

## Purpose

Canonical JSON ordering, stable IDs, source hashes and self-excluding digests make rebuilds byte deterministic.

## Engineering contract

Wall-clock time is never an identity input.

## Non-compensatory boundary

This artifact creates no promotion, runtime, live-order or capital authority. Missing evidence remains UNKNOWN, all legacy source bytes remain unchanged, and downstream use is restricted by the digest-bound LCM-10A handoff.
