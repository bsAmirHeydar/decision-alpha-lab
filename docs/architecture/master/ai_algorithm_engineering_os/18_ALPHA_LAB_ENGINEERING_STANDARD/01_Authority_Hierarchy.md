---
id: AIEOS2-DB06E6EA9040
title: "Authority Hierarchy and Policy Precedence"
type: standard
status: active
domain: alpha-lab-standard
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - alpha-lab
  - alpha-lab-standard
---
# Authority Hierarchy and Policy Precedence

## Rule

The repository must have one deterministic answer to “which document wins?” Use the precedence defined in `AGENTS.md` and the project policy. An implementation detail, model score, or historical accident cannot override an approved domain rule.

## Decision Procedure

1. Identify all conflicting claims.
2. Classify each artifact as normative or informative.
3. Compare authority rank and version/status.
4. Preserve current safe behavior until resolved.
5. Record the resolution in an ADR/decision log.
6. Update contracts, tests, and downstream consumers.

## Failure Signals

- Two modules implement different definitions for the same term.
- A dashboard threshold becomes a filter without promotion.
- A comment contradicts a specification.
- A hotfix introduces an undocumented permanent exception.
