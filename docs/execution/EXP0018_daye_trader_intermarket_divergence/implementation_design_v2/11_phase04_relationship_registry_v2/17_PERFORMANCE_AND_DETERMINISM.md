---
id: EXP0018-P04-PERFORMANCE
title: "P04 Performance and Determinism"
type: nonfunctional-contract
status: active
project: EXP0018
phase: P04
---
# Performance and Determinism

Registry size is fixed at 22. Resolution complexity is bounded by period-count × 22 and uses exact IDs. P04 reprocesses only when the P03 source fingerprint changes. Output count is bounded by configuration. Repeated input stores must produce byte-stable registry mappings and stable opportunity IDs.
