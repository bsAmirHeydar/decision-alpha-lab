---
title: No Intrabar Order Inference from M1
status: roadmap-approved-for-implementation
version: 1.0.0
updated: 2026-07-22
tags: [rthp, mt5, atomic-concept]
---
# No Intrabar Order Inference from M1

OHLC does not reveal the path inside a minute. The adapter may detect whether a level was inside the bar range, but it cannot infer the exact tick time or whether High occurred before Low. Ambiguity is represented explicitly rather than resolved by a synthetic path.
