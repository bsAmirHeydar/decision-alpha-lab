---
title: "LCM-01 Output Manifest and Receipt"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-01]
phase_id: LCM-01
claim_ceiling: FORENSIC_SURVEY_REFERENCE_ONLY
---
# LCM-01 Output Manifest and Receipt

Every published survey artifact except the manifest itself is listed by root-relative path, size and SHA-256. The receipt binds survey summary, event ledger, provenance, handoff and process-stage execution evidence.

Verification rejects missing, extra or modified package files. Partial output is never silently accepted as a complete survey.
