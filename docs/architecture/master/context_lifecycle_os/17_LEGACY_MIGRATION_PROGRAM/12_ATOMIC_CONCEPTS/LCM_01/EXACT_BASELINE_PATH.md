---
title: "Exact Baseline Path"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-01, atomic-concept]
phase_id: LCM-01
claim_ceiling: FORENSIC_SURVEY_REFERENCE_ONLY
---
# Exact Baseline Path

## Definition

A root-relative path present in the approved LCM-00 baseline manifest.

## Invariants

It is immutable during LCM-01; it appears exactly once in inventory; its byte hash must match.

## Evidence and use

Used as the closed subject set for every worker.

## Related

[[LCM01_INPUT_BASELINE_BINDING]]
