---
id: AIEOS2-88D6B0A24B42
title: "Compile and Runtime Compatibility"
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
# Compile and Runtime Compatibility

Language/library assumptions are untrusted until tested against the actual toolchain. Compatibility work records compiler/runtime version and exact diagnostic.

For MQL5, permanent compatibility checks include mutating string case functions, integer serialization, object API overloads, timeseries indexing, and unavailable history. Cascading parser warnings are fixed at the earliest causal line.
