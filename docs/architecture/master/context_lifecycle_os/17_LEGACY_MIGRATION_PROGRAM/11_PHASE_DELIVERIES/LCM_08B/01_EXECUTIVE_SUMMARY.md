---
title: "LCM-08B — 01 Executive Summary"
status: accepted-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, lcm-08b, pilot-migration]
phase_id: LCM-08B
---
# Executive Summary

LCM-08B migrates exactly one LCM-08A-selected pilot, `CTX_EXP0015_INTERMARKET_TIME_EXPERIMENT_3CD87586_V1`, from `lab/03_experiments/EXP0015_intermarket_time_divergence/experiment.py` into the ACL-compatible context package `lab/11_strategy_factory/contexts/CTX_EXP0015_INTERMARKET_TIME_EXPERIMENT_3CD87586_V1`. The source remains immutable. The canonical core is separated from the legacy research outcome projection. Ten deterministic golden cases pass exact field-level parity. No consumer cutover, source move, deletion, quarantine, runtime authority, live-order authority, or capital authority occurs.
