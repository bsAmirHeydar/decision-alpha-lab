---
title: "LCM-01 Reproducibility Contract"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-01]
phase_id: LCM-01
claim_ceiling: FORENSIC_SURVEY_REFERENCE_ONLY
---
# LCM-01 Reproducibility Contract

Reproducibility is bound to baseline digest, source handoff digest, scanner version and scanner configuration. Scanner stages use deterministic sort keys and canonical JSON digests.

QA rebuilds the survey into a fresh destination and compares Survey ID and summary digest. Host Python version is reported but excluded from Survey ID material.
