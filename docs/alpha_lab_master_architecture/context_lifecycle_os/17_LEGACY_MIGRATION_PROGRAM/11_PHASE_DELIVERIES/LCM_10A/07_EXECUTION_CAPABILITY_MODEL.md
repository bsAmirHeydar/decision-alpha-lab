---
title: "LCM-10A — Execution Capability Model"
status: accepted-reference
version: 1.0.0
updated: 2026-07-20
phase_id: LCM-10A
claim_ceiling: LCM_10A_REFERENCE_ONLY
---
# Execution Capability Model

## Purpose

Capabilities represent request construction, submission, modification, cancellation, close, reconciliation, broker reads, ledger and network surfaces.

## Engineering contract

Each capability records authority class, severity, mode evidence, owner evidence, source location and an explicit false authority boundary.

## Non-compensatory boundary

This artifact creates no promotion, runtime, live-order or capital authority. Missing evidence remains UNKNOWN, all legacy source bytes remain unchanged, and downstream use is restricted by the digest-bound LCM-10A handoff.
