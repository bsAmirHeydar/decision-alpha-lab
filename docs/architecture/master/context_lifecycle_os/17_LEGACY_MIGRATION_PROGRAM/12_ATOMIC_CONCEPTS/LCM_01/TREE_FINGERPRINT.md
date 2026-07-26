---
title: "Documentation Tree Fingerprint"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-01, atomic-concept]
phase_id: LCM-01
claim_ceiling: FORENSIC_SURVEY_REFERENCE_ONLY
---
# Documentation Tree Fingerprint

## Definition

A digest of sorted relative-path and file-hash pairs within a namespace.

## Invariants

It is sensitive to path set and bytes, not semantic meaning.

## Evidence and use

Used to detect exact duplicate trees.

## Related

[[LCM01_EXACT_DUPLICATE_TREE_POLICY]]
