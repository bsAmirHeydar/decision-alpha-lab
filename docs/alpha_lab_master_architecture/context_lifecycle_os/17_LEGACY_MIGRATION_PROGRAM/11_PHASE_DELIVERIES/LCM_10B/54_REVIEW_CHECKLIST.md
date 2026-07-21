---
title: "LCM-10B — Review Checklist"
status: accepted-reference
version: 1.0.0
updated: 2026-07-20
tags: [acl-os, lcm, lcm-10b]
---
# Review Checklist

## Contract

Confirm digest binding, exact accounting, false authority, side-aware semantics, no implicit market, no source changes and bounded handoff.

## Engineering invariants

- Claim ceiling remains `LCM_10B_REFERENCE_ONLY`.
- Submission, live, paper, runtime and capital authority remain false.
- Missing evidence is represented as `UNKNOWN` or an explicit blocker.
- Legacy source behavior is unchanged.
- Generated machine artifacts are immutable projections of source-bound evidence.

## Verification

This dimension is included in the LCM-10B non-compensatory QA and handoff review. A failed mandatory check blocks publication.
