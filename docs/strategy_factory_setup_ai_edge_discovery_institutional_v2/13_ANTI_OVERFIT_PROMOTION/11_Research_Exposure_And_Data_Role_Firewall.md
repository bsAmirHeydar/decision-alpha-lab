---
title: Research Exposure and Data-Role Firewall
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- gap-closure
- canonical
---

# Principle

Evidence is consumed not only by code, but by humans, agents, dashboards, reports and decisions. Every protected observation is an exposure.

# Roles

Exploration, training, calibration, selection-validation, locked-final, prospective-paper, shadow, micro-live and live are independently authorized.

# Enforcement

- Row/object storage access policies.
- Query and export audit.
- Agent capability tokens.
- Dashboard/report exposure logging.
- Versioned exposure ledger linked to experiment decisions.
- New final evidence or downgrade when exposure exceeds policy.

# Kill criteria

Unlogged access, cross-role preprocessing, repeated locked tuning, manual cherry-picking or model/agent memory contamination.
