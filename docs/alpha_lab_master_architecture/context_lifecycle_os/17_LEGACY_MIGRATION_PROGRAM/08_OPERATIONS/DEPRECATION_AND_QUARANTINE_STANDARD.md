---
title: "Deprecation and Quarantine Standard"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Deprecation and Quarantine Standard

Lifecycle: `ACTIVE_LEGACY → WRAPPED_LEGACY → PARITY_VERIFIED → DEPRECATED → QUARANTINED → DELETE_ELIGIBLE → RETIRED`.

Deprecation warnings identify the canonical successor and removal window. Quarantine removes code from active compile/runtime paths while preserving original bytes, hashes, dependencies, parity and restoration instructions.
