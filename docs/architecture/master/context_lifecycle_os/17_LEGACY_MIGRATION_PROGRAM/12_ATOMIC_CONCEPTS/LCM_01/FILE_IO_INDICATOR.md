---
title: "File-I/O Indicator"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-01, atomic-concept]
phase_id: LCM-01
claim_ceiling: FORENSIC_SURVEY_REFERENCE_ONLY
---
# File-I/O Indicator

## Definition

A static reference to file read/write/open/close or related operations.

## Invariants

No file is opened by the scanner as executable behavior.

## Evidence and use

Feeds persistence and path migration review.

## Related

[[LCM01_PERSISTENCE_AND_FILE_IO_SURFACE]]
