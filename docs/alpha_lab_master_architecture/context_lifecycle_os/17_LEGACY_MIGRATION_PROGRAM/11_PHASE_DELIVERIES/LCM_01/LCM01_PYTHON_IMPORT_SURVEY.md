---
title: "LCM-01 Python Import Survey"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-01]
phase_id: LCM-01
claim_ceiling: FORENSIC_SURVEY_REFERENCE_ONLY
---
# LCM-01 Python Import Survey

Python source is parsed with the standard AST. `import` and `from ... import ...` edges are indexed, relative imports are resolved when possible, command/test entry candidates are recorded, and syntax failures are preserved.

The reference survey records 18,062 Python import edges and 11 parse failures. External-or-standard-library status is not a dependency-security approval.
