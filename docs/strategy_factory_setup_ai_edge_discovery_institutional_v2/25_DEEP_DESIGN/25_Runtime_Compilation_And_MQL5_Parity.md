---
title: Immutable Runtime Compilation, MQL5 Parity and Decision Reconciliation
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- deep-design
- core-production
---

# Objective

Compile a selected context-treatment-policy stack into one immutable runtime generation and prove source/export/MQL5 decision equivalence before any execution authority is considered.

## Capability tier

**Core Production**

# Non-negotiable principles

- Runtime consumes approved artifacts; it does not train, tune or discover.
- Feature order, preprocessing, model, calibration, policy, treatment, risk and fallback are hash-bound.
- Partial, incompatible, stale or unsigned bundles cannot activate.
- Prediction parity is insufficient; final bounded decision parity is required.
- Restart and rollback cannot duplicate decisions, reservations or orders.

# Reference architecture

- Bundle compiler resolves exact UCEE context, feature, model, policy, treatment, capital, portfolio and monitoring artifacts.
- Export adapters produce native deterministic representation and optional approved exchange formats.
- MQL5 mirror implements the same preprocessing, numerical policy, policy graph, fallback and trace semantics.
- Parity harness replays golden, boundary, missing, stale, extreme, OOD and broker-specification cases.
- Generation manager implements build, warm, validate, activate, retire, quarantine and rollback states.
- Decision journal and reservation journal support restart reconciliation and duplicate suppression.
- Live adapter remains physically and logically isolated behind I18 authorization.

# Algorithms and decision logic

- Canonicalize all manifests and derive generation identity from content hashes.
- Quantize or constrain numerical paths only after error and decision-boundary analysis.
- Compare intermediate feature/preprocessing/model/calibration outputs and final decision envelopes.
- Use tolerance bands for numeric outputs and exact equality for categorical decisions, support and vetoes.
- Inject corrupt, partial, reordered and incompatible artifacts to prove fail-closed activation.
- Replay after restart from journal checkpoints and verify one-shot decision entitlement.
- Run shadow reconciliation between expected and observed runtime traces.

# Canonical contracts

| Contract | Minimum semantics |
|---|---|
| `runtime_bundle` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `generation_manifest` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `parity_vector` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `parity_certificate` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `activation_record` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `decision_journal` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `rollback_record` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |

Every contract includes schema version, deterministic identity, upstream hashes, evidence class, known-time declaration where relevant, owner, compatibility range and explicit failure semantics.

# Data, role and lineage controls

1. Raw, canonical, feature, outcome, training, calibration, selection-validation, locked-final, prospective, shadow and live roles are distinct.
2. Human, model, agent, dashboard and report access to protected evidence is recorded in the exposure ledger.
3. Revisions create a new artifact and never rewrite decision-time evidence.
4. Cross-fold preprocessing, tokenization, graph construction, feature selection and model selection are prohibited.
5. Trial, candidate, failure, retry, prune, timeout and waiver records remain immutable.

# Measurement system

- Feature and preprocessing exact-hash parity.
- Prediction numerical error and boundary flips.
- Decision, treatment, risk and fallback agreement.
- Activation/rollback atomicity.
- Restart duplicate or omission count.
- Runtime latency, memory and error budget.

Metrics are segmented by time, symbol, context, regime, payoff profile, entry mechanism, broker/economics profile, support bucket and evidence class. Aggregates may not hide unstable subgroups.

# Adversarial failure table

| Class | Failure mechanism |
|---|---|
| Failure | Python and MQL5 agree on predictions but differ on policy fallback. |
| Failure | Bundle activates with one stale component. |
| Failure | Float conversion flips tight thresholds. |
| Failure | Restart replays an entitled signal twice. |
| Failure | Static source check is misreported as actual MetaEditor compile. |

# Authority boundary

- Research components propose and estimate; they cannot sign promotion.
- AI agents cannot alter context truth, data roles, protected evidence, risk limits, runtime generations or live authorizations.
- Policies remain bounded by UCEE I12 admission, I13 authority/fallback, I14 compilation, I17 risk/portfolio and I18 release qualification.
- Unsupported, stale, incomplete, OOD, mismatched or corrupt paths resolve to Manual, Skip, Abstain, Reject or Quarantine.

# Acceptance checklist

- [ ] Complete signed bundle is the only activation unit.
- [ ] Golden and adversarial parity vectors pass.
- [ ] No partial or incompatible bundle activates.
- [ ] Restart/rollback preserves decision identity and one-shot semantics.
- [ ] Actual MetaEditor evidence remains a distinct production gate.

# Required evidence packet

- Specification and assumption cards.
- Code, environment, data and artifact hashes.
- Positive, negative, boundary, mutation and adversarial tests.
- Baseline, ablation, stress, transport and reproducibility reports.
- Open limitations, kill criteria, downstream handoff and rollback path.

# Related architecture

- [[00_Home]]
- [[UCEE_I01_I18_Compatibility]]
- [[Anti_Overfit_Master_Protocol]]
- [[Promotion_Dossier_And_Signed_Admission]]
- [[Release_And_Production_Qualification]]
