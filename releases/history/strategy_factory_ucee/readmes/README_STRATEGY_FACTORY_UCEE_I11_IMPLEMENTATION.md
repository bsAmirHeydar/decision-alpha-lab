# UCEE I11 — Experiment DAG, Search, Scheduling, and Budget Governance

UCE-I11 is the deterministic experiment-orchestration layer after the UCE-I10 model/view packs. It compiles admitted candidates, immutable data contracts, folds, seeds, parameter spaces, objectives, calibration/threshold axes, resource claims, and export requirements into an exact DAG and complete trial universe.

## Delivered surfaces

- Pure `ExperimentDagCompiler` with stable trial/node/edge/resource identities.
- Candidate admission boundary: UCE-I10 `accept`/`warn` are schedulable; `reject` is evidence-only.
- Baseline-first deterministic priority.
- Grid, seeded random, Halton quasi-random, deterministic TPE reference, successive halving, Hyperband, evolutionary, Pareto, and optional Optuna boundary.
- Hard trial/candidate/time/memory/CPU/GPU/retry/artifact/seed/fold budgets.
- Deterministic dependency scheduler with retry, cancellation, timeout, quarantine, cache hit, and resume evidence.
- Spawn-based local worker isolation and deterministic environment capture.
- Append-only hash-chained selection ledger.
- Content-addressed cache with producer/schema/input/provenance validation.
- Declared-versus-executed and artifact/event reproducibility audit.
- 24 closed JSON schemas and deterministic conformance vectors.
- MQL5 contract mirror, registry, budget guard, diagnostic, and self-tests.
- Detailed Obsidian delivery chapters, ADRs, atomic concepts, operator checklist, status, acceptance evidence, and UCE-I12 handoff.

## Authority boundary

This phase has no broker, order, position, live-network, or trading authority. It schedules offline/research work and produces evidence for UCE-I12. A strong model metric is not a promotion decision.

## QA baseline

- UCE-I11 phase tests: 59 passed.
- UCE-I01 through UCE-I11 cumulative tests: 290 passed.
- Engineering policy: 4/4 passed, 0 errors, 0 warnings.
- Boundary, schema, conformance, MQL5 static, and delivery checks: required.
- MetaEditor: pending local Windows compile; static validation is not reported as compilation.

## Primary documentation

Start at:

`docs/strategy_factory_universal_context_exploitation_engine/implementation_program/phase_deliveries/uce_i11/00_UCE_I11_DELIVERY_MOC.md`
