---
id: UCPS-0FCA70BAD098
title: "System Disposition and Capability Ownership"
type: architecture
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - consolidation
  - platform-seal
---
# System Disposition and Capability Ownership

## Final disposition

| Current system | Final role |
|---|---|
| Strategy Factory V1/V2 | capabilities merged into canonical engine; unique behavior retained as extensions or fixtures |
| ACL-OS | lifecycle, identity, authority and evidence capabilities distributed into canonical modules |
| UCEE | Treatment, research, policy, portfolio, runtime and execution capabilities merged into their domain owners |
| SAED V3/V4 | one governed research extension; no parallel identity or authority plane |
| AIEOS | engineering standards, policies and tools; not a second operating system |
| LCM | historical evidence plus selected maintenance tools; no active phase engine after seal |
| RTHP | Golden Context package under `contexts/rthp/` |
| NDS and EXP families | Context, Extension, Adapter, Fixture, Product or Historical Reference by explicit disposition |

## Ownership rule

A capability may have multiple strategies, policies or adapters but only one interface authority and one default production implementation. Distinct semantics are preserved as named variants rather than hidden duplicates.

## Required records

The capability ownership matrix records current implementations, canonical owner, retained variants, consumer count, migration wave and retirement criteria.
