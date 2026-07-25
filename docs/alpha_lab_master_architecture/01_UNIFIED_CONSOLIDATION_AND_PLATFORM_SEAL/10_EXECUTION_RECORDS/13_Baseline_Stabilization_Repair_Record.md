---
id: UCPS-UC01-REPAIR-6B21E4D9
title: "UC-01 Baseline Stabilization Repair Record"
type: repair_record
status: implemented_reference
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - consolidation
  - uc-01
  - baseline
  - repair
---
# UC-01 Baseline Stabilization Repair Record

## Purpose

The first complete Python syntax inventory discovered eleven pre-existing files whose newline string literals had been physically split across source lines. The files could not be parsed by Python and therefore prevented a trustworthy logic baseline. UC-01 repairs only those malformed literals so the repository can be inventoried and characterized without silently classifying executable logic as unreadable text.

## Preservation ordering

The governed operator sequence protects the pre-repair state before the repair-bearing commit is created:

1. create the immutable `pre-unified-consolidation` tag from the current `HEAD`;
2. create `archive/pre-unified-consolidation` from the same commit;
3. create and hash the Git bundle;
4. create and hash the materialized source archive;
5. run the isolated restore drill;
6. capture the post-repair executable baseline;
7. commit the UC-01 package and generated receipts.

The patch modifies no historical commit. Original malformed bytes remain recoverable through the tag, archive branch, bundle and source archive.

## Exact repair set

1. `lab/11_strategy_factory/python/saed_v4_anytime_valid_online_fdr/cli.py`
2. `lab/11_strategy_factory/python/saed_v4_complete_search_exposure_ledger/cli.py`
3. `lab/11_strategy_factory/python/saed_v4_decision_focused_treatment_selection/cli.py`
4. `lab/11_strategy_factory/python/saed_v4_foundation_model_adapters/cli.py`
5. `lab/11_strategy_factory/python/saed_v4_generative_path_stress_lab/cli.py`
6. `lab/11_strategy_factory/python/saed_v4_independent_multi_lab_replication/cli.py`
7. `lab/11_strategy_factory/python/saed_v4_mechanistic_interpretability/cli.py`
8. `lab/11_strategy_factory/python/saed_v4_multimodal_views/cli.py`
9. `lab/11_strategy_factory/python/saed_v4_offline_policy_research/cli.py`
10. `lab/11_strategy_factory/python/saed_v4_self_supervised_pretraining/serialization.py`
11. `tools/strategy_factory/generate_uce_i13_vectors.py`

## Permitted transformation

The only permitted transformation is replacing an invalid source-level line break inside a quoted newline literal with the valid escaped representation `\n`. The JSONL serializer additionally restores the intended `'\n'.join(...) + '\n'` expression.

No identifier, import, argument, control-flow branch, calculation, artifact path, authority field, trading rule or output schema is changed.

## Verification

- every declared repair path must parse with `ast.parse`;
- the patch manifest and artifact inventory must declare exactly these eleven files as `MODIFY`;
- all other patch paths must be `ADD`;
- deletion count must remain zero;
- the full Python inventory must contain zero parse blockers before UC-01 can be accepted;
- any additional modified pre-existing path invalidates the static patch.

## Claim ceiling

This repair record does not authorize semantic refactoring, modernization, formatting sweeps, package movement or consumer cutover. Any broader change belongs to a later UC stage and requires its own preservation and parity evidence.
