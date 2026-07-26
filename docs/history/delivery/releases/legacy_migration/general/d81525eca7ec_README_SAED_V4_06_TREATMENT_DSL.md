# SAED V4-06 — Treatment DSL V4

This patch implements the reference-only V4-06 finite Treatment declaration layer for Decision Alpha Lab. It consumes the immutable V4-05 graph/handoff, defines an exact-versioned institutional primitive registry, parses closed source programs, performs deterministic static analysis, canonicalizes accepted programs, binds approved graph descriptors, and emits integrity, replay, diff, partition, exposure and V4-07 handoff artifacts.

## Authority

The phase can define, validate, canonicalize, bind, replay and diff a finite DSL. It cannot mutate UCEE or the V4-05 graph, infer Context truth, generate an unbounded action space, solve the action lattice, train a model, select a Treatment, allocate capital, activate runtime, access a network or submit an order.

## Main paths

- Python: `lab/11_strategy_factory/python/saed_v4_treatment_dsl`
- Tests: `lab/11_strategy_factory/tests/phase_saed_v4_06_treatment_dsl`
- Schemas: `lab/11_strategy_factory/schemas/saed_v4_06`
- Fixtures: `lab/11_strategy_factory/examples/saed_v4_06`
- Evidence: `lab/11_strategy_factory/artifacts/saed_v4_06` and phase artifacts
- MQL5: `mql5/Include/AlphaLab/StrategyFactory/SAEDV4TreatmentDsl`
- Obsidian: `docs/strategy_factory_sovereign_context_intelligence_v4/62_PHASE_DELIVERIES_V4/V4_06`
- QA: `tools/strategy_factory/saed_v4_06`

## Validation

Run `python tools/strategy_factory/saed_v4_06/run_saed_v4_06_full_qa.py`, then `python tools/strategy_factory/saed_v4_06/validate_saed_v4_06_delivery.py`. MetaEditor compilation remains pending local Windows evidence.
