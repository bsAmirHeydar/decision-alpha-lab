# Alpha Lab LCM-06 — Migration Framework and Compatibility Layer

## Scope

LCM-06 implements the deterministic control plane required to migrate legacy Contexts, Setups, Treatments, Visualizers and platform adapters into ACL-OS without silently changing domain behavior. The phase supplies packet validation, alias/locator resolution, trace normalization and parity comparison, compatibility-adapter contracts, move-only planning, redirect previews, quarantine readiness and non-compensatory deletion gates.

LCM-06 is a reference framework. It does not move, delete, merge, refactor, cut over or materialize any legacy source or target package.

## Reference output

- Framework Run ID: `FRAMEWORK_066C5FA5795AA4C283B17271E4478751`
- Upstream Topology Run ID: `TOPOLOGY_F28766C555330F0B89CC662DA8129220`
- Claim ceiling: `MIGRATION_FRAMEWORK_REFERENCE_ONLY`
- Acceptance state: `REFERENCE_FRAMEWORK_ACCEPTED_NO_MIGRATION_EXECUTED`
- Migration packet fixtures: 5
- Packet results: 1 valid, 1 ambiguity-blocked, 1 security-review-blocked and 2 unknown-blocked
- Alias-resolution results: 3
- Trace comparisons: 3 — one PASS, one SOFT_MISMATCH and one HARD_MISMATCH
- Compatibility-adapter contracts: 4
- Move-plan previews: 1
- Redirect previews: 3
- Quarantine validations: 2
- Deletion validations: 2
- Framework registries: 9
- Framework contracts: 7
- Event-ledger events: 10
- Output-manifest artifacts: 37

## Hard engineering boundaries

- Unknown evidence blocks migration progression.
- Hard parity mismatches cannot be waived.
- Alias ambiguity is quarantined rather than guessed through.
- Compatibility adapters preserve known-time, event ordering, reason codes and authority boundaries.
- Move plans and redirects are preview-only.
- Quarantine validation does not move source files.
- Deletion validation does not delete source files.
- Shared-engine discovery may begin in LCM-07, but extraction remains unauthorized until equivalence is established.
- Runtime, live-order and capital authority remain false.

## Primary machine artifacts

- `registry/legacy_context_migration/frameworks/FRAMEWORK_066C5FA5795AA4C283B17271E4478751/`
- `registry/legacy_context_migration/lcm_06/schemas/v1/`
- `registry/legacy_context_migration/lcm_06/policies/`
- `registry/legacy_context_migration/lcm_06/registries/v1/`
- `tools/strategy_factory/lcm/lcm_06/`
- `lab/11_strategy_factory/migration/tests_lcm_06/`
- `lab/11_strategy_factory/mql5/Include/AlphaLab/ContextOS/Migration/LCM06/`

## Explicit non-claims

This patch does not claim migrated Contexts, migrated Setups, behavioral equivalence for a real legacy module, MetaEditor compilation, MT5 runtime parity, shared-engine extraction, source movement, source deletion, target materialization, semantic refactoring, consumer cutover, runtime authority, live-order authority or capital authority.
