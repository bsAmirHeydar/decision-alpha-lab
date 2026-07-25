# Alpha Lab — RTHP Real Train Activation v1

This additive patch completes the context-owned path from immutable paired tick data to an executable RTHP research-training run. It does not modify the canonical RTHP Context or any shared ACL, SAED, UCEE, Dataset, Trainer, Validation, Treatment, Execution, or Runtime engine.

## Delivered capability

A single context-owned command now performs:

1. source validation and immutable source snapshotting;
2. New York-time cycle construction;
3. RTHP relation-candidate and synchronized-confirmation materialization;
4. automatic creation of the occurrence, reference-state, cycle-instance, and role-price-path ledgers;
5. automatic real-data binding resolution with local URIs and SHA-256 hashes;
6. existing ContextPackage feature, view, and dependence-cluster compilation;
7. post-cut mature-label compilation from the existing RTHP task and label registries;
8. immutable batch freezing;
9. training through the existing TrainerRegistry and TaskOrchestrator;
10. selection locking, final-test sealing, model evidence packaging, run hashing, and independent verification.

## Train command

```text
$env:PYTHONPATH = 'lab/11_strategy_factory/python'
python -m strategy_factory_rthp_train_activation_v1 validate-config --config <run-config.json>
python -m strategy_factory_rthp_train_activation_v1 run --config <run-config.json>
python -m strategy_factory_rthp_train_activation_v1 verify-run --run-root <run-output-root>
```

Copy the committed real template from:

`lab/11_strategy_factory/generated_contexts/rthp_cross_symbol_cycle_divergence/train_activation/v1/configs/train_activation.real.template.v1.json`

and replace every placeholder with real immutable source information.

## Release evidence

- 12 direct activation tests passed.
- 400 existing RTHP/ACL/UCEE regression tests passed.
- Deterministic smoke materialization produced 1,300 confirmed occurrences.
- Two smoke research tasks trained successfully through the existing trainer engine.
- Shared Engine files changed: 0.
- Canonical RTHP Context files changed: 0.
- Existing repository files overwritten: 0.
