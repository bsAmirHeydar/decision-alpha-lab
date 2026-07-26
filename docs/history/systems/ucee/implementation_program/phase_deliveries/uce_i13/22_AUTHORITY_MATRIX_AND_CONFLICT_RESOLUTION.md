---
title: "Authority Matrix and Conflict Resolution"
tags: [strategy-factory, universal-context-engine, uce-i13, policy-graph]
status: implemented_static_and_python_validated
doc_version: 1.0.0
last_updated: 2026-07-13
---
# Authority Matrix and Conflict Resolution

## Decision summary

Order kill switch, risk engine, human operator, manual policy, treatment compiler, model, portfolio engine, and system.

The implementation is deliberately bounded. A model may filter, rank, choose among supported treatments, choose among supported risk tiers, or abstain. It may not manufacture a context occurrence, invent an action, widen support, suppress a hard veto, or convert a research promotion into live execution authority.

## Scope and ownership

- This chapter owns **Authority Matrix and Conflict Resolution** and treats its behavior-bearing fields as versioned identity.
- The primary operational objective is: Order kill switch, risk engine, human operator, manual policy, treatment compiler, model, portfolio engine, and system.
- A consumer may not infer omitted semantics from prose, filenames, defaults, or historical behavior.
- A failed, rejected, abstained, or overridden decision remains in the evidence trail.

## Contract identities

| Identity | Meaning |
|---|---|
| `manual_policy_hash` | Pinned setup eligibility, treatment, risk, exception, and veto identity. |
| `admission_hash` | Signed UCE-I12 model promotion and capability support identity. |
| `graph_hash` | Canonical DAG nodes, configuration, dependencies, support, and output identity. |
| `known_time_ms` | Latest time at which all consumed information was knowable. |
| `decision_hash` | Canonical decision state plus node-trace tail identity. |

## Core invariants

1. No policy node creates a context occurrence; it consumes a pre-existing occurrence identity.
2. AI nodes operate only when the UCE-I12 outcome is signed, valid, unexpired, and explicitly `promote`.
3. The legal action, treatment, risk, and context sets are intersections of declared supports, never inferred unions.
4. Known-time and feature-time identities are immutable inputs to every decision and replay artifact.
5. Kill-switch, risk rejection, and hard vetoes are non-compensatory and cannot be averaged away by confidence.
6. Every invalid model path has a deterministic fallback and an auditable reason code.
7. Manual-only remains a first-class executable baseline and is not reconstructed from model behavior.
8. This phase has no broker, order, position, live-network, or external execution authority.

## Processing model

```text
pinned manual policy + immutable context occurrence
                         │
             manual eligibility/treatment/veto
                         │
signed promoted model ──┼── validity/support/uncertainty audit
                         │
               bounded policy DAG nodes
                         │
      kill/risk/operator/manual authority resolution
                         │
           approve / reject / abstain / pending
                         │
          hash-chained trace + paired attribution
```

## Failure matrix

| Failure | Detection | Required disposition |
|---|---|---|
| Missing or mismatched identity | Contract validation before graph execution | Reject or manual-only fallback; never guess |
| Stale, OOD, low-confidence, or missing-view model output | Model-output validator | Apply the frozen fallback rule and log the exact reason |
| Cycle, unreachable node, unknown config, or wrong authority | DAG compiler | Refuse graph compilation |
| Unsupported action, treatment, risk tier, or context | Support intersection audit | Abstain or reject according to the frozen fallback policy |
| Kill switch, risk rejection, or hard veto | Authority resolver | Immediate reject by the highest authority |
| Trace hash mismatch or replay divergence | Evidence verification | Quarantine the artifact and block handoff |

## Executable evidence obligations

- Repeat the same immutable inputs and compare canonical JSON, decision hash, and trace tail exactly.
- Mutate one behavior-bearing field and verify the owning artifact identity changes.
- Inject a future timestamp or stale validity horizon and verify model authority is withheld.
- Attempt to expand support beyond signed admission and verify compilation or execution fails closed.
- Set every model score high while engaging a hard veto and verify rejection remains unchanged.
- Tamper with one trace entry and verify chain validation fails.
- Replay the same occurrences in a different input order and verify known-time ordering produces the same replay hash.

## Operator runbook

1. Load and verify the pinned manual policy, fallback policy, authority matrix, and signed promotion admission.
2. Validate schemas, semantic versions, SHA-256 identities, known-time fields, and support declarations.
3. Compile the graph and review the deterministic topological order and authority assigned to every node.
4. Run manual-only parity before enabling any AI node.
5. Run golden, negative, stale, OOD, missing-view, conflict, timeout, and replay conformance tests.
6. Archive the compiled graph identity, conformance vector hash, limitations, and rollback target.
7. Enable only the declared mode; do not substitute a broader hybrid graph for a narrower approved mode.
8. On incident, quarantine the graph and revert to the exact pinned manual-only generation.

## Telemetry and retained evidence

- Graph, manual-policy, fallback-policy, authority-matrix, admission, occurrence, and model-output hashes.
- Node sequence, node kind, authority, status transition, support choice, fallback reason, and previous trace hash.
- Manual-only and hybrid decision pairs on the same opportunity universe.
- Abstention, fallback, hard-veto, stale-output, OOD, missing-view, and operator-override counters.
- Exact build version, Python package version, schema IDs, conformance-vector hash, and MQL5 static-validation result.
- Residual risks, unresolved local MetaEditor gate, migration impact, and rollback generation.

## Non-completion conditions

- Manual-only semantics differ from the pinned setup definition.
- AI creates or broadens a context, action, treatment, or risk tier.
- An invalid model path lacks a deterministic fallback.
- Authority conflict is resolved by implicit call order rather than an explicit matrix.
- A human override has no identity, reason, time bound, or evidence hash.
- Incremental value is reported without the manual baseline on paired opportunities.
- Static MQL5 checks are described as a successful MetaEditor compilation.

## Residual risk

The golden fixtures prove contract closure, determinism, parity, and fail-closed behavior on supplied data. They do not establish future profitability, operational latency, portfolio capacity, production key custody, ONNX parity, or live MetaTrader safety. Those claims remain downstream.

## Related implementation surfaces

- `lab/11_strategy_factory/python/strategy_factory_policy_v3/`
- `lab/11_strategy_factory/schemas/v3/policy_*.schema.json`
- `lab/11_strategy_factory/tests/phase_uce_i13_policy_graph/`
- `mql5/Include/AlphaLab/StrategyFactory/HybridPolicy/`
- `lab/11_strategy_factory/test_vectors/v3/uce_i13_policy_conformance_vectors.json`

## Navigation

- [[00_UCE_I13_DELIVERY_MOC|UCE-I13 Delivery MOC]]
- [[../../phases/UCE_I13_MANUAL_AI_HYBRID_POLICY_GRAPH|Canonical UCE-I13 phase]]
- [[../../phases/UCE_I14_RUNTIME_COMPILATION_ONNX_AND_MQL5_PARITY|Next phase: UCE-I14]]
