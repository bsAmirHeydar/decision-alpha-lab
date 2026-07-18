---
title: "LCM-01 Failure Taxonomy"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-01]
phase_id: LCM-01
claim_ceiling: FORENSIC_SURVEY_REFERENCE_ONLY
---
# LCM-01 Failure Taxonomy

Hard failures include baseline hash mismatch, missing baseline path, invalid handoff, authority escalation, unsafe path, stage receipt mismatch, output mutation, duplicate inventory path, incomplete baseline coverage, event-chain failure, provenance mismatch and non-empty destination.

Soft/static limitations are represented as UNKNOWN only when the package can still be complete within the claim ceiling. A hard failure discards staging output.
