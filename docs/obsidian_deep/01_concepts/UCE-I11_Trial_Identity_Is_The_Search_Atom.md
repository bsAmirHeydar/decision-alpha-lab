---
title: "UCE-I11 Trial Identity Is The Search Atom"
tags: [atomic-concept, uce-i11, strategy-factory]
status: canonical
---
# UCE-I11 Trial Identity Is The Search Atom

## Definition

A trial is the complete tuple of candidate, trainer, parameters, fold, seed, resource level, dataset/split/transform/target/economics/known-time identities, search/budget policies, and compiler/scheduler versions. Omitting any behavior axis creates a false cache/reproducibility equivalence.

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
