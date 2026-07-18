---
title: "Root-Relative Path"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-01, atomic-concept]
phase_id: LCM-01
claim_ceiling: FORENSIC_SURVEY_REFERENCE_ONLY
---
# Root-Relative Path

## Definition

A repository path expressed from the repository root with forward slashes.

## Invariants

No host prefix, drive letter or traversal above root is allowed.

## Evidence and use

Primary path identity in all LCM-01 outputs.

## Related

[[LCM01_PATH_CANONICALIZATION]]
