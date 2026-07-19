---
title: "LCM-08A — 04 Input Artifact Matrix"
status: implemented-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, lcm-08a, context-portfolio]
phase_id: LCM-08A
---
# LCM-08A — 04 Input Artifact Matrix

## Purpose

LCM-01 through LCM-07 input registries and their role in portfolio reconstruction.

## Binding rules

- The authoritative input is the exact LCM-07 handoff and the accepted LCM-01 through LCM-07 registries.
- Missing evidence is recorded as `UNKNOWN`; it is never inferred from names, paths, comments or apparent similarity.
- Risk dimensions remain individually visible. A critical dimension cannot be neutralized by a low aggregate score.
- This phase does not move, delete, rewrite, instrument, adapt or switch any legacy consumer.
- No runtime, live-order or capital authority is created.

## Verification obligation

The machine package must bind this rule to deterministic records, stable identities, SHA-256 digests, hostile review and clean-overlay verification. A partial build or unverified artifact is not a release.

## Downstream effect

Only the selected pilot may enter LCM-08B. All other Context candidates remain frozen in their assigned wave or unresolved state.
