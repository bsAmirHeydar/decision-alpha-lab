---
title: "LCM-01 Path Canonicalization"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-01]
phase_id: LCM-01
claim_ceiling: FORENSIC_SURVEY_REFERENCE_ONLY
---
# LCM-01 Path Canonicalization

Paths are represented with forward slashes and are interpreted relative to the repository root. Absolute paths, empty paths and paths escaping above the root are not canonical survey identities.

Case-preserving path and case-folded path are both recorded. The former preserves repository identity; the latter supports Windows collision analysis without renaming any source.
