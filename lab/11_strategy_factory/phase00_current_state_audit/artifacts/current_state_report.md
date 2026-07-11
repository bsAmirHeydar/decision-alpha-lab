# Strategy Factory Phase 00 — Current-State Report

## Audit identity

- Generated at: `2026-07-11T06:46:18.064489+00:00`
- Git commit: `8a5472e6d5113386263a6665159c45e0d68c5876`
- Repository root label: `decision-alpha-lab`
- Audit status: **ACCEPTED_WITH_DEFERRED_REMEDIATIONS**

## Executive conclusion

The audited repository is a compact research foundation, not yet a Strategy Factory implementation. It contains a functional MT5-to-Parquet market-data path, a reusable L-rule structural-node detector, and one revisit-aware structural metric. The later EXP0017, NDS, Daye, model-training, execution, and portfolio systems referenced by the implementation roadmap are not present in this uploaded snapshot.

The correct migration strategy is therefore **preserve and wrap the implemented anatomy/data primitives, replace empty scaffolding with shared factory modules, consolidate persistence, and freeze canonical contracts before expanding behavior**.

## Inventory

- Files audited: **103**
- Empty files: **54**
- Python contracts discovered: **14**
- Potential duplicate capability groups: **3**
- Live execution authority findings: **0**

### File categories

- `documentation`: 37
- `ephemeral`: 4
- `generated_or_market_data`: 20
- `other`: 18
- `python_source`: 13
- `registry_or_config`: 11

## Migration classification

- `ADAPT`: 4
- `DELETE_LATER`: 2
- `MIGRATE`: 6
- `REUSE_AS_IS`: 1
- `WRAP`: 3

## Capital authority finding

No executable `OrderSend`, `OrderCheck`, `CTrade`, or `mt5.order_send` call site was found. The audited snapshot has market-data access but no identified order-send authority.


## Test baseline

- Python compileall: **PASS**
- Pytest clean-checkout baseline: **FAIL**
- Pytest return code: `2`

The collection failure is a Phase 02 packaging concern, not evidence that the implemented market/anatomy logic is numerically wrong. It must still be corrected before shared-engine development.

## Primary migration decisions

1. Keep the laboratory philosophy and Python/MQL5 authority separation.
2. Adapt `MT5Connector` behind a vendor-neutral market-data port.
3. Wrap `MarketDataEngine` as a legacy provider until canonical bar/time contracts exist.
4. Wrap `LRuleNodeDetector` as an anatomy plugin; never move L-rule semantics into the kernel.
5. Wrap `M0001RTV` as a feature/label plugin and correct its interface drift under contract tests.
6. Replace three cache implementations with one versioned Artifact Store.
7. Migrate empty experiment/validation/production shells to manifest-driven runs.
8. Delete tracked bytecode and runtime caches after ignore rules are installed.

## Pilot decision

Phase 00 selects **CP0001 Structural Nodes + M0001 RTV** as the local foundation pilot because it is the only complete implemented chain in this archive. This does not replace the roadmap decision to use EXP0017 and NDS as later platform pilots; those codebases must first be present in the working repository.

## Risk profile

- `CRITICAL`: 1
- `HIGH`: 6
- `INFO`: 1
- `LOW`: 1
- `MEDIUM`: 1


## Phase gate

Phase 00 is accepted when the generated artifacts are reproducible, the authority scan remains clean or fully classified, every reusable module has a migration action, the pilot is explicit, and Phase 01 can consume the contract/schema map without undocumented assumptions.
