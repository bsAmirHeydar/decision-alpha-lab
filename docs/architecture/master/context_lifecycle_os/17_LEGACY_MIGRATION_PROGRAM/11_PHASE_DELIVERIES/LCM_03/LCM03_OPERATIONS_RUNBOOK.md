---
title: "Lcm03 Operations Runbook"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-03, identity, alias, locator]
phase_id: LCM-03
claim_ceiling: IDENTITY_AND_LOCATOR_REFERENCE_ONLY
---
# Lcm03 Operations Runbook

Provides build, verify, replay and failure handling procedures.

## Invariants

- A path, filename, experiment code or symbol name is an alias, not permanent domain truth.
- Ambiguity and collision block resolution; they are not resolved by naming convention.
- Registration does not move, delete, merge, refactor, cut over or authorize execution.
- Provisional identity is not human semantic approval.

## Verification

The machine package binds this contract through versioned registries, content digests, consumer census, collision reports, event ledger, provenance and the LCM-04 handoff.

## Related

- [[LCM_03_CANONICAL_IDENTITY_ALIAS_AND_LOCATOR]]
- [[LCM03_TO_LCM04_HANDOFF_CONTRACT]]
