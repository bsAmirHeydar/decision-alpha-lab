---
title: "LCM-01 Scanner Configuration Freeze"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-01]
phase_id: LCM-01
claim_ceiling: FORENSIC_SURVEY_REFERENCE_ONLY
---
# LCM-01 Scanner Configuration Freeze

The scanner configuration freezes text decode limits, per-file edge limits, duplicate thresholds, namespace thresholds, Windows path threshold, include roots and ignored ephemeral directory names.

Configuration is written before scanning and included in the Survey ID material. Any behavior-changing scanner configuration requires a new configuration digest and therefore a new survey identity.
