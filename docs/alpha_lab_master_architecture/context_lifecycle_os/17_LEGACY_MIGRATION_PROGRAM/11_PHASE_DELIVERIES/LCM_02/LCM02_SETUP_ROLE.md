---
title: "Setup Role"
status: reference-restricted
phase_id: LCM-02
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, migration, classification]
---
# Setup Role

SETUP is separated from Context and Treatment. Trigger or signal tokens are evidence, not final semantic proof.

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
