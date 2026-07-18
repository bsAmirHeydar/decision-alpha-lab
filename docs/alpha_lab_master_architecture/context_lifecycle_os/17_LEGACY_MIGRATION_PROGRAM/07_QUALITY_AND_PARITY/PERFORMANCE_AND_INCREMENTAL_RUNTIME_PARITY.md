---
title: "Performance and Incremental Runtime Parity"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Performance and Incremental Runtime Parity

Migration must not preserve correctness by recomputing all history on every tick. Performance evidence measures warm start, incremental update, history expansion, chart restart, multi-instance load and memory. Optimization may follow parity, but a performance refactor that changes event timing is a semantic change.
