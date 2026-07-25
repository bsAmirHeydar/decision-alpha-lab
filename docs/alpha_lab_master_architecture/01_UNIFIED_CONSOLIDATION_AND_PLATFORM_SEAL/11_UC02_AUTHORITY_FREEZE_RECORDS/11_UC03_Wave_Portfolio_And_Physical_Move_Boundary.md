---
id: UCPS-3DD090D4F385
title: "UC-03 Wave Portfolio and Physical-Move Boundary"
type: execution-record
status: approved
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-24
updated: 2026-07-24
tags:
  - consolidation
  - uc02
  - authority-freeze
---
# UC-03 Wave Portfolio and Physical-Move Boundary

## Wave portfolio

UC-02 assigns every artifact to one physical-reorganization wave:

- `UC03-W01-ROOT` — root and repository controls;
- `UC03-W02-CODE` — Python production source and Context split;
- `UC03-W03-CONTRACTS` — contracts, schemas, policies, configurations and adapters;
- `UC03-W04-DOCS` — documentation and Obsidian links;
- `UC03-W05-MQL5` — terminal topology and includes;
- `UC03-W06-TESTS` — one test hierarchy and collision removal;
- `UC03-W07-REGISTRY` — identity and state records;
- `UC03-W08-RELEASES` — release-history normalization;
- `UC03-W09-PRODUCTS` — product and example surfaces;
- `UC03-W10-GENERATED` — runtime, data and generated-artifact externalization;
- `UC03-W11-OPS` — operations and maintenance tooling.

## Move-before-refactor rule

UC-03 changes physical location and references while preserving behavior. Semantic merging belongs to UC-04. Combining both changes in one wave is forbidden unless an approved ADR proves separation is impossible.

## Deletion boundary

No wave may delete a legacy implementation merely because a target directory exists. Deletion waits for UC-04 parity, UC-06 cutover and UC-07 authorization.
