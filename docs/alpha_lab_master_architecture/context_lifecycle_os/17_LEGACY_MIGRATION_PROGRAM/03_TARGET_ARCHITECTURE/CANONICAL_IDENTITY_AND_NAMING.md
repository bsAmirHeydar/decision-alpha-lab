---
title: "Canonical Identity and Naming"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Canonical Identity and Naming

Canonical IDs are stable and independent of path:

- `CTX_<FAMILY>_<NAME>_V<MAJOR>`
- `STP_<FAMILY>_<NAME>_V<MAJOR>`
- `TRT_<FAMILY>_<NAME>_V<MAJOR>`
- `VIS_<FAMILY>_<NAME>_V<MAJOR>`
- `ENG_<DOMAIN>_<NAME>_V<MAJOR>`
- `ADP_<PLATFORM>_<NAME>_V<MAJOR>`

A semantic breaking change creates a new major identity. A move, documentation fix or compatible adapter update does not create a new domain identity. Every old file, symbol, experiment code and object prefix maps through the Legacy Alias Registry.
