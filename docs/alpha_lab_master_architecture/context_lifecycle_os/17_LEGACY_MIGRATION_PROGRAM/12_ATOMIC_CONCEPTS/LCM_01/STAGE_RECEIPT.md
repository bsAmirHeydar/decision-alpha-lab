---
title: "Stage Receipt"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-01, atomic-concept]
phase_id: LCM-01
claim_ceiling: FORENSIC_SURVEY_REFERENCE_ONLY
---
# Stage Receipt

## Definition

A digest-bound statement of one worker stage outputs and metrics.

## Invariants

Its output hashes and authority denials must verify before finalization.

## Evidence and use

Prevents partial-stage silence.

## Related

[[LCM01_STAGE_RECEIPT_MODEL]]
