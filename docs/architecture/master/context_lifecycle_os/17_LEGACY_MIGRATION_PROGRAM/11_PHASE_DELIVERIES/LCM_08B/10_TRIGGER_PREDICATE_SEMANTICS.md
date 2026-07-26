---
title: "LCM-08B — 10 Trigger Predicate Semantics"
status: accepted-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, lcm-08b, pilot-migration]
phase_id: LCM-08B
---
# Trigger Predicate Semantics

For HIGH, wick touch is `high >= level`, close break is `close > level`, and hunt-reject is `high >= level and close < level`. LOW mirrors these inequalities. Equality behavior is preserved exactly. Break-points use the same price component as the trigger predicate.
