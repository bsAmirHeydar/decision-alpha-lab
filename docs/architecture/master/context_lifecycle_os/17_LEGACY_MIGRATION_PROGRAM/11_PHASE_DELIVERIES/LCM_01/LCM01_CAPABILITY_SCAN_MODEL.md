---
title: "LCM-01 Capability Scan Model"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-01]
phase_id: LCM-01
claim_ceiling: FORENSIC_SURVEY_REFERENCE_ONLY
---
# LCM-01 Capability Scan Model

Static token and AST evidence identifies 4,840 capability indicators across MQL5 and Python. Categories include order APIs, drawing, file I/O, network, timers, global variables, timeframe access, session/DST terms, chart callbacks, multi-symbol access, indicator buffers, persistence, subprocess, dynamic evaluation/import/compile and mutation indicators.

Every hit is marked `risk_indicator_only=true` and `live_authority_inferred=false`. Capability presence triggers review; it does not prove runtime reachability.
