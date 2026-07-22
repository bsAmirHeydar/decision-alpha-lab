---
title: RTHP MT5 Automation — Read-Only MT5 API and No-Trade Authority
status: implemented
version: 1.0.0
updated: 2026-07-22
---

# Read-Only API Boundary

Allowed calls are connection, terminal/account/version information, symbol enumeration/selection/metadata, M1 history retrieval, last-error reporting, and shutdown. Trade, order, position mutation, and capital operations are absent from the code path and denied by registration.
