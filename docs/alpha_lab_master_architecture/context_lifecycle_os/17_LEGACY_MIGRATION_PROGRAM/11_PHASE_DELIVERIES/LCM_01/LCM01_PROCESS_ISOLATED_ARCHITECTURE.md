---
title: "LCM-01 Process-Isolated Scanner Architecture"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-01]
phase_id: LCM-01
claim_ceiling: FORENSIC_SURVEY_REFERENCE_ONLY
---
# LCM-01 Process-Isolated Scanner Architecture

Large repository scans are split into inventory, MQL5, Python, documentation, configuration and structural workers. Each worker loads the closed baseline, writes only its owned output set and exits, releasing memory before the next stage.

The parent process retains only compact authority and provenance metadata. Stage outputs are not trusted merely because a worker exited successfully; each worker publishes a digest-bound receipt that is re-verified before finalization.
