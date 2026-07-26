---
title: "Authority, Ownership and Separation of Duties"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Authority, Ownership and Separation of Duties

## Required roles

- **Domain owner:** confirms doctrine, ambiguity resolutions and intended behavior.
- **Migration engineer:** inventories, adapts and refactors within approved semantics.
- **Parity reviewer:** independently evaluates traces and tolerances.
- **MQL5 reviewer:** verifies compile, tester, symbol/timeframe and object lifecycle behavior.
- **Security reviewer:** reviews order, file, network, secret and capital boundaries.
- **Knowledge curator:** resolves canonical documentation and Obsidian redirects.
- **Release operator:** packages, stages and records the patch.

No individual may both approve a semantic change and independently certify its parity. High-risk execution migration requires at least domain-owner and security-review approval in addition to engineering review.
