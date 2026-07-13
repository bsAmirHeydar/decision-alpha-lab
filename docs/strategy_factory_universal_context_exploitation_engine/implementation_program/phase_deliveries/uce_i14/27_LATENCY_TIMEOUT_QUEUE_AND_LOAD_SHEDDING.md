---
title: "Latency, Timeout, Queue, and Load Shedding"
tags: [strategy-factory, universal-context-engine, uce-i14, immutable-runtime]
status: implemented_static_and_python_validated
doc_version: 1.0.0
last_updated: 2026-07-13
---
# Latency, Timeout, Queue, and Load Shedding

## Decision summary

Define latency budgets, timeout dispositions, queue pressure handling, and non-blocking fallback.

UCE-I14 converts the exact accepted UCE-I13 generation into one closed runtime artifact set. It does not create a new context, alter treatment doctrine, reinterpret risk, or grant live order authority. The output is an immutable, signed, parity-certified generation that can be warmed, validated, atomically activated, retired, quarantined, and rolled back.

## Scope and ownership

- The chapter owner is `27_LATENCY_TIMEOUT_QUEUE_AND_LOAD_SHEDDING`; downstream consumers must cite its artifact identities rather than reconstruct behavior from prose.
- The operational objective is: Define latency budgets, timeout dispositions, queue pressure handling, and non-blocking fallback.
- Acceptance requires executable evidence, not a document-only assertion.
- Rejected, failed, duplicate, stale, and quarantined attempts remain in the evidence trail.

## Contract identities

| Identity | Bound behavior |
|---|---|
| `bundle_hash` | Complete unsigned manifest, exact component roles, ordered features, model/export/policy identities, modes, monitoring, rollback, and limitations. |
| `preprocessing_hash` | Feature order, missingness, clipping, scaling, category vocabulary, output expansion, and precision. |
| `model_hash` | Model kind, ordered inputs/outputs, weights, bias, precision, and registered metadata. |
| `export_hash` | Export format, model identity, artifact bytes, tensor names, precision, opset, warnings, and unsupported operators. |
| `parity_certificate_hash` | Vector universe, tolerances, source/export/MQL5 observations, decisions, runtime versions, and status. |
| `decision_hash` | Semantic decision fields and trace; excludes latency and completion time. |
| `activation_receipt_hash` | Activated bundle, generation, previous bundle, activation time, state, and idempotency key. |

## Core invariants

1. Every behavior-changing field is present in canonical serialization and therefore changes an owning SHA-256 identity.
2. Known-time data may influence only decisions at or after its declared availability; future suffixes cannot rewrite a past decision identity.
3. A partial, mismatched, unsigned, unqualified, or parity-failing bundle is not activatable.
4. The runtime may abstain, reject, quarantine, or fall back; it may not guess missing semantics.
5. No generic I14 package or MQL5 include owns broker, order, position, or live-network authority.
6. Operational timing is retained as telemetry but is excluded from the semantic decision hash so restart replay remains deterministic.

## Processing model

```text
signed I13 policy generation + exact feature/preprocessing/model artifacts
                              │
                   closed component inventory
                              │
             approved native export / qualified ONNX adapter
                              │
       source ↔ export ↔ MQL5 preprocessing/inference parity
                              │
          failure qualification + signature verification
                              │
          built → warmed → validated → active generation
                              │
        bounded decision host + journal + telemetry + rollback
```

## Required inputs

- Signed UCE-I12 promotion admission and the exact UCE-I13 compiled graph.
- Pinned manual policy, fallback policy, authority matrix, and support declarations.
- Ordered feature schema and preprocessing contract including missingness and precision.
- Model artifact, output labels, calibration identity, treatment/risk registries, and economic boundary.
- Monitoring policy, latency policy, rollback target, conformance vectors, and residual-risk declaration.

## Required outputs

- Canonical JSON or dataclass artifact whose public fields are schema-validated.
- Stable SHA-256 identity and explicit semantic version.
- Golden and negative fixtures that demonstrate both acceptance and refusal behavior.
- Test evidence, retained telemetry fields, limitations, rollback instructions, and handoff identity.

## Failure matrix

| Failure | Detection | Mandatory disposition | Evidence |
|---|---|---|---|
| Missing required component | Bundle-role closure before warm-up | Refuse build or activation | Missing roles and expected manifest hash |
| Feature order or preprocessing mismatch | Hash and ordered-name comparison | Refuse activation | Expected/actual order and hashes |
| Corrupt or substituted model/export | Byte and semantic hash validation | Quarantine bundle | Artifact role, expected hash, actual hash |
| Unsupported operator or unavailable ONNX runtime | Capability registry/probe | Use only approved native path or reject | Probe, adapter name, warnings |
| Numeric or decision parity failure | Cross-language vector execution | Reject certificate and activation | Per-vector outputs, error, labels, tolerance |
| Invalid signature | HMAC/signature verifier | Refuse activation | Key ID and verification result; never secret material |
| Stale context, timeout, queue pressure | Runtime gate and telemetry | Abstain, shed load, or fail closed | Reason code and timing |
| Restart journal divergence | Snapshot reconciliation | Block activation and quarantine | Journal tail and active pointer evidence |
| Kill switch | Highest non-compensatory authority | Immediate reject | Decision reason and authority trace |

