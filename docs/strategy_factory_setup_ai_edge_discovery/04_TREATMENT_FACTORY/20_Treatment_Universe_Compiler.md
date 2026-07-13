---
id: SAED-FF28FD1F54
title: "Treatment Universe Compiler"
type: architecture
status: canonical
domain: strategy-factory-setup-ai-edge-discovery
version: 1.0.0
created: 2026-07-13
updated: 2026-07-13
tags:
  - strategy-factory
  - setup-factory
  - ai-training
  - treatment
  - compiler
---

# Treatment Universe Compiler

## Mission

Compile a finite, declared and auditable candidate universe from Context capabilities, payoff profiles, entry mechanisms, treatment atoms and objective guardrails.

## Compilation Stages

1. Load exact Context package and capability declaration.
2. Load style, entry, stop, exit, management and cost registries.
3. Generate semantic combinations.
4. Apply compatibility graph.
5. Validate geometry and direction.
6. Validate known-time availability.
7. Validate broker/execution feasibility.
8. Remove exact duplicates.
9. Mark deterministic dominance without hiding the attempt.
10. Enforce sample/capability requirements.
11. Add `Skip`, Manual baseline and conservative fallback.
12. Freeze universe hash.

## Output

A `treatment_universe_freeze` plus compiled drafts and rejection evidence for every excluded candidate.

## Invariant

Pruned candidates remain visible to multiplicity accounting. Pruning is not deletion.
