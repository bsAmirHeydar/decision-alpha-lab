---
title: "Rollback"
status: reference-restricted
phase_id: LCM-02
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, migration, classification]
---
# Rollback

Remove only files listed in the LCM-02 patch index or reset the phase commit. Source behavior never changed.

## Invariants

- UNKNOWN is blocking.
- Classification is not semantic approval.
- No move, delete, refactor, merge, cutover, runtime, order or capital authority is created.

## Verification

The machine package, closed registries, tests and output manifest must preserve these statements exactly.


## Related

- [[00_MOC]]
- [[LCM02_PHASE_BOUNDARY]]
- [[LCM02_TO_LCM03_HANDOFF_CONTRACT]]
