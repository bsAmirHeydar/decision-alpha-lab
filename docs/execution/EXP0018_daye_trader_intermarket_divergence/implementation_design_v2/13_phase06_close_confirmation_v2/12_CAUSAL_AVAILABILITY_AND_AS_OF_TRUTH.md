---
id: EXP0018-P06-ASOF
title: "P06 Causal Availability and As-Of Truth"
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

# Causal truth

Three times remain separate:

- event time: target host close;
- availability time: when sufficient source and host evidence existed;
- processing time: callback execution.

A pending candidate accepts source updates only when `source_availability <= target_host_close`. Post-close source data cannot rewrite the close snapshot. Confirmation additionally requires source evidence available through the close.
