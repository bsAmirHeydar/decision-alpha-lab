# RTHP Real Train Activation v1

This directory is the context-owned activation layer that converts immutable paired tick artifacts into a complete RTHP research-training run while leaving every shared engine and the canonical RTHP Context unchanged.

## One-shot path

1. Validate an activation configuration.
2. Load causally ordered primary and secondary BID tick JSONL artifacts.
3. Build New York-time cycle instances.
4. Materialize canonical RTHP occurrences, reference states, cycle instances, and role price paths.
5. Resolve the real-data binding with local file URIs and SHA-256 digests.
6. Compile the existing RTHP ContextPackage features, views, and dependence clusters.
7. Compile only mature post-cut labels from the registered RTHP task and label contracts.
8. Freeze an immutable batch manifest.
9. Delegate training to the existing Strategy Factory TrainerRegistry and TaskOrchestrator.
10. Seal final-test access, package model evidence, write a run ledger, and verify all run hashes.

## Boundaries

The activation layer does not alter Context semantics, shared engines, treatment logic, execution, order routing, or capital authority. It does not fetch network data. All source artifacts must exist locally and expose explicit event and known times.

## Commands

```text
python -m strategy_factory_rthp_train_activation_v1 validate-config --config <config.json>
python -m strategy_factory_rthp_train_activation_v1 run --config <config.json>
python -m strategy_factory_rthp_train_activation_v1 verify-run --run-root <run-directory>
```

Use `configs/train_activation.real.template.v1.json` as the real-run template. The committed smoke profile and tick fixtures are deterministic non-alpha evidence only.
