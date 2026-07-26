# Alpha Lab LCM-05 — Target Topology and Repository Locator

## Scope

LCM-05 defines the target repository topology and deterministic locator plan for the entire classified repository. It does not move, delete, merge, refactor or cut over any legacy artifact.

## Reference output

- Topology Run ID: `TOPOLOGY_F28766C555330F0B89CC662DA8129220`
- Claim ceiling: `TARGET_TOPOLOGY_REFERENCE_ONLY`
- Acceptance state: `REFERENCE_TOPOLOGY_ACCEPTED_MATERIALIZATION_BLOCKED`
- Classified artifact mappings: 38,595
- Canonical identity package mappings: 2,792
- Identity ambiguity quarantine proposals: 2,040
- Root relocation plans: 1,076
- Documentation successor records: 121
- Resolved dependency edges evaluated: 101,389
- Legacy dependency-direction violations recorded: 2,126
- Unsafe proposed paths: 0
- Case-insensitive target collisions: 0

## Engineering boundaries

The patch creates control-plane registries, maps, policies, schemas, tests, static MQL5 contracts and Obsidian documentation. Every target remains non-materialized. Human ownership, security review, legacy behavioral parity, equivalence review, identity ambiguity resolution and MetaTrader runtime evidence remain blocking.

## Primary machine artifacts

- `registry/legacy_context_migration/target_paths/TOPOLOGY_F28766C555330F0B89CC662DA8129220/`
- `registry/legacy_context_migration/lcm_05/schemas/v1/`
- `registry/legacy_context_migration/lcm_05/policies/`
- `tools/strategy_factory/lcm/lcm_05/`
- `lab/11_strategy_factory/migration/tests_lcm_05/`

## Explicit non-claims

This patch does not claim migrated Contexts, migrated Setups, semantic equivalence, runtime parity, MetaEditor compilation, MT5 parity, source movement, source deletion, consumer cutover, order authority or capital authority.
