---
title: Missing Bar Is Not Automatically Missing Data
status: roadmap-approved-for-implementation
version: 1.0.0
updated: 2026-07-22
tags: [rthp, mt5, atomic-concept]
---
# Missing Bar Is Not Automatically Missing Data

An absent M1 timestamp can represent a market closure, symbol-specific session, holiday, no-quote interval, terminal truncation, acquisition failure, or unexplained gap. The quality layer must classify the cause before deciding whether the interval is acceptable or blocking.
