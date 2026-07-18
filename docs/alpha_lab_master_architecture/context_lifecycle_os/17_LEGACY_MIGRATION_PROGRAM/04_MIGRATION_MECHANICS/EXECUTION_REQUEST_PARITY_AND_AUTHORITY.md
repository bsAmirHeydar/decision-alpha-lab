---
title: "Execution Request Parity and Authority"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Execution Request Parity and Authority

Execution migration is performed with broker submission disabled. The comparator evaluates normalized request intent: action, side, entry, stop, target, volume, expiry, cancellation, spread adjustment and rejection reason.

The canonical Context and Setup layers never own order APIs. Direct execution is isolated behind a capability-guarded adapter. Live authority remains false throughout LCM unless a separate promotion/runtime/security chain authorizes it.
