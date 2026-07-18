---
title: "LCM-01 Windows Path-Risk Survey"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-01]
phase_id: LCM-01
claim_ceiling: FORENSIC_SURVEY_REFERENCE_ONLY
---
# LCM-01 Windows Path-Risk Survey

Windows reserved names, trailing dot/space components and long root-relative paths are reported. The frozen threshold is part of the scanner configuration.

The reference survey reports 0 long-path findings at the configured threshold. This is a repository-path check, not a guarantee about every user checkout prefix.
