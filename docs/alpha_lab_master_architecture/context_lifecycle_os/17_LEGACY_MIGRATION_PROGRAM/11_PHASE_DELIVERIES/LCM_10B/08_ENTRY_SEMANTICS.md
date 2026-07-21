---
title: "LCM-10B — Entry Semantics"
status: accepted-reference
version: 1.0.0
updated: 2026-07-20
tags: [acl-os, lcm, lcm-10b]
---
# Entry Semantics

## Contract

Market, limit, stop and stop-limit are distinct. Missing entry kind is blocking and never defaults to market.

## Engineering invariants

- Claim ceiling remains `LCM_10B_REFERENCE_ONLY`.
- Submission, live, paper, runtime and capital authority remain false.
- Missing evidence is represented as `UNKNOWN` or an explicit blocker.
- Legacy source behavior is unchanged.
- Generated machine artifacts are immutable projections of source-bound evidence.

## Verification

This dimension is included in the LCM-10B non-compensatory QA and handoff review. A failed mandatory check blocks publication.
