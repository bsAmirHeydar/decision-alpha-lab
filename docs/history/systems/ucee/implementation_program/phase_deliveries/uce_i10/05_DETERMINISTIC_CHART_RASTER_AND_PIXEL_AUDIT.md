---
title: "Deterministic Chart Raster and Pixel Audit"
tags: [strategy-factory, universal-context-engine, uce-i10, deep-views]
status: implemented
doc_version: 1.1.0
last_updated: 2026-07-13
---
# Deterministic Chart Raster and Pixel Audit

## Purpose

Convert OHLCV history into a reproducible tensor and prove that future candles cannot alter past pixels.

This chapter is normative for UCE-I10. Words such as **must**, **reject**, and **abstain** describe executable policy, not recommendations. A later phase may extend this surface only through a versioned contract and a recorded migration decision.

## Governing invariants

1. **Future rows are filtered before duplicate, order, and OHLC validation.**
2. **Channel order, dimensions, normalization, overlay policy, and augmentation policy are versioned.**
3. **The renderer emits fixed C×H×W arrays with canonical source and evidence hashes.**
4. **Pixel audits compare the complete payload and report changed-pixel count and maximum absolute difference.**

## Contract and implementation surface

- `wick, body, direction, volume, close, and range channels`
- `window min/max and last-close-range normalization`
- `left alignment of incomplete windows`
- `prefix-invariance reports`
- `deterministic raster convolution reference encoder`

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
| `auto-scaling based on future candles` | Reject or abstain; retain code and evidence; do not silently repair. |
| `malformed future rows poisoning a historical render` | Reject or abstain; retain code and evidence; do not silently repair. |
| `drawing discretionary overlays not represented in the contract` | Reject or abstain; retain code and evidence; do not silently repair. |
| `image augmentations that reverse time or alter label semantics` | Reject or abstain; retain code and evidence; do not silently repair. |

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

- [[06_VISION_ADAPTERS_AND_AUGMENTATION_RESTRICTIONS]]
- [[19_TEST_STRATEGY_GOLDEN_NEGATIVE_AND_CHAOS]]
- [[../../phases/UCE_I10_DEEP_MULTI_VIEW_GRAPH_AND_REGIME_PACK|Canonical UCE-I10 phase specification]]
- [[../../phases/UCE_I11_EXPERIMENT_DAG_SEARCH_AND_BUDGETING|UCE-I11 — Experiment DAG, Search, and Budgeting]]
