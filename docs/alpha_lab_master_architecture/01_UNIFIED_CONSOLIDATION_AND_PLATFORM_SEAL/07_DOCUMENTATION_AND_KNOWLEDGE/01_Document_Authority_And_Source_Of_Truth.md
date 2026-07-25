---
id: UCPS-F01603A928C9
title: "Document Authority and Source of Truth"
type: standard
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - consolidation
  - platform-seal
---
# Document Authority and Source of Truth

## Authority hierarchy

Machine contracts, schemas and policies define executable truth. Accepted ADRs define approved architectural deviation. Canonical notes explain architecture and operation. Generated notes project machine state. Historical notes preserve context but have no active authority.

## One-concept rule

Each concept has one normative machine definition and at most one canonical human explanation per audience. Duplicated authoritative-looking notes are defects.

## Status semantics

`canonical`, `approved`, `generated`, `operational`, `deprecated`, `historical` and `superseded` have explicit meaning. Status must be visible in frontmatter.

## Drift

Documentation and code are checked through references, contract digests, generated projections and review gates. A note that contradicts a machine contract cannot remain canonical.
