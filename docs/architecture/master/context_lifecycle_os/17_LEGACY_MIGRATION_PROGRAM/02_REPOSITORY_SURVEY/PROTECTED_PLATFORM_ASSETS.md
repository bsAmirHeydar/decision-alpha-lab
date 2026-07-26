---
title: "Protected Platform Assets"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Protected Platform Assets

The following are protected from context-migration refactors unless a separate platform ADR authorizes changes:

- `lab/11_strategy_factory/acl_os`;
- `tools/strategy_factory/acl_os`;
- ACL-00…ACL-15 fixtures and tests;
- Strategy Factory platform contracts;
- SAED and UCE/UCEE research/platform modules;
- accepted master-architecture documents.

LCM may consume these interfaces, add migration adapters and report incompatibilities. It may not simplify the platform by folding Context-specific logic into the kernel.