## Executable evidence obligations

1. Repeat the same canonical inputs and compare all owning hashes exactly.
2. Mutate one behavior-bearing field and verify the corresponding identity changes.
3. Remove one required component and verify the bundle cannot validate or activate.
4. Reorder features or outputs and verify cross-language preprocessing/model binding fails.
5. Corrupt export bytes and verify the loader refuses them before inference.
6. Run golden, edge, missing, extreme, OOD, and batch vectors through all available paths.
7. Engage a hard kill switch while scores are favorable and verify rejection remains unchanged.
8. Restore a journal after restart and verify no duplicate semantic decision is created.
9. Attempt live mode without an isolated authorized adapter and verify refusal.
10. Preserve failed and rejected evidence in the release inventory.

## Test families

| Family | Minimum proof |
|---|---|
| Contract | Closed schemas, semantic versions, SHA-256 patterns, canonical serialization, explicit migration/rejection. |
| Causality | Known-time ordering, stale context refusal, prefix stability, future-suffix invariance. |
| Determinism | Repeated hash equality, stable tie-breaks, restart replay, idempotent activation. |
| Differential | Source vs exported native vs MQL5 mirror outputs and exact labels. |
| Failure | Partial bundle, corrupt export, wrong signature, unsupported mode/operator, timeout, queue, restart, kill switch. |
| Boundary | No broker/network imports or OrderSend calls in generic runtime surfaces. |
| Governance | Manifest, hashes, QA, limitations, local MetaEditor status, rollback, I15 handoff. |

## Operator runbook

1. Verify all I13 admission and policy dependency hashes.
2. Generate preprocessing output names and confirm exact equality with model input names.
3. Export using an audited adapter; record dependency availability and warnings.
4. Build the closed runtime bundle and sign its unsigned canonical payload.
5. Execute parity vectors and require a PASS certificate.
6. Run failure qualification; critical findings block validation.
7. Warm the generation without changing the active pointer.
8. Validate signature, hashes, parity, failure report, journal snapshot, and rollback target.
9. Activate with an idempotency key; retire the prior complete generation atomically.
10. Observe telemetry; quarantine and roll back on critical incident.

## Telemetry and retained evidence

- Bundle/component/preprocessing/model/export/policy/parity/failure/activation identities.
- Generation state transitions and previous/active/rollback pointers.
- Request, occurrence, known-time, semantic decision hash, trace hash, and duplicate status.
- Preprocessing/inference/total latency and timeout/queue counters.
- Mode, live-adapter authorization state, abstention, rejection, kill-switch, and fallback reasons.
- ONNX dependency probe and approved-native adapter version.
- Static MQL5 validation, local MetaEditor result, limitations, and unresolved residual risks.

## Non-completion conditions

- Any required behavior is absent from identity or schema.
- Source, exported, and MQL5 paths use different feature or preprocessing semantics.
- A partial or mismatched bundle can become active.
- Numeric error exceeds tolerance or labels diverge on a required vector.
- Runtime decision carries order authority outside an isolated adapter.
- Restart or rollback can duplicate a semantic decision.
- Static checks are represented as successful MetaEditor compilation.

## Residual risk

Synthetic fixtures establish contract closure, deterministic behavior, fail-closed operation, and reference-path parity. They do not establish market edge, broker-fill realism, production key custody, operating-system crash atomicity, project-specific ONNX conversion, or real MetaTrader compilation. These remain explicit downstream qualifications.

## Implementation surfaces

- `lab/11_strategy_factory/python/strategy_factory_runtime_v3/`
- `lab/11_strategy_factory/schemas/v3/runtime_*.schema.json`
- `lab/11_strategy_factory/examples/uce_i14/`
- `lab/11_strategy_factory/tests/phase_uce_i14_runtime_compilation/`
- `mql5/Include/AlphaLab/StrategyFactory/ImmutableRuntime/`
- `tools/strategy_factory/*uce_i14*`

## Navigation

- [[00_UCE_I14_DELIVERY_MOC|UCE-I14 Delivery MOC]]
- [[../../phases/UCE_I14_RUNTIME_COMPILATION_ONNX_AND_MQL5_PARITY|Canonical UCE-I14 phase]]
- [[../../phases/UCE_I15_FIRST_REAL_CONTEXT_TOURNAMENT|Next phase: UCE-I15]]
