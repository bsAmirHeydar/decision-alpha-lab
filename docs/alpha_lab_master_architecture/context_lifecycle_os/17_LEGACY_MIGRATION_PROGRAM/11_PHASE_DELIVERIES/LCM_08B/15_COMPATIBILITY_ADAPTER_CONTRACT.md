---
title: "LCM-08B — 15 Compatibility Adapter Contract"
status: accepted-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, lcm-08b, pilot-migration]
phase_id: LCM-08B
---
# Compatibility Adapter Contract

The adapter translates canonical occurrences into the exact legacy dataclass shape, restores sequential event IDs, pair label, outcome columns, and note text. It cannot add filters, normalize intentional variance, call order APIs, mutate chart objects, change source files, or switch consumers.
