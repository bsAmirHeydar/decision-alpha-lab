---
title: "Capability and Ownership Map"
tags: [strategy-factory, phase-00, ownership, capability-map]
status: canonical
---

# Capability and Ownership Map

## Ownership rule

A shared kernel owns mechanics. A strategy or anatomy plugin owns market meaning. Infrastructure owns storage and transport. No module may own all three.

## Current-to-target ownership

| Capability | Current owner | Target owner | Migration form |
|---|---|---|---|
| Research governance | `docs/` | shared governance | reuse |
| MT5 data access | CP0000 connector | data connector plugin | adapt |
| Market-data service | CP0000 service | shared market-data port | wrap then migrate |
| Parquet persistence | CP0000 + CP0001 | shared Artifact Store | consolidate |
| L-rule anatomy | CP0001 detector | structural-node anatomy plugin | wrap |
| RTV metric | CP0001 metric | feature/label plugin | wrap |
| Experiments | legacy folders | manifest-driven run engine | migrate |
| Validation | empty shell | shared validation engine | replace |
| Registry | empty YAML files | schema-validated registries | adapt |
| Execution | empty folders | authority-gated execution packages | adapt later |
| Generated caches | source tree | versioned artifact storage | migrate |
| Tests | live scripts mixed with code | deterministic test architecture | migrate |

## Kernel exclusion list

The following semantics must never be moved into the shared Strategy Factory kernel:

- what constitutes an L-rule node;
- what constitutes a revisit;
- RTV zone geometry;
- future Hook, F, SMT, Daye, ICT, or Astro meanings;
- strategy-specific invalidation;
- strategy-specific confirmation.

The kernel may define interfaces for these concepts but must not implement their market meaning.

## Shared mechanics candidates

The following capabilities are appropriate future shared modules:

- canonical timestamp and bar contracts;
- artifact identity and atomic persistence;
- event identity;
- feature lineage;
- candidate policy interfaces;
- outcome simulation;
- cost conversion;
- fold planning;
- anti-overfit controls;
- model artifact registration;
- decision and abstention contracts;
- risk rejection;
- execution trace;
- telemetry.

## Authority boundaries

```text
Connector
  may read market data
  may not decide trades

Anatomy plugin
  may emit canonical events
  may not allocate risk

Feature plugin
  may compute known-time values
  may not inspect future outcomes

Model
  may score or rank
  may not send orders

Risk engine
  may reject or reduce
  may not invent market direction

Broker adapter
  may construct broker requests
  may not redefine strategy logic
```
