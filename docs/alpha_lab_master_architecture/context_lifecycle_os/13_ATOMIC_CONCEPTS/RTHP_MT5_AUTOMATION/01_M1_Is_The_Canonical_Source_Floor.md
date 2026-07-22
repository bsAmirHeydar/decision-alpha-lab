---
title: M1 Is the Canonical Source Floor
status: roadmap-approved-for-implementation
version: 1.0.0
updated: 2026-07-22
tags: [rthp, mt5, atomic-concept]
---
# M1 Is the Canonical Source Floor

The production RTHP acquisition path begins with fully closed M1 bars. Sub-M1 bars and raw tick history are not canonical inputs. Higher intervals are deterministically aggregated from M1. This avoids broker-specific false precision while preserving the M15-confirmed Context.
