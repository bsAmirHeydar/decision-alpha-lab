---
id: EXP0018-P06-PERFORMANCE
title: "P06 Performance and Refresh"
type: implementation-note
status: implemented
project: EXP0018
phase: P06
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - exp0018
  - p06
  - confirmation
---

# Performance

- timer-driven; no work in `OnTick`;
- only two current and two closed host bars are requested per refresh;
- pending candidate count is bounded;
- runtime result count and finalized identity memory are bounded;
- checkpoint writes occur only when state or host-close identity changes;
- no full historical host-bar scan occurs in live P06.
