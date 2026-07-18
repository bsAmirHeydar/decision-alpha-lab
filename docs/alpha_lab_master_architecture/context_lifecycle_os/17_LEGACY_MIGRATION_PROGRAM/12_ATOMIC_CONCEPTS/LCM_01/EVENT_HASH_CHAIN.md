---
title: "Event Hash Chain"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-01, atomic-concept]
phase_id: LCM-01
claim_ceiling: FORENSIC_SURVEY_REFERENCE_ONLY
---
# Event Hash Chain

## Definition

The sequence of survey lifecycle events linked by previous-event digest.

## Invariants

Reordering or payload mutation invalidates verification.

## Evidence and use

Provides ordered audit evidence.

## Related

[[LCM01_EVENT_LEDGER]]
