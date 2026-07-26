---
title: "UCE-I11 Cache Validity Requires Provenance"
tags: [atomic-concept, uce-i11, strategy-factory]
status: canonical
---
# UCE-I11 Cache Validity Requires Provenance

## Definition

A matching payload hash is insufficient. Producer/schema versions, ordered input hashes, and provenance must match, otherwise the record is stale, incompatible, or corrupt.

## Why it exists

UCE-I11 must expose the complete search and execution universe to downstream statistical governance. Hidden mutation, silent cache reuse, deleted failures, or inferred semantics would make winner selection impossible to audit.

## Operational consequence

- Serialize the rule in a closed contract.
- Include its behavior fields in canonical identity.
- Test both the accepted and rejected path.
- Preserve resulting evidence for UCE-I12.

## Related implementation

- `strategy_factory_experiments_v3/contracts.py`
- `strategy_factory_experiments_v3/compiler.py`
- `strategy_factory_experiments_v3/scheduler.py`
- `strategy_factory_experiments_v3/ledger.py`
- [[../../strategy_factory_universal_context_exploitation_engine/implementation_program/phase_deliveries/uce_i11/00_UCE_I11_DELIVERY_MOC|UCE-I11 delivery MOC]]
