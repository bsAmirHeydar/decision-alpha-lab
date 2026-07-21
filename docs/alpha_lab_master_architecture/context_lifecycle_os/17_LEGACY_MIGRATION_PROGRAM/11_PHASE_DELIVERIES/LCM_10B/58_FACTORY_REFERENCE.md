---
title: "LCM-10B — Setup Factory Reference Bridge"
status: accepted-reference
version: 1.0.0
updated: 2026-07-20
tags: [acl-os, lcm, lcm-10b]
---
# Setup Factory Reference Bridge

## Contract

ACL-04 exposes a read-only resolver for Setup-to-Treatment references; it cannot execute or activate an adapter.

## Engineering invariants

- Claim ceiling remains `LCM_10B_REFERENCE_ONLY`.
- Submission, live, paper, runtime and capital authority remain false.
- Missing evidence is represented as `UNKNOWN` or an explicit blocker.
- Legacy source behavior is unchanged.
- Generated machine artifacts are immutable projections of source-bound evidence.

## Verification

This dimension is included in the LCM-10B non-compensatory QA and handoff review. A failed mandatory check blocks publication.
