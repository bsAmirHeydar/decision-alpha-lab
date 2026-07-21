---
title: "LCM-10A — Deterministic Rebuild"
status: accepted-reference
version: 1.0.0
updated: 2026-07-20
phase_id: LCM-10A
claim_ceiling: LCM_10A_REFERENCE_ONLY
---
# Deterministic Rebuild

## Purpose

Rebuilding the package from the same source tree must reproduce identical bytes.

## Engineering contract

Any difference blocks publication and requires root-cause analysis.

## Non-compensatory boundary

This artifact creates no promotion, runtime, live-order or capital authority. Missing evidence remains UNKNOWN, all legacy source bytes remain unchanged, and downstream use is restricted by the digest-bound LCM-10A handoff.
