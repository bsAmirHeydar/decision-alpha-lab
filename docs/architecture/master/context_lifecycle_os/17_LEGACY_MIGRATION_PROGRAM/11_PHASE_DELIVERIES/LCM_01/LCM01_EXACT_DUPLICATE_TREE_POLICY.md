---
title: "LCM-01 Exact-Duplicate Tree Policy"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-01]
phase_id: LCM-01
claim_ceiling: FORENSIC_SURVEY_REFERENCE_ONLY
---
# LCM-01 Exact-Duplicate Tree Policy

The reference survey identifies 4 exact duplicate namespace-tree groups. Equality requires identical relative path sets and byte hashes.

Exact tree equality proves byte equivalence only. It does not grant deletion authority because links, history, external consumers and canonical-location decisions remain unresolved.
