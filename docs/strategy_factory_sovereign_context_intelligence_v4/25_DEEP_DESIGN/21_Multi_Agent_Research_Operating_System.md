---
title: Multi-Agent Research Operating System and Authority Control
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- deep-design
- governed-challenger
---

# Objective

Use specialized AI agents to accelerate hypothesis generation, code synthesis, audit, documentation and evidence assembly while maintaining deterministic tools, human accountability and zero autonomous trading or promotion authority.

## Capability tier

**Governed Challenger**

# Non-negotiable principles

- Agents operate through typed task envelopes and least-privilege tools.
- No agent may alter raw truth, data roles, locked evidence, promotion decisions, risk limits or live runtime state.
- Agent outputs are proposals or evidence annotations until independently validated.
- Every tool call, source, patch, assumption and artifact hash is auditable.
- Agent disagreement is surfaced, not averaged away.

# Reference architecture

- Program Director Agent decomposes approved research charters into bounded work packages.
- Hypothesis Agent proposes falsifiable hypotheses linked to context ontology and research memory.
- Data/Leakage Sentinel validates known-time, lineage, folds and role access before training starts.
- Model Engineering Agent produces bounded implementations and manifests but cannot choose protected winners.
- Statistical Adversary, Causal Auditor and Execution Auditor independently challenge claims.
- Evidence Curator assembles dossiers from signed machine artifacts without rewriting results.
- Human research owner, model-risk committee and release authority remain separate accountable roles.

# Algorithms and decision logic

- Use plan–execute–verify loops with typed inputs, explicit stop conditions and artifact-level acceptance tests.
- Require two-agent or agent-plus-human review for code affecting data roles, labels, economics, risk or runtime handoff.
- Apply deterministic retrieval from approved research memory rather than unconstrained web synthesis for canonical claims.
- Sandbox generated code with network, file and credential restrictions; promote only reviewed diffs.
- Compute confidence from evidence completeness and independent verifier agreement, not linguistic certainty.
- Escalate conflicting conclusions to an adjudication task rather than allowing a coordinator to overwrite minority findings.
- Use signed run manifests so every agent process can be replayed or audited.

# Canonical contracts

| Contract | Minimum semantics |
|---|---|
| `agent_task_envelope` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `agent_capability_token` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `tool_policy` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `agent_run_manifest` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `review_record` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `disagreement_packet` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `agent_incident` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |

Every contract includes schema version, deterministic identity, upstream hashes, evidence class, known-time declaration where relevant, owner, compatibility range and explicit failure semantics.

# Data, role and lineage controls

1. Raw, canonical, feature, outcome, training, calibration, selection-validation, locked-final, prospective, shadow and live roles are distinct.
2. Human, model, agent, dashboard and report access to protected evidence is recorded in the exposure ledger.
3. Revisions create a new artifact and never rewrite decision-time evidence.
4. Cross-fold preprocessing, tokenization, graph construction, feature selection and model selection are prohibited.
5. Trial, candidate, failure, retry, prune, timeout and waiver records remain immutable.

# Measurement system

- Accepted artifact yield per agent-hour.
- Defect and leakage discovery rate by verifier.
- Human review burden and reversal rate.
- Proportion of outputs with complete source/artifact trace.
- Unauthorized action attempts and policy denials.
- Reproducibility of agent-generated patches and analyses.

Metrics are segmented by time, symbol, context, regime, payoff profile, entry mechanism, broker/economics profile, support bucket and evidence class. Aggregates may not hide unstable subgroups.

# Adversarial failure table

| Class | Failure mechanism |
|---|---|
| Failure | Coordinator agent accumulates de facto promotion authority. |
| Failure | Agents cite fabricated or unapproved evidence. |
| Failure | Generated code silently changes dataset semantics. |
| Failure | Agent memory contaminates locked evidence boundaries. |
| Failure | High agreement is mistaken for correctness. |

# Authority boundary

- Research components propose and estimate; they cannot sign promotion.
- AI agents cannot alter context truth, data roles, protected evidence, risk limits, runtime generations or live authorizations.
- Policies remain bounded by UCEE I12 admission, I13 authority/fallback, I14 compilation, I17 risk/portfolio and I18 release qualification.
- Unsupported, stale, incomplete, OOD, mismatched or corrupt paths resolve to Manual, Skip, Abstain, Reject or Quarantine.

# Acceptance checklist

- [ ] Capability tokens enforce least privilege.
- [ ] All agents are unable to place orders, sign promotion or modify risk.
- [ ] Generated artifacts require deterministic tests and independent review.
- [ ] Disagreements and failed tasks are retained.
- [ ] Agent shutdown cannot corrupt experiment or runtime state.

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
