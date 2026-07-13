---
id: SAED-2AC4C2CC98
title: "UCEE Compatibility and Contract Map"
type: architecture
status: canonical
domain: strategy-factory-setup-ai-edge-discovery
version: 1.0.0
created: 2026-07-13
updated: 2026-07-13
tags:
  - strategy-factory
  - setup-factory
  - ai-training
  - compatibility
  - contracts
---

# UCEE Compatibility and Contract Map

## Principle

No new central semantics are introduced where UCEE already owns a contract. This module adds registries, templates and orchestration profiles that serialize into existing V3 schemas.

## Contract Crosswalk

| Setup AI concept | Existing schema / package |
|---|---|
| Context occurrence | `context_observation.schema.json`, `policy_context_occurrence.schema.json` |
| Context package freeze | `context_package_manifest.schema.json`, `tournament_context_package_freeze.schema.json` |
| Treatment atom | `treatment_atom_descriptor.schema.json` |
| Compatibility edge | `treatment_atom_compatibility.schema.json` |
| Candidate draft | `treatment_draft.schema.json` |
| Complete bundle | `compiled_treatment.schema.json` |
| Treatment sibling | `treatment_sibling.schema.json` |
| Dataset row | `dataset_row.schema.json` |
| Dataset manifest | `dataset_manifest.schema.json` |
| Trainer capability/config | `trainer_capability_descriptor.schema.json`, `trainer_config.schema.json` |
| Treatment-choice output | `treatment_choice_prediction.schema.json` |
| Quantile/survival/regime output | V3 prediction schemas and `strategy_factory_trainers_v3` |
| Experiment declaration | `experiment_declaration.schema.json` |
| Search plan and trial identity | `experiment_search_plan.schema.json`, `experiment_trial_identity.schema.json` |
| Selection ledger | `experiment_selection_ledger_entry.schema.json` |
| Promotion universe | `promotion_selection_universe.schema.json` |
| Anti-overfit reports | `promotion_*_report.schema.json` |
| Manual baseline | `policy_manual_definition.schema.json` |
| AI output | `policy_model_output.schema.json` |
| Hybrid graph | `policy_graph_spec.schema.json`, `policy_compiled_graph.schema.json` |
| Abstention/fallback | `policy_abstention_event.schema.json`, `policy_fallback_policy.schema.json` |
| Runtime | `runtime_bundle_manifest.schema.json`, `runtime_preprocessing_contract.schema.json` |
| Portfolio handoff | `portfolio_opportunity_candidate.schema.json` |
| Production evidence | `production_evidence_bundle.schema.json` |

## Package Crosswalk

- Context: `strategy_factory_contracts_v3`
- Treatments: `strategy_factory_treatments_v3`, `strategy_factory_treatment_compiler_v3`
- Economics: `strategy_factory_economics_v3`
- Outcome/Dataset: `strategy_factory_dataset_v3`
- Trainers: `strategy_factory_trainers_v3`
- Deep/multi-view: `strategy_factory_deep_views_v3`
- Experiments: `strategy_factory_experiments_v3`
- Promotion: `strategy_factory_promotion_v3`
- Policies: `strategy_factory_policy_v3`
- Runtime: `strategy_factory_runtime_v3`
- Tournament: `strategy_factory_tournament_v3`
- Onboarding: `strategy_factory_onboarding_v3`
- Portfolio: `strategy_factory_portfolio_v3`
- Production: `strategy_factory_production_v3`

## Compatibility Rules

1. New registries may add declarative values but cannot reinterpret existing fields.
2. Every behavior-changing parameter is included in identity and canonical serialization.
3. Dataset and runtime preprocessing are one artifact, not parallel implementations.
4. Python and MQL5 consume the same frozen feature order, thresholds and fallback policy.
5. Any necessary UCEE core change requires an ADR, compatibility test and migration plan.
