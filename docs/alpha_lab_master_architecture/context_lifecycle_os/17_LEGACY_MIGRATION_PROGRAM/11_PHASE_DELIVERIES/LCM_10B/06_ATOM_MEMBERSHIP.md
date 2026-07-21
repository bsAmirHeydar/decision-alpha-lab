---
title: "LCM-10B — Treatment Atom Membership"
status: accepted-reference
version: 1.0.0
updated: 2026-07-20
tags: [acl-os, lcm, lcm-10b]
---
# Treatment Atom Membership

## Contract

All 1,109 observed atoms are assigned exactly once to 422 source-bound packages. Membership preserves original atom digests.

## Engineering invariants

- Claim ceiling remains `LCM_10B_REFERENCE_ONLY`.
- Submission, live, paper, runtime and capital authority remain false.
- Missing evidence is represented as `UNKNOWN` or an explicit blocker.
- Legacy source behavior is unchanged.
- Generated machine artifacts are immutable projections of source-bound evidence.

## Verification

This dimension is included in the LCM-10B non-compensatory QA and handoff review. A failed mandatory check blocks publication.
