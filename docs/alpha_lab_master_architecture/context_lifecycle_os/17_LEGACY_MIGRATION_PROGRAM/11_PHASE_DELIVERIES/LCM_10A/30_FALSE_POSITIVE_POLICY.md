---
title: "LCM-10A — False-Positive Policy"
status: accepted-reference
version: 1.0.0
updated: 2026-07-20
phase_id: LCM-10A
claim_ceiling: LCM_10A_REFERENCE_ONLY
---
# False-Positive Policy

## Purpose

Static matches may over-report, but evidence is never silently discarded.

## Engineering contract

Ambiguous matches are retained as reference evidence or UNKNOWN for owner review.

## Non-compensatory boundary

This artifact creates no promotion, runtime, live-order or capital authority. Missing evidence remains UNKNOWN, all legacy source bytes remain unchanged, and downstream use is restricted by the digest-bound LCM-10A handoff.
