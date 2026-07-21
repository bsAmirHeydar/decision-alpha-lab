---
status: accepted-reference
version: 1.0.0
updated: 2026-07-20
tags: [acl-os, lcm, lcm-09b, setup-migration]
phase_id: LCM-09B
claim_ceiling: LCM_09B_REFERENCE_ONLY
---
# Owner Resolution Workbook

This workbook defines the evidence required to move any Setup identity from `REFERENCE_BLOCKED` to a future `REFERENCE_READY` amendment. It does not authorize that change in this patch.

## Per-identity required evidence

1. named semantic owner and reviewer;
2. source digest re-verification;
3. observed characterization packet with creation, suppression, no-trade, confirmation, invalidation, cancellation, expiry, and restart cases where applicable;
4. exact definitions for all mandatory lifecycle rules;
5. canonical Context identity/version and known-time contract;
6. duplicate/non-equivalence decision against family siblings;
7. canonical Treatment identity or approved pending dependency;
8. legacy and canonical golden traces generated independently;
9. zero unresolved hard mismatch or explicit blocking decision;
10. versioned owner approval and amendment handoff.

## Prohibited shortcuts

- static token counts as behavioral proof;
- family label as equivalence proof;
- profitability as rule correctness evidence;
- aggregate parity percentage as waiver;
- manual prose edits to generated package JSON;
- enabling Factory promotion or runtime flags;
- importing Treatment or broker code into Setup core.

## Amendment procedure

A future amendment must update only approved identities, regenerate the complete package deterministically, preserve historical blockers/events, publish new package versions and digests, rerun all direct/Factory tests, and issue a new handoff. Existing package digests remain immutable historical evidence.
