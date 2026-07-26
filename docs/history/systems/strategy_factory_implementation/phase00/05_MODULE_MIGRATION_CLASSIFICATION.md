---
title: "Module Migration Classification"
tags: [strategy-factory, phase-00, migration]
status: canonical
---

# Module Migration Classification

## Classification vocabulary

### `REUSE_AS_IS`

The capability and ownership are already compatible with the target architecture. Minor editorial changes do not change classification.

### `ADAPT`

The implementation is useful, but its interface, dependency direction, schema, or lifecycle must change.

### `WRAP`

The implementation should remain semantically intact behind a new interface. Wrapping is preferred when changing internals could alter market meaning.

### `MIGRATE`

The capability belongs in a different storage, package, or lifecycle system. Old and new may coexist during transition.

### `DEPRECATE`

The capability will remain temporarily accessible but must not receive new dependents.

### `DELETE_LATER`

The artifact is generated or obsolete. Removal waits until ignore rules and rollback evidence exist.

### `REVIEW`

Evidence is insufficient for a binding decision.

## Current classification counts

| Action | Count |
|---|---:|
| Reuse as-is | 1 |
| Adapt | 4 |
| Wrap | 3 |
| Migrate | 6 |
| Delete later | 2 |

## Binding decisions

### Reuse

`docs/` research governance is preserved because its separation of research and execution matches the target platform.

### Adapt

- `MT5Connector` becomes a vendor-specific data connector implementing a canonical port.
- `ParquetStore` contributes persistence behavior but not its current path semantics.
- `registry/` remains a public location but gains validated schemas.
- `lab/09_execution/` retains the authority boundary but not placeholder-only contents.

### Wrap

- `MarketDataEngine` is wrapped so existing MQL-style accessors can continue during migration.
- `LRuleNodeDetector` is wrapped as anatomy-specific logic.
- `M0001RTV` is wrapped as a feature/label producer.

### Migrate

- experiment folders;
- validation shell;
- market-data cache;
- node cache;
- metric cache;
- live/manual test scripts.

### Delete later

- tracked Python bytecode;
- `.pytest_cache`.

## Prohibited migration shortcut

No later phase may copy a legacy module into the shared kernel merely to avoid writing an adapter. Ownership must follow capability semantics, not convenience.
