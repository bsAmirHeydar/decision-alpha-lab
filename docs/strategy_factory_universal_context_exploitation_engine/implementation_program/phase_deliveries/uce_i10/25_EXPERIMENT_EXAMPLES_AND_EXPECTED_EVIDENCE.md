---
title: "Experiment Examples and Expected Evidence"
tags: [strategy-factory, universal-context-engine, uce-i10, deep-views]
status: implemented
doc_version: 1.1.0
last_updated: 2026-07-13
---
# Experiment Examples and Expected Evidence

## Purpose

Show how a compliant sequence, raster, graph, regime, and fusion experiment should be assembled and reviewed.

This chapter is normative for UCE-I10. Words such as **must**, **reject**, and **abstain** describe executable policy, not recommendations. A later phase may extend this surface only through a versioned contract and a recorded migration decision.

## Governing invariants

1. **The example begins with dataset and admission evidence, not model selection.**
2. **All base predictions used by stacking are OOF.**
3. **Seed runs share folds, target contract, economics, and evaluation protocol.**
4. **Final-test data remains sealed until the selected candidate and thresholds are frozen.**

## Contract and implementation surface

- `sequence-only challenger`
- `raster ablation`
- `graph topology ablation`
- `regime/global routing analysis`
- `late versus gated versus stacked fusion comparison`

The implementation is split deliberately: immutable dataclasses and JSON schemas define meaning; deterministic builders and native baselines define executable reference behavior; optional adapters declare capabilities without contaminating the base package; qualification and handoff artifacts decide whether downstream orchestration may schedule the candidate.

## Processing sequence

1. Resolve the exact dataset manifest, split/fold identity, context observation, and known-time cut.
2. Validate the phase entry gate and refuse work when required evidence is absent or rejected.
3. Construct the representation from permitted rows only and serialize all behavior-changing configuration.
4. Produce canonical SHA-256 identity for source material, contract, artifact, and evidence.
5. Run deterministic replay and relevant causality/failure tests before fitting a candidate.
6. Fit only through the declared Trainer SDK capability or documented adapter boundary.
7. Evaluate OOF behavior, economics, calibration, stability, ablations, export parity, and latency.
8. Emit a promotable, challenger-only, or rejected decision with named blockers and warnings.

## Evidence requirements

| Evidence | Minimum content | Failure behavior |
|---|---|---|
| Dataset identity | manifest hash/ID, row set, fold and known-time semantics | reject |
| Contract identity | version, closed fields, enum domain, canonical hash | reject |
| Causality | known-time audit and future-perturbation result | reject |
| Determinism | repeated-run hashes and seed/resource configuration | reject or challenger-only per policy |
| Model evaluation | OOF metric, economic utility, calibration and support | reject |
| Complexity proof | classical baseline and required ablations | reject |
| Runtime proof | export path, parity error, latency, fallback | reject promotion |
| Governance | inventory, file hashes, QA result, limitations and handoff | incomplete phase |

## Failure matrix

| Condition | Required response |
|---|---|
| `comparing candidates on different row sets` | Reject or abstain; retain code and evidence; do not silently repair. |
| `changing thresholds after seeing final-test results` | Reject or abstain; retain code and evidence; do not silently repair. |
| `using one lucky seed as the experiment summary` | Reject or abstain; retain code and evidence; do not silently repair. |
| `failing to retain rejected candidates` | Reject or abstain; retain code and evidence; do not silently repair. |

## Observability and review

Reviewers must be able to answer five questions from artifacts alone: what data was knowable, what exact representation was built, which implementation/version ran, what evidence qualified or rejected it, and what downstream authority was granted. Logs or dashboards may summarize these facts but may not replace the canonical artifacts.

## Test obligations

- Golden identity test for deterministic output.
- Negative contract test for missing, malformed, stale, reordered, or incompatible input.
- Future-perturbation test where relevant.
- Repeated-run deterministic replay.
- Differential comparison with the accepted classical/native baseline.
- Failure-path test proving rejected evidence cannot be bypassed.
- Schema closure and canonical serialization test.
- Boundary test proving no order/execution authority entered I10.

## Operational checklist

- [ ] Exact repository revision recorded.
- [ ] Entry evidence exists and is accepted or explicitly WARN.
- [ ] No final-test row was consumed during fitting, selection, fusion, calibration, or thresholding.
- [ ] All identity-bearing parameters are serialized.
- [ ] Required tests and validators ran with retained exit codes.
- [ ] MetaEditor compile status is reported truthfully as passed, failed, or pending-local-Windows.
- [ ] Residual risks and rollback path are present in the handoff.

## Non-goals

This chapter does not authorize live execution, broker connectivity, discretionary overrides, or post-hoc removal of rejected evidence. It also does not establish trading alpha by itself; it establishes a reproducible engineering and scientific surface on which alpha claims can later be tested.

## Related notes

- [[00_UCE_I10_DELIVERY_MOC]]
- [[22_ACCEPTANCE_EVIDENCE]]
- [[../../phases/UCE_I10_DEEP_MULTI_VIEW_GRAPH_AND_REGIME_PACK|Canonical UCE-I10 phase specification]]
- [[../../phases/UCE_I11_EXPERIMENT_DAG_SEARCH_AND_BUDGETING|UCE-I11 — Experiment DAG, Search, and Budgeting]]
