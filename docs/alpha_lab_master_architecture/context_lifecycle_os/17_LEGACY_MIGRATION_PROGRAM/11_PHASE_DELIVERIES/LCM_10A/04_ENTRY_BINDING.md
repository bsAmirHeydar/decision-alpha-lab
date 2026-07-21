---
title: "LCM-10A — Entry Binding"
status: accepted-reference
version: 1.0.0
updated: 2026-07-20
phase_id: LCM-10A
claim_ceiling: LCM_10A_REFERENCE_ONLY
---
# Entry Binding

## Purpose

The exact LCM-09B handoff is bound with LCM-01, LCM-02 and LCM-07 manifests.

## Engineering contract

The build fails closed if the handoff digest or the 60 Setup dependency seed count changes.

## Non-compensatory boundary

This artifact creates no promotion, runtime, live-order or capital authority. Missing evidence remains UNKNOWN, all legacy source bytes remain unchanged, and downstream use is restricted by the digest-bound LCM-10A handoff.
