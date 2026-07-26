---
title: "LCM-01 Input Baseline Binding"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-01]
phase_id: LCM-01
claim_ceiling: FORENSIC_SURVEY_REFERENCE_ONLY
---
# LCM-01 Input Baseline Binding

The only admissible repository path set is the LCM-00 baseline `BASELINE_E214DB424C25F427B988901324A38EE6`, bound by manifest digest `sha256:6c90efabe69899c449caf188d7785de20f10d7db6027eeb985dd488c79555b6c`. LCM-01 re-verifies every file hash before scanning.

The survey must not expand its subject set by walking newly created LCM-01 outputs. All scanner stages derive their closed input paths from the baseline manifest. The LCM-00 handoff digest is preserved in the survey receipt, provenance graph and LCM-02 handoff.
