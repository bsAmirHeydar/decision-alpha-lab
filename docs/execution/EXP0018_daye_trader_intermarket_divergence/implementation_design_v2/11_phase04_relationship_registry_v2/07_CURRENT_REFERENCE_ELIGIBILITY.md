---
id: EXP0018-P04-ELIGIBILITY
title: "P04 Current and Reference Eligibility"
type: invariant-contract
status: active
project: EXP0018
phase: P04
---
# Eligibility

Default current eligibility:

- COMPLETE: allowed;
- OPEN: allowed;
- PARTIAL: rejected;
- EMPTY, UNAVAILABLE, INVALID: rejected.

Default reference eligibility:

- COMPLETE only.

This asymmetry is intentional. Hunt observation occurs inside an open current period, while the reference must be historically closed and exact. Configuration may widen current eligibility for research, but must not silently widen reference eligibility.
