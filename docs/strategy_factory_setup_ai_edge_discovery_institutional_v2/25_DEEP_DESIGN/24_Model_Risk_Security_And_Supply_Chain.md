---
title: Model Risk, Security and AI Supply-Chain Governance
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

Protect the research and runtime ecosystem against compromised data, code, dependencies, models, agents, credentials and artifacts while formalizing model-risk ownership and revocation.

## Capability tier

**Core Production**

# Non-negotiable principles

- Every executable, model and dataset is untrusted until verified and admitted.
- Security controls are independent from statistical performance.
- External foundation models and checkpoints are research inputs, not privileged truth.
- Least privilege, signed artifacts, short-lived authorization and revocation are mandatory.
- Model limitations, support and failure modes are governed throughout the lifecycle.

# Reference architecture

- Supply-chain intake scans source, license, SBOM, signatures, unsafe serialization and provenance.
- Model-risk registry stores owner, purpose, support, validation, tier, dependencies and open findings.
- Artifact admission service verifies content hashes, signatures, compatibility and authorization.
- Secret broker issues scoped short-lived credentials; no secrets are embedded in datasets, notebooks or agents.
- Runtime allowlists bind generation, account, broker, symbol, context, model and operator.
- Incident response supports quarantine, revocation, rollback, forensic preservation and customer/account scoping.
- Independent governance committees approve exceptions with expiry and compensating controls.

# Algorithms and decision logic

- Generate and verify SBOMs for containers, Python, native and MQL5 dependencies.
- Use safe model serialization formats or isolated loaders for untrusted checkpoints.
- Scan training and evaluation data for poisoning signatures, abnormal provenance and label manipulation.
- Perform adversarial model extraction, prompt/tool injection and agent privilege tests where applicable.
- Bind every promoted artifact to exact upstream hashes and an admission signature.
- Continuously reconcile active runtime generations against allowlists and revocation lists.
- Run periodic disaster recovery and compromise simulations.

# Canonical contracts

| Contract | Minimum semantics |
|---|---|
| `model_risk_scorecard` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `sbom_manifest` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `artifact_admission` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `security_scan_report` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `authorization_token` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `revocation_record` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `security_incident` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |

Every contract includes schema version, deterministic identity, upstream hashes, evidence class, known-time declaration where relevant, owner, compatibility range and explicit failure semantics.

# Data, role and lineage controls

1. Raw, canonical, feature, outcome, training, calibration, selection-validation, locked-final, prospective, shadow and live roles are distinct.
2. Human, model, agent, dashboard and report access to protected evidence is recorded in the exposure ledger.
3. Revisions create a new artifact and never rewrite decision-time evidence.
4. Cross-fold preprocessing, tokenization, graph construction, feature selection and model selection are prohibited.
5. Trial, candidate, failure, retry, prune, timeout and waiver records remain immutable.

# Measurement system

- Unsigned/unverified artifact rejection rate.
- Open model-risk findings by severity and age.
- Time to revoke and rollback compromised generations.
- Supply-chain vulnerability exposure and patch latency.
- Privilege-denial events and anomalous agent/tool activity.
- Recovery-point and recovery-time performance.

Metrics are segmented by time, symbol, context, regime, payoff profile, entry mechanism, broker/economics profile, support bucket and evidence class. Aggregates may not hide unstable subgroups.

# Adversarial failure table

| Class | Failure mechanism |
|---|---|
| Failure | A high-performing external checkpoint bypasses intake. |
| Failure | Unsafe serialization executes code during loading. |
| Failure | Agent credentials exceed task scope. |
| Failure | Revocation exists in policy but not in runtime enforcement. |
| Failure | Model-risk findings are closed by the model owner alone. |

# Authority boundary

- Research components propose and estimate; they cannot sign promotion.
- AI agents cannot alter context truth, data roles, protected evidence, risk limits, runtime generations or live authorizations.
- Policies remain bounded by UCEE I12 admission, I13 authority/fallback, I14 compilation, I17 risk/portfolio and I18 release qualification.
- Unsupported, stale, incomplete, OOD, mismatched or corrupt paths resolve to Manual, Skip, Abstain, Reject or Quarantine.

# Acceptance checklist

- [ ] All dependencies and artifacts have provenance/SBOM/signature.
- [ ] No external model enters production directly.
- [ ] Revocation and rollback are tested end to end.
- [ ] Critical findings block admission independent of performance.
- [ ] Secrets and authorizations are scoped, expiring and audited.

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
