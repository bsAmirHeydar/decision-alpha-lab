---
title: Repository and File Map
status: proposed-reference
version: 1.0.0
updated: 2026-07-17
tags: [acl-os, context-lifecycle]
---
# Repository and File Map

Every artifact has one canonical home, owner and edit policy.

## Canonical roots

- `docs/architecture/master/context_lifecycle_os/`: architecture, ADRs, templates and runbooks.
- `registry/history/acl/`: public schemas, catalogs, policies and compatibility metadata.
- `lab/11_strategy_factory/contexts/<context_id>/`: authored Context packages.
- `lab/11_strategy_factory/acl_os/`: reference fixtures and tests.
- `tools/strategy_factory/acl_os/`: scaffold, validation and delivery tools.
- Future `src/alpha_lab/acl_os/`: production control-plane package.
- Future `mql5/Include/StrategyFactory/ACL/`: generated/runtime mirror contracts.
- External content-addressed store: immutable datasets, models, reports and runtime generations.
- Event store/control database: operational state; never source code.

## Authored versus generated

Doctrine, policy and source contracts are authored. Compiler/report projections live under `generated/` and carry source hashes. Research evidence is immutable by Batch ID. Runtime bundles are immutable by generation ID. Generated files are never edited by hand.

## Ownership

Every domain has semantic, technical and security owners. Capital authority is separate. Folders inherit explicit ownership declarations; unowned paths fail architecture QA.

## Relocation and change

Paths are not identities. Relocation requires an artifact-locator update, migration map, compatibility checks and deprecation notice. Historical references remain resolvable without preserving old coupling.

## Related

- [[CANONICAL_REPOSITORY_TOPOLOGY]]
- [[FOLDER_OWNERSHIP_AND_BOUNDARIES]]
- [[NAMING_AND_IDENTITY_STANDARD]]
