---
id: EXP0018-P06-SECURITY
title: "P06 Security and No-Execution Boundary"
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

# Security boundary

P06 contains no `CTrade`, `OrderSend`, position management, WebRequest, model call, licensing mutation, or object creation. File writes are restricted to optional audit and state checkpoint files in MetaTrader Common Files.
