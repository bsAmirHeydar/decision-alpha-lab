---
title: "Survey Replay"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-01, atomic-concept]
phase_id: LCM-01
claim_ceiling: FORENSIC_SURVEY_REFERENCE_ONLY
---
# Survey Replay

## Definition

A complete rebuild of the survey in a fresh destination.

## Invariants

Survey ID and summary digest must match under the same baseline/config/scanner version.

## Evidence and use

Primary deterministic QA check.

## Related

[[LCM01_REPRODUCIBILITY_CONTRACT]]
