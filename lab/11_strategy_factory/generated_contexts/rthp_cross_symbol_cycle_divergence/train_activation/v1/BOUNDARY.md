# RTHP Train Activation Boundary

## Owned by this layer

- Raw paired-tick source validation.
- RTHP historical materialization and ledger emission.
- RTHP real-data binding resolution.
- ContextPackage feature/view/cluster compilation.
- RTHP label maturity and task binding.
- Context-owned batch manifest generation.
- Invocation of existing trainer plugins and the existing TaskOrchestrator.
- Immutable run packaging and verification.

## Delegated to existing engines

- ContextPackage contracts and view compilers.
- Trainer capability registry.
- Classical, reference, ranking, and survival trainer implementations.
- Guarded dataset access.
- OOF/final-test orchestration.
- Metrics, serialization parity, artifact packaging, and model cards.

## Prohibited

- Editing canonical RTHP Context files.
- Editing shared Engine files or registries.
- Creating Entry, Stop, Target, Treatment, Order, or Capital authority.
- Network fetches.
- Using a source record whose known time precedes event time.
- Using post-cut values as features.
- Training on unmatured labels.
- Reusing an existing immutable run directory.
