---
title: "LCM-01 Operations Runbook"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-01]
phase_id: LCM-01
claim_ceiling: FORENSIC_SURVEY_REFERENCE_ONLY
---
# LCM-01 Operations Runbook

Run baseline verification first, then execute the inventory, MQL5, Python, documentation, configuration and structural workers into a private empty staging root. Verify every stage receipt, merge bounded views, build summary/events/provenance/handoff, publish atomically, then run package verification and deterministic replay.

Never point the survey destination at a non-empty path. Never modify baseline files to make the scanner pass. Resolve scanner defects in a separate code patch and rebuild the full survey.
