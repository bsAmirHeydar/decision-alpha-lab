---
title: "What Remains Strategy-Specific"
domain: strategy-factory-v2
status: canonical
language: en
version: 2.0.0
tags:
  - alpha-lab
  - strategy-factory
  - anatomy-to-decision
---

# Strategy-specific surface area

After V2, a new anatomy should customize only the irreducible semantics.

## Required

1. **Anatomy doctrine** — what the event means and when it is known.
2. **Anatomy adapter** — how the existing engine emits AnatomyEvent.
3. **Feature providers** — only features not already supplied by shared providers.
4. **Allowed candidate templates** — entry, stop, exit combinations compatible with the anatomy.
5. **Matched null** — the baseline that isolates whether the anatomy adds information.
6. **Golden fixtures** — canonical positive, negative, boundary, and invalid examples.

## Optional

- custom candidate policy;
- custom label;
- custom model plugin;
- custom decision policy;
- custom risk restriction;
- custom execution adapter when the instrument requires it.

## Shared and forbidden to duplicate

A strategy may not own a private implementation of:

- walk-forward splitting;
- anti-overfit controls;
- run registry;
- model registry;
- standard statistics;
- paper lifecycle;
- hard account risk;
- telemetry schema;
- promotion state machine;
- broker request audit.

If a strategy requires a missing capability, the capability is added to the shared kernel behind an interface and tests. It is not copied into the experiment directory.
