---
title: "LCM-10A — Rollback Contract"
status: accepted-reference
version: 1.0.0
updated: 2026-07-20
phase_id: LCM-10A
claim_ceiling: LCM_10A_REFERENCE_ONLY
---
# Rollback Contract

## Purpose

Rollback removes only paths in the exact patch index and restores the LCM-09B accepted state.

## Engineering contract

Because no legacy source changes, rollback does not require behavioral reconstruction.

## Non-compensatory boundary

This artifact creates no promotion, runtime, live-order or capital authority. Missing evidence remains UNKNOWN, all legacy source bytes remain unchanged, and downstream use is restricted by the digest-bound LCM-10A handoff.
