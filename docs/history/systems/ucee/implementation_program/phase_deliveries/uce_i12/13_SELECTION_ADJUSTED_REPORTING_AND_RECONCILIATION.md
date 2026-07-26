---
title: "Selection-Adjusted Reporting and Reconciliation"
tags:
  - strategy-factory
  - universal-context-engine
  - uce-i12
  - statistical-governance
status: implemented_static_and_python_validated
doc_version: 1.0.0
last_updated: 2026-07-13
---
# Selection-Adjusted Reporting and Reconciliation

## Decision summary

- Winner metrics are shown beside multiplicity, PBO, deflation, null, and stress evidence.
- Declared versus tested versus missing counts are printed together.
- Manual overrides are never rewritten as ordinary selected trials.

## Why this document exists

UCE-I12 sits between broad experiment search and bounded policy composition. The upstream search layer deliberately exposes a large candidate universe. This document defines how that universe is converted into auditable evidence without deleting failures, retrofitting thresholds, or treating overlapping observations as independent. The rule is fail-closed: an omitted identity, missing report, invalid signature, or critical blocker is evidence against promotion.

## Immutable inputs

- UCE-I11 experiment manifest and complete trial identities.
- Hash-chained selection ledger containing every outcome and manual intervention.
- Dataset, split, target, economics, known-time, candidate, trainer, treatment, threshold, fold, and seed identities.
- Out-of-fold or locked-confirmatory predictions and path-level economic outcomes.
- Versioned UCE-I12 policy, family definition, seed policy, bootstrap policy, null plan, stress plan, calibration plan, and prospective challenge freeze.

## Machine-readable outputs

- Canonical JSON artifacts with closed schemas and SHA-256 identity.
- One or more `TestEvidence` records with status, severity, metric, threshold, blockers, warnings, and details.
- Artifact hashes included in the signed evidence bundle.
- Explicit downstream disposition: reject, challenge, or promote.

## Core invariants

1. **Complete-universe invariant:** failed and untested choices still count in multiplicity.
2. **Known-time invariant:** no later observation may alter an earlier evidence artifact.
3. **Non-compensation invariant:** critical blockers cannot be averaged away by score.
4. **Determinism invariant:** fixed inputs, policy, seed, and versions produce identical identities and results.
5. **Baseline invariant:** manual and matched null comparisons remain visible beside model performance.
6. **Prospective invariant:** challenge rules are frozen before challenge observations.
7. **Authority invariant:** promotion evidence grants no order, broker, position, or network authority.

## Processing contract

```text
immutable UCE-I11 manifest + complete ledger
                    │
          selection-universe reconciliation
                    │
   ┌────────────────┼────────────────┐
 uncertainty   multiplicity   winner-overfit
   │                │                │
 null controls ─ stress ─ calibration/decision quality
                    │
          non-compensatory scorecard
                    │
        signed reject/challenge/promote bundle
```

The implementation validates identity before numerical work. Numerical output generated from an unreconciled universe is invalid even when the calculations themselves are arithmetically correct.

## Failure matrix

| Failure | Detection | Required disposition |
|---|---|---|
| Manifest, ledger, and universe counts differ | reconciliation report | reject |
| Missing p-value hidden from family size | multiplicity count equation | reject |
| Inner/outer observation overlap | nested-selection audit | reject |
| Critical leakage or integrity test fails | scorecard critical veto | reject |
| Mandatory null absent or failed | null-coverage audit | reject |
| Stress retention below policy | stress aggregate | reject |
| Calibration warning without critical failure | calibration thresholds | challenge |
| Prospective rule frozen after observations | freeze contract | reject |
| Evidence hash or signature mismatch | bundle verification | reject/quarantine |
| MetaEditor not run locally | compile evidence absent | pending local gate, never reported as pass |

## Executable test obligations

- Repeat the same seeded procedure and compare exact output and evidence hash.
- Mutate one behavior-bearing policy field and verify identity changes.
- Delete one failed or skipped trial and verify universe construction fails.
- Inject one overlap between inner and outer observations and verify rejection.
- Tamper with one evidence artifact and verify bundle signature/integrity failure.
- Make every aggregate metric excellent while retaining one critical blocker; outcome must remain reject.
- Verify MQL5 files contain no execution or network authority tokens.

## Operator runbook

1. Freeze the policy, family definition, null plan, stress plan, calibration plan, and challenge declaration.
2. Verify UCE-I11 manifest and ledger chain.
3. Build and reconcile the complete selection universe.
4. Run uncertainty and subgroup reporting before significance claims.
5. Apply multiplicity to the declared family universe, including missing p-values.
6. Execute winner-overfit, null, stress, and calibration suites.
7. Inspect critical blockers before reading the weighted score.
8. Build, sign, verify, and archive the evidence bundle.
9. Record reject, challenge, or promote without editing previous artifacts.
10. Hand only immutable hashes and explicit residual risks to UCE-I13.

## Evidence retained

- Input identity hashes and package versions.
- Seeds, iterations, block size, cluster identity, and effective sample size.
- Family counts, tested counts, missing counts, adjusted p-values, and rejected identities.
- PBO combinations, deflation trial count, reality-check and SPA distributions.
- Null and stress plans with each result, including failures.
- Calibration bins, coverage, threshold utility, abstention, and risk-tier reports.
- Scorecard components, critical blockers, challenges, residual risks, and signature verification.

## Code surfaces

- `strategy_factory_promotion_v3/contracts.py`
- `strategy_factory_promotion_v3/winner_overfit.py`
- `lab/11_strategy_factory/schemas/v3/promotion_*.schema.json`
- `mql5/Include/AlphaLab/StrategyFactory/StatisticalPromotion/`
- `lab/11_strategy_factory/tests/phase_uce_i12_promotion/`

## Residual risk

Passing this contract demonstrates reproducible statistical governance on the supplied evidence. It does not prove future profitability, eliminate distribution shift, establish unlimited capacity, or authorize live execution. Those claims require prospective evidence and downstream production qualification.

## Navigation

- [[00_UCE_I12_DELIVERY_MOC|UCE-I12 delivery MOC]]
- [[../../phases/UCE_I12_STATISTICAL_AND_ANTI_OVERFIT_PROMOTION_GATE|Canonical phase specification]]
- [[../../phases/UCE_I13_MANUAL_AI_HYBRID_POLICY_GRAPH|Next phase: UCE-I13]]
