---
title: "LCM-01 MQL5 Include Survey"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-01]
phase_id: LCM-01
claim_ceiling: FORENSIC_SURVEY_REFERENCE_ONLY
---
# LCM-01 MQL5 Include Survey

The MQL5 scanner indexes `#include` directives across the frozen `.mq5` and `.mqh` path set. It distinguishes resolved internal edges, ambiguous internal edges, unresolved edges and external platform-library edges.

The reference survey reports 3,181 MQL5 include edges. Preprocessor aliasing, generated include paths and runtime reachability remain explicit static-analysis limitations.
