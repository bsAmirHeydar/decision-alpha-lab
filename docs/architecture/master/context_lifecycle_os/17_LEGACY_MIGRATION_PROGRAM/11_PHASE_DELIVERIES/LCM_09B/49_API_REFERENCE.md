---
status: accepted-reference
version: 1.0.0
updated: 2026-07-20
tags: [acl-os, lcm, lcm-09b, setup-migration]
phase_id: LCM-09B
claim_ceiling: LCM_09B_REFERENCE_ONLY
---
# API Reference

## Build service

```python
LCM09BSetupMigrationService().build(repo_root: Path, output_root: Path) -> dict
```

Builds the migration package from the exact LCM-09A freeze. Existing output root is replaced only after upstream input validation. Returns stable migration, count, handoff, and manifest information.

## Pure evaluator

```python
CanonicalSetupEvaluator().evaluate(package, snapshot, sequence=1, prior_state=None) -> dict
```

Evaluates only validated canonical packages over caller-supplied Context snapshots. Blocked packages emit deterministic `BLOCKED` / `no_trade=true`. Incomplete known-time input, Context identity mismatch, or invalid package digest raises a contract error.

## Legacy evidence adapter

```python
LegacyDecisionAdapter().normalize(registration, event) -> dict
```

Normalizes an externally supplied observed event. It rejects blocked adapters and unknown event types and never loads legacy source.

## Factory reference port

```python
port = SetupFactoryReferencePort(registration_path)
port.list_reference_candidates() -> list[dict]
port.get(setup_id: str) -> dict
```

Loads a digest-valid authority-negative registry. It exposes copies of reference records and cannot modify Factory selection state.

## Restart functions

```python
checkpoint(state: dict) -> dict
restore(checkpoint_doc: dict) -> dict
```

Creates and verifies a digest-bound lifecycle checkpoint. Tampering or invalid sequence fails.

## Verification

```python
verify_package(package_root: Path) -> dict
verify_installation(repo_root: Path, package_root: Path, index_path: Path) -> dict
```

Verifies required artifacts, manifest bytes, packages, Factory registration, parity, acceptance, hostile review, handoff, artifact locator, authority boundary, and installation paths.

## CLI

```text
python -m src.engine.tooling.strategy_factory.lcm.lcm_09b.cli build
python -m src.engine.tooling.strategy_factory.lcm.lcm_09b.cli verify-package
python -m src.engine.tooling.strategy_factory.lcm.lcm_09b.cli verify-installation
python -m src.engine.tooling.strategy_factory.lcm.lcm_09b.cli qa
python -m src.engine.tooling.strategy_factory.lcm.lcm_09b.cli validate-schemas
python -m src.engine.tooling.strategy_factory.lcm.lcm_09b.cli static-validate
```

All commands require explicit paths; no repository or package location is silently guessed.
