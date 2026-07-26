---
title: "Pilot Selection and Migration Sequence"
tags: [strategy-factory, phase-00, pilot, migration]
status: canonical
---

# Pilot Selection and Migration Sequence

## Local foundation pilot

The uploaded snapshot selects:

```text
CP0001 Structural Nodes
+
M0001 Relative Territory Volatility
```

## Why this pilot

It is the only implemented path in the audited archive that crosses multiple future Strategy Factory boundaries:

```text
Market data
→ persistence
→ anatomy
→ event lifecycle
→ metric/feature
→ generated artifacts
```

It therefore exposes the exact migration problems the factory must solve:

- vendor-coupled data access;
- implicit timestamps;
- custom persistence;
- strategy-specific anatomy;
- feature/metric output;
- cache identity;
- live integration tests.

## What the pilot is not

It is not declared profitable. It is not the final multi-strategy pilot. It is not a replacement for EXP0017 or NDS.

It is a **foundation compatibility pilot** used to prove that the new contracts can wrap existing working logic without semantic drift.

## Migration sequence

### Stage A — Freeze observable legacy behavior

- create deterministic bar fixtures;
- store expected node outputs;
- store expected M0001 outputs;
- record edge cases.

### Stage B — Introduce canonical contracts

- canonical bar/time contract;
- anatomy-event contract;
- feature/metric record contract;
- artifact identity.

### Stage C — Wrap, do not rewrite

- legacy `MarketDataEngine` provider;
- L-rule anatomy adapter;
- M0001 feature/label adapter.

### Stage D — Differential validation

Run legacy and wrapped paths on identical fixtures. Compare:

- node identity;
- node price;
- confirmed state;
- revisit identity;
- zone bounds;
- M0001 values;
- row ordering;
- missing behavior.

### Stage E — Migrate persistence

Only after semantic parity:

- write canonical artifacts;
- dual-read or dual-write temporarily;
- verify hashes and schemas;
- retire custom cache paths.

## Later pilots

When the current full repository is supplied:

1. EXP0017 validates event-driven multi-symbol/time anatomy.
2. NDS Zone-AF validates deep proprietary anatomy and specialized candidate policies.

The full Factory is considered broadly reusable only after both later pilots reuse the post-anatomy core without private forks.
