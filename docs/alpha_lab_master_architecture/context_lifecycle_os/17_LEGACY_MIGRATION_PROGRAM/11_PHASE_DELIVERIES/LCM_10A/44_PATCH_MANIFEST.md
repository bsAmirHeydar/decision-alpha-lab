---
title: "LCM-10A — Patch Manifest Contract"
status: accepted-reference
version: 1.0.0
updated: 2026-07-20
phase_id: LCM-10A
claim_ceiling: LCM_10A_REFERENCE_ONLY
---
# Patch Manifest Contract

## Purpose

The root patch manifest binds every changed path, byte count and SHA-256.

## Engineering contract

The file index is the only staging authority for the release.

## Non-compensatory boundary

This artifact creates no promotion, runtime, live-order or capital authority. Missing evidence remains UNKNOWN, all legacy source bytes remain unchanged, and downstream use is restricted by the digest-bound LCM-10A handoff.
