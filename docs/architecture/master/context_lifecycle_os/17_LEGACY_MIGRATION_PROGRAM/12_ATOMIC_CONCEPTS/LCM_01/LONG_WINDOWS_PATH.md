---
title: "Long Windows Path Risk"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-01, atomic-concept]
phase_id: LCM-01
claim_ceiling: FORENSIC_SURVEY_REFERENCE_ONLY
---
# Long Windows Path Risk

## Definition

A root-relative path exceeding the frozen survey threshold.

## Invariants

The threshold does not include every possible checkout prefix.

## Evidence and use

Feeds path-shortening decisions without authorizing rename.

## Related

[[LCM01_WINDOWS_PATH_RISK_SURVEY]]
