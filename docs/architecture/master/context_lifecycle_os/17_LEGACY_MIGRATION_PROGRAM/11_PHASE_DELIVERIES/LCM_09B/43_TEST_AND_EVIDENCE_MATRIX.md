---
status: accepted-reference
version: 1.0.0
updated: 2026-07-20
tags: [acl-os, lcm, lcm-09b, setup-migration]
phase_id: LCM-09B
claim_ceiling: LCM_09B_REFERENCE_ONLY
---
# Test and Evidence Matrix

## Direct verification categories

| Requirement | Primary evidence | Direct tests |
|---|---|---|
| all frozen identities accounted | canonical registry, closure report | portfolio accounting |
| package fail-closed behavior | package files, evaluator | package and evaluator tests |
| no independent Context clock | package bindings, evaluator API | package boundary and known-time tests |
| no Treatment leakage | dependency seeds, package binding | Treatment boundary tests |
| Factory zero authority | registration registry, ACL-04 port | Factory and authority tests |
| adapter never executes legacy | adapter registry and implementation | adapter boundary tests |
| no false parity PASS | parity detail and registry | parity tests |
| restart integrity | checkpoint digest | restart tests |
| deterministic publication | rebuild, JSONL ordering, manifest | determinism tests |
| source immutability | source path/digest verification | source binding tests |
| schema conformance | Draft 2020-12 schemas | schema syntax and instance tests |
| package integrity | manifest, receipt, locator | full verification tests |
| no order/chart/network/process surface | static scanner | static boundary test |
| bounded next-phase handoff | handoff digest and false authority fields | handoff tests |

## Verification commands

```powershell
python -m compileall -q tools/strategy_factory/lcm/lcm_09b tools/strategy_factory/acl_os/acl_04/legacy_reference.py
python -m pytest -q lab/11_strategy_factory/migration/tests_lcm_09b
python -m pytest -q lab/11_strategy_factory/acl_os/tests_acl_04
python -m src.engine.tooling.strategy_factory.lcm.lcm_09b.cli verify-package --package-root registry/history/lcm/setup_package_migrations/SETUPMIGRATION_8F5CED333AA143A8F2A798BA01D550D9
python -m src.engine.tooling.strategy_factory.lcm.lcm_09b.cli qa --repo-root . --package-root registry/history/lcm/setup_package_migrations/SETUPMIGRATION_8F5CED333AA143A8F2A798BA01D550D9
```

## Non-claims

MetaEditor and MT5 are unavailable in the build environment. No MQL5 compile, Strategy Tester, terminal runtime, or cross-language behavioral parity claim is made. The phase does not modify MQL5, so this environment limit does not weaken the Python migration/tooling acceptance; it remains an explicit blocker for future per-identity executable migration.

## Baseline regression note

The supplied repository baseline contains two pre-existing manifest-integrity failures in LCM-08C and LCM-09A generated evidence. LCM-09B does not mutate those upstream artifacts. The QA report records the exact failing tests and proves that the same failures reproduce on a clean extraction of the supplied ZIP. Direct LCM-09B and ACL-04 bounded regression suites pass independently.
