---
id: ENG-CI-20260722-CANONICAL-VAULT
title: "Engineering Policy CI Recovery - Canonical Vault Binding"
type: incident
status: active
deployment_status: pending-commit-and-push
version: 1.0.0
created: 2026-07-22
updated: 2026-07-22
owner: Decision Alpha Lab engineering
tags:
  - ai-engineering
  - ci
  - obsidian
  - incident
---
# Engineering Policy CI Recovery - Canonical Vault Binding

## Intent and scope

Restore the repository preflight after the approved LCM-15B documentation reorganization. This patch changes only CI/preflight routing, required policy entry points, action runtime majors, regression coverage, and their documentation. It does not change market doctrine, research behavior, schemas, execution authority, the vault validator, or generated compatibility locators.

## Current and desired behavior

- Current at base commit `b6207d127`: the preflight validates `docs/ai_algorithm_engineering_os`, which LCM-15B converted to generated compatibility locators. The committed tree reports 242 missing IDs and 20 ambiguous links.
- Desired: the preflight validates the authored canonical vault at `docs/alpha_lab_master_architecture/ai_algorithm_engineering_os` and preserves the same fail-closed validator behavior.
- Independent warning: the workflow uses Node 20 action majors. The bounded update is `actions/checkout@v5` and `actions/setup-python@v6`, both using Node 24.

## Root cause and evidence

The last successful run before the regression was commit `c5e10dac`. The first failing run was commit `bef162388`, which implemented LCM-15B. The workflow and validator did not change across that boundary; the validated path changed meaning from authored notes to compatibility redirects while the runner retained the legacy path.

At diagnosis time:

- legacy committed vault: 253 notes, 4 unique IDs, 262 errors;
- canonical vault: 253 notes, 247 unique IDs, 0 errors, 0 warnings;
- repository policy, MQL5 compatibility, and repository layout stages already passed.

## Invariants and failure behavior

- The canonical vault remains the single authored source of truth.
- Generated redirect content and its historical hash evidence remain untouched.
- Missing IDs, broken or ambiguous links, empty notes, and disallowed placeholders in the canonical vault still fail CI.
- Check order, summary output, subprocess isolation, and nonzero failure propagation remain unchanged.
- No trading, model-promotion, live-order, credential, schema, or capital authority is introduced.

## Verification and Definition of Done

The recovery is complete when the focused regression tests pass, the canonical validator reports zero errors and warnings, all four engineering-policy stages pass from the repository root, the workflow uses Node 24 action majors, and a clean base-plus-patch selected archive produces the same focused regression and canonical-vault result.

## Compatibility, rollback, and residual risk

No data migration is required. Existing legacy locators remain available to external consumers. The canonical OS changelog and notes are deliberately unchanged because LCM-15B receipts hash-bind those authored target bytes; this incident note records the operational correction instead. Rollback is an exact reversion of the bounded files, but it intentionally restores the known CI failure. Branch protection is outside this patch; `main` can still accept a commit before CI finishes unless repository settings are changed by an authorized owner.

## Related decisions and controls

- [[ALPHA_LAB_ENGINEERING_HANDBOOK|Engineering Handbook]]
- [[ALPHA_LAB_OBSIDIAN_KNOWLEDGE_STANDARD|Obsidian Knowledge Standard]]
- [[ALPHA_LAB_QUALITY_GATE_MATRIX|Quality Gate Matrix]]
- [[docs/alpha_lab_master_architecture/context_lifecycle_os/17_LEGACY_MIGRATION_PROGRAM/05_PHASES/LCM_15B_ROOT_RELEASE_AND_DOCUMENTATION_REORGANIZATION|LCM-15B Documentation Reorganization]]
- [[docs/alpha_lab_master_architecture/ai_algorithm_engineering_os/00_START_HERE/00_Home|Canonical Engineering OS Home]]
