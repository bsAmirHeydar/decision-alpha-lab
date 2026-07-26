---
title: "LCM-01 Python Parse-Failure Registry"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-01]
phase_id: LCM-01
claim_ceiling: FORENSIC_SURVEY_REFERENCE_ONLY
---
# LCM-01 Python Parse-Failure Registry

Syntax errors are retained as evidence rather than silently skipped. Each failure records path, reason, line and a digest of the parser message.

The reference survey reports 11 Python parse failures. A failed parse means import/capability coverage for that file is incomplete and therefore UNKNOWN.
