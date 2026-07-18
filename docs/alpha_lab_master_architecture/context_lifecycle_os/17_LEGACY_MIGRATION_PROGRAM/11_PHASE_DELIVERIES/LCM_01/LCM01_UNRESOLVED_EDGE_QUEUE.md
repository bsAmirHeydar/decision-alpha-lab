---
title: "LCM-01 Unresolved Edge Queue"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-01]
phase_id: LCM-01
claim_ceiling: FORENSIC_SURVEY_REFERENCE_ONLY
---
# LCM-01 Unresolved Edge Queue

The reference survey preserves 15,117 unresolved, ambiguous or path-escape edges in a dedicated queue. The queue includes source path, line, edge type, raw target and reported candidates.

LCM-02 may classify and assign ownership to these edges. It may not convert them to resolved status without evidence or treat absence of resolution as proof that the target is unused.
