---
title: "LCM-01 Dependency Resolution Model"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-01]
phase_id: LCM-01
claim_ceiling: FORENSIC_SURVEY_REFERENCE_ONLY
---
# LCM-01 Dependency Resolution Model

Resolution statuses are closed: resolved internal, ambiguous internal, unresolved, external platform library, external-or-standard-library, external URI, anchor-only and path escape.

Resolved means that the static target maps to one baseline path. It does not mean the source path is active, the edge executes, or the target is semantically valid. Ambiguous and unresolved edges are blockers for deletion and cutover decisions.
