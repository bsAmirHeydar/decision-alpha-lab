---
status: accepted-reference
version: 1.0.0
updated: 2026-07-20
tags: [acl-os, lcm, lcm-09b, setup-migration]
phase_id: LCM-09B
claim_ceiling: LCM_09B_REFERENCE_ONLY
---
# Operations Runbook

## Prerequisites

- place the patch ZIP and `APPLY_ALPHA_LAB_LCM_09B.bat` in repository root;
- use a Python environment with the repository test dependencies installed;
- ensure no unrelated staged changes exist;
- retain the original ZIP until installation verification completes.

## Automated path

The batch expands the archive with overwrite enabled, removes the consumed ZIP, compiles the changed Python modules, validates the generated package, runs phase-direct tests, runs bounded ACL-04 regression, runs QA, stages exact paths from `LCM_09B_FILE_INDEX.txt`, checks the staged diff, commits from `COMMIT_MESSAGE_LCM_09B.md`, and pushes.

The batch stops on the first failed gate. It never uses `git add .` or `git add -A`.

## Manual package verification

1. verify `LCM_09B_FILE_HASHES.sha256` against repository bytes;
2. verify the generated package manifest;
3. verify all 60 package digests and source bindings;
4. verify Factory registration count and authority fields;
5. verify parity record count and blocked dispositions;
6. verify handoff and locator digests;
7. run schema syntax and instance validation;
8. run direct tests and bounded regression;
9. inspect `git diff --cached --check` before commit.

## Rebuild operation

```powershell
python -m tools.strategy_factory.lcm.lcm_09b.cli build --repo-root . --output-root registry/legacy_context_migration/setup_package_migrations/SETUPMIGRATION_8F5CED333AA143A8F2A798BA01D550D9
```

A rebuild is allowed only from the exact accepted LCM-09A handoff. Compare the rebuilt output manifest and handoff digests before publication. A digest difference requires investigation; it must not be normalized away.

## Failure recovery

- extraction failure: do not stage; restore the ZIP and retry on a clean root;
- compile/test failure: leave files unstaged and inspect the first failure;
- manifest failure: discard the generated migration root and rebuild from bound input;
- source digest mismatch: stop; do not refresh the expected digest automatically;
- handoff mismatch: stop; a new phase amendment is required;
- Git staging mismatch: reset only paths in the exact index and inspect unrelated changes.

## Rollback

Before push, use `git restore --staged --pathspec-from-file=LCM_09B_FILE_INDEX.txt` followed by `git restore --pathspec-from-file=LCM_09B_FILE_INDEX.txt`; remove untracked indexed paths explicitly. After commit, use a normal revert commit. Legacy source requires no restoration because this phase moves, deletes, and edits no legacy source.
