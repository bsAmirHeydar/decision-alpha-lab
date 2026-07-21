---
title: "LCM-10B — Handoff"
status: accepted-reference
version: 1.0.0
updated: 2026-07-20
tags: [acl-os, lcm, lcm-10b]
---
# Handoff

## Contract

The handoff authorizes LCM-10C dry-run parity, safety controls, negative authority tests and forbidden API rescans only.

## Engineering invariants

- Claim ceiling remains `LCM_10B_REFERENCE_ONLY`.
- Submission, live, paper, runtime and capital authority remain false.
- Missing evidence is represented as `UNKNOWN` or an explicit blocker.
- Legacy source behavior is unchanged.
- Generated machine artifacts are immutable projections of source-bound evidence.

## Verification

This dimension is included in the LCM-10B non-compensatory QA and handoff review. A failed mandatory check blocks publication.
