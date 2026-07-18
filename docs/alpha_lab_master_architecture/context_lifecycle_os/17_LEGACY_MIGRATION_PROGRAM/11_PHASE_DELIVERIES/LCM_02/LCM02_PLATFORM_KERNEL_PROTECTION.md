---
title: "Platform Kernel Protection"
status: reference-restricted
phase_id: LCM-02
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, migration, classification]
---
# Platform Kernel Protection

ACL-OS, Strategy Factory and LCM control-plane assets are protected from domain migration and deletion.

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
