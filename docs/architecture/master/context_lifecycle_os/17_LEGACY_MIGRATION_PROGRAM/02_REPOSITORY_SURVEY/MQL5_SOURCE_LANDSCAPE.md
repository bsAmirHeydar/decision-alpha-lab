---
title: "MQL5 Source Landscape"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# MQL5 Source Landscape

The project contains 2,457 MQL source files: 288 `.mq5` and 2,169 `.mqh` files.

## Structural observations

- Source is split across Experts, Indicators, Scripts and multiple Include namespaces.
- `AlphaLab`, `DecisionAlphaLab` and `StrategyFactory` coexist as namespace roots.
- Static contract mirrors from ACL/SAED/UCE must not be mistaken for domain runtime logic.
- Direct order-capability pattern hits occur in E-series, FlagCounting/NDS, Intermarket execution and selected platform adapters.
- Drawing and timeframe APIs are distributed across domain and visualization files, indicating responsibility coupling that must be characterized before extraction.

## Required next analysis

LCM-01 resolves include targets, reachable entry points, compile units and source ownership. LCM-03 assigns identities. LCM-04 captures event traces. No MQL file is moved solely from this initial pattern scan.
